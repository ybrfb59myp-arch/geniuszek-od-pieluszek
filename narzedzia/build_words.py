"""Buduje slowa.js z listy słów w narzedzia/slowa.txt (opis źródeł – w nagłówku tego pliku).

Słowa są grupowane po liczbie liter: 3, 4, 5, 6, 7, 8 i "9+" (9 i więcej).
Dla każdego słowa liczy się podział na karty z talii oraz dwie flagi:
  z – da się je ułożyć z jednego zestawu kart,
  d – zawiera dwuznak lub zmiękczenie (osobna karta, np. „sz”, „ci”).

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
KARTY = {c: 1 for c in "aąbcćdeęfghijklłmnńoóprsśtuwyzźż"}
for c in "aeimot":
    KARTY[c] = 2
for c in ["cz", "ch", "sz", "rz", "dż", "dzi", "dź", "ni", "si", "ci", "dz", "zi"]:
    KARTY[c] = 1
WIELOZNAKI = sorted([k for k in KARTY if len(k) > 1], key=len, reverse=True)


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
        potrzeba = {k: karty.count(k) for k in karty}
        z_zestawu = all(KARTY.get(k, 0) >= n for k, n in potrzeba.items())
        dwuznak = any(len(k) > 1 for k in karty)
        dane.setdefault(grupa(w), []).append({"s": w, "k": karty, "z": z_zestawu, "d": dwuznak})
    dane = dict(sorted(dane.items(), key=lambda kv: int(kv[0].rstrip("+"))))

    for dl, l in dane.items():
        print(f"{dl:>2} liter: {len(l):4} słów | {sum(x['z'] for x in l):4} z 1 zestawu | "
              f"{sum(not x['d'] for x in l):4} bez dwuznaków | {sum(x['z'] and not x['d'] for x in l):4} oba warunki")
    razem = [x for l in dane.values() for x in l]
    print(f"RAZEM:    {len(razem):4} słów | {sum(x['z'] for x in razem):4} z 1 zestawu | "
          f"{sum(not x['d'] for x in razem):4} bez dwuznaków | {sum(x['z'] and not x['d'] for x in razem):4} oba warunki")
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
            f.write("// s = słowo, k = karty po kolei, z = da się ułożyć z jednego zestawu, d = ma dwuznak/zmiękczenie\n")
            f.write("window.SLOWA = ")
            json.dump(dane, f, ensure_ascii=False, separators=(",", ":"))
            f.write(";\n")
