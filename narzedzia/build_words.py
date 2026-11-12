"""Buduje slowa.js i talia.js z listy słów w narzedzia/slowa.txt (opis źródeł – w nagłówku tego pliku).

Słowa są grupowane po liczbie liter: 3, 4, 5, 6, 7, 8 i "9+" (9 i więcej).
Dla każdego słowa liczy się podział na karty z talii oraz:
  t – z ilu talii da się je ułożyć (1, 2 albo 3 = potrzeba więcej niż dwóch),
  d – czy zawiera dwuznak lub zmiękczenie (osobna karta, np. „sz”, „ci”).
talia.js zawiera skład jednej talii (KARTY poniżej) – aplikacja sprawdza nim, czy zdanie da się ułożyć.

Użycie:
  python3 narzedzia/build_words.py slowa.js                # zbuduj slowa.js
  python3 narzedzia/build_words.py slowa.js --sjp slowa-sjp.txt
      # dodatkowo sprawdź, czy każde słowo jest w słowniku do gier SJP.pl
      # (plik slowa.txt z https://sjp.pl/sl/growy/ – za duży, żeby trzymać go w repozytorium)
"""
import json, os, sys

PLIK_SLOW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "slowa.txt")
MIN_LITER = 3

# Karty w talii (strona z literą). Liczba = ile takich kart jest w jednym zestawie.
# Talia 51 kart: A ×3; E, K, M, O, T ×2; pozostałe po jednej. Skład wyliczony tak, żeby z jednej talii
# dało się ułożyć jak najwięcej słów z listy (ok. 89%), przy zachowaniu słów „mama” i „tata”.
KARTY = {c: 1 for c in "aąbcćdeęfghijklłmnńoóprsśtuwyzźż"}
KARTY["a"] = 3
for c in "ekmot":
    KARTY[c] = 2
for c in ["cz", "ch", "sz", "rz", "dż", "dzi", "dź", "ni", "si", "ci", "dz", "zi"]:
    KARTY[c] = 1
WIELOZNAKI = sorted([k for k in KARTY if len(k) > 1], key=len, reverse=True)

# Najwięcej talii, z ilu układamy (w aplikacji wybór: 1 albo 2 talie).
TALIE = 2


def miesci_sie(karty, talie=TALIE):
    """Czy z podanych kart (lista) da się ułożyć tekst, mając `talie` zestawów kart."""
    return all(KARTY.get(k, 0) * talie >= karty.count(k) for k in set(karty))


def ile_talii(karty):
    """Z ilu talii da się to ułożyć: 1, 2, … albo TALIE + 1, gdy potrzeba więcej niż TALIE."""
    return next((t for t in range(1, TALIE + 1) if miesci_sie(karty, t)), TALIE + 1)


def na_karty(slowo):
    """Dzieli słowo na karty: najpierw dzi, potem dwuznaki, potem pojedyncze litery."""
    out, i = [], 0
    while i < len(slowo):
        for z in WIELOZNAKI:
            if slowo.startswith(z, i):
                out.append(z); i += len(z); break
        else:
            out.append(slowo[i]); i += 1
    return out


def wczytaj_slowa(plik=PLIK_SLOW):
    slowa = []
    with open(plik, encoding="utf-8") as f:
        for linia in f:
            linia = linia.strip()
            if linia and not linia.startswith("#"):
                slowa += linia.split()
    return slowa


def klucz_sortowania(s):
    return (s.replace("ą", "a~").replace("ć", "c~").replace("ę", "e~").replace("ł", "l~")
             .replace("ń", "n~").replace("ó", "o~").replace("ś", "s~").replace("ź", "z~").replace("ż", "z~~"))


def grupa(slowo):
    return str(len(slowo)) if len(slowo) < 9 else "9+"


def main(sjp=None):
    lista, bledy = wczytaj_slowa(), []
    widziane = set()
    for w in lista:
        if w in widziane:
            bledy.append(f"duplikat: {w}")
        widziane.add(w)
        if w != w.lower():
            bledy.append(f"{w}: tylko małe litery")
        if len(w) < MIN_LITER:
            bledy.append(f"{w}: za krótkie (min. {MIN_LITER} litery)")
        for k in na_karty(w):
            if k not in KARTY:
                bledy.append(f"{w}: brak karty '{k}'")
        if sjp is not None and w not in sjp:
            bledy.append(f"{w}: nie ma w słowniku do gier SJP.pl")
    if bledy:
        print("\n".join(bledy)); sys.exit(1)

    dane = {}
    for w in sorted(widziane, key=klucz_sortowania):
        karty = na_karty(w)
        dwuznak = any(len(k) > 1 for k in karty)
        dane.setdefault(grupa(w), []).append({"s": w, "k": karty, "t": ile_talii(karty), "d": dwuznak})
    dane = dict(sorted(dane.items(), key=lambda kv: int(kv[0].rstrip("+"))))

    def wiersz(nazwa, l):
        print(f"{nazwa}: {len(l):4} słów | {sum(x['t'] == 1 for x in l):4} z 1 talii | "
              f"{sum(x['t'] <= 2 for x in l):4} z 2 talii | {sum(not x['d'] for x in l):4} bez dwuznaków | "
              f"{sum(x['t'] == 1 and not x['d'] for x in l):4} z 1 talii bez dwuznaków")
    for dl, l in dane.items():
        wiersz(f"{dl:>2} liter", l)
    wiersz("   RAZEM", [x for l in dane.values() for x in l])
    return dane


if __name__ == "__main__":
    argumenty = sys.argv[1:]
    sjp = None
    if "--sjp" in argumenty:
        i = argumenty.index("--sjp")
        with open(argumenty[i + 1], encoding="utf-8") as f:
            sjp = set(l.strip() for l in f)
        del argumenty[i:i + 2]
    dane = main(sjp)
    if argumenty:
        with open(argumenty[0], "w", encoding="utf-8") as f:
            f.write("// Listy słów dla aplikacji Geniuszek od Pieluszek (wygenerowane przez narzedzia/build_words.py)\n")
            f.write("// s = słowo, k = karty po kolei, t = z ilu talii da się ułożyć (3 = więcej niż dwie), d = ma dwuznak/zmiękczenie\n")
            f.write("window.SLOWA = ")
            json.dump(dane, f, ensure_ascii=False, separators=(",", ":"))
            f.write(";\n")
        with open(os.path.join(os.path.dirname(os.path.abspath(argumenty[0])), "talia.js"), "w", encoding="utf-8") as f:
            f.write("// Skład jednej talii: karta -> liczba sztuk (wygenerowane przez narzedzia/build_words.py)\n")
            f.write("window.TALIA = ")
            json.dump(KARTY, f, ensure_ascii=False, separators=(",", ":"))
            f.write(";\n")
