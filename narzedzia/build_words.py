"""Buduje slowa.js: listy prostych słów dla 2–5-latków, pogrupowane po liczbie liter.

Źródło kandydatów: aztekium.pl (lista ogólna "Wyrazy" 3/4/5/6 liter + kategorie:
owoce, zwierzęta, zabawki, przedmioty), uzupełnione kilkoma potocznymi słowami
z mowy dziecięcej, których aztekium nie ma (np. lody, buty, lizak, nocnik).
Wybór: konkretne, obrazowe rzeczowniki z codziennego świata dziecka.
"""
import json, sys

SLOWA = {
    3: """dom kot koń lis lew jeż miś nos oko osa ser sok sos ząb żuk wąż las lód koc nóż
          byk bąk but dym dąb gęś kij ryż sól zoo łoś paw rak wóz mak ćma mur pas róg noc łuk wąs""",
    4: """kura koza pies foka lama sowa mysz wilk żaba żółw owca słoń krab kret ryba ptak dzik
          mewa smok bóbr kruk zupa miód dżem lody tort jajo kiwi figa kawa noga ręka ucho usta
          oczy zęby pupa dach okno stół kran piec kosz klej auto kula koło list mapa piła most
          płot buty lala guma kask igła mama tata brat pani król góra woda zima lato łąka liść
          róża łódź buda park łapa nora""",
    5: """krowa kogut osioł zając jeleń sarna zebra małpa panda koala rekin motyl mucha pająk
          orzeł gołąb indyk kotek baran chleb masło mleko kasza banan arbuz mango melon dynia
          groch burak rzepa kokos pizza bułka rogal kakao lizak jajko żelki głowa palec buzia
          włosy plecy szyja stopa pięta język serce piłka lalka balon farba kubek rower sanki
          narty zegar lampa radio klucz torba bluza pasek guzik drzwi łóżko szafa półka fotel
          wanna mydło miska łyżka słoik wózek łódka motor dźwig kocyk łyżwy niebo śnieg kwiat trawa
          wiatr rzeka morze plaża ogień błoto grzyb tęcza burza dzień ogród brama wujek pirat
          pilot""",
    6: """kaczka myszka świnia żyrafa tygrys kangur delfin chomik królik bocian papuga wróbel
          mrówka ślimak borsuk piesek jabłko śliwka wiśnia malina cebula ogórek fasola orzech
          ciasto pączek kotlet jogurt keczup cukier sałata frytki jagoda brzuch kolano łokieć
          czapka szalik kurtka sweter bluzka majtki piżama kapcie kredka klocki pędzel ołówek
          plecak garnek talerz wiadro miotła pralka schody balkon budzik kołdra nocnik kanapa
          lustro pociąg statek kartka zeszyt koszyk drzewo słońce chmura deszcz piasek
          kamień kałuża brzoza babcia ciocia lekarz rycerz wróżka""",
}

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


def main():
    dane, bledy = {}, []
    for dl, tekst in SLOWA.items():
        lista = tekst.split()
        if len(set(lista)) != len(lista):
            bledy.append(f"duplikaty w {dl}: {[w for w in lista if lista.count(w) > 1]}")
        for w in lista:
            if len(w) != dl:
                bledy.append(f"{w}: {len(w)} liter, a jest na liście {dl}")
            for k in na_karty(w):
                if k not in KARTY:
                    bledy.append(f"{w}: brak karty '{k}'")
        dane[dl] = []
        for w in sorted(set(lista), key=lambda s: s.replace("ą", "a~").replace("ć", "c~").replace("ę", "e~")
                        .replace("ł", "l~").replace("ń", "n~").replace("ó", "o~").replace("ś", "s~")
                        .replace("ź", "z~").replace("ż", "z~~")):
            karty = na_karty(w)
            potrzeba = {k: karty.count(k) for k in karty}
            z_zestawu = all(KARTY.get(k, 0) >= n for k, n in potrzeba.items())
            dwuznak = any(len(k) > 1 for k in karty)
            dane[dl].append({"s": w, "k": karty, "z": z_zestawu, "d": dwuznak})
    if bledy:
        print("\n".join(bledy)); sys.exit(1)
    for dl, l in dane.items():
        print(dl, "liter:", len(l), "słów |", sum(x["z"] for x in l), "da się ułożyć z 1 zestawu |",
              sum(not x["d"] for x in l), "bez dwuznaków |",
              sum(x["z"] and not x["d"] for x in l), "oba warunki")
    return dane


if __name__ == "__main__":
    dane = main()
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf-8") as f:
            f.write("// Listy słów dla aplikacji Geniuszek od Pieluszek (wygenerowane przez build_words.py)\n")
            f.write("// s = słowo, k = karty po kolei, z = da się ułożyć z jednego zestawu, d = ma dwuznak/zmiękczenie\n")
            f.write("window.SLOWA = ")
            json.dump({str(k): v for k, v in dane.items()}, f, ensure_ascii=False, separators=(",", ":"))
            f.write(";\n")
