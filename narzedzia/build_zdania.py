"""Buduje zdania.js – składniki, z których aplikacja układa zdania z 2–5 wyrazów.

Dane (podmioty, miejsca, czynności, czasowniki, przymiotniki) są w zdania_dane.py.
Ten skrypt je sprawdza i zapisuje w zdania.js; same zdania układa generator.js w aplikacji.
Na koniec uruchamia narzedzia/zdania_narzedzie.js (jeśli jest node), które liczy pulę zdań
(zdania-liczby.js) i zapisuje przykłady do przejrzenia (narzedzia/zdania-przyklady.txt).

Użycie:
  python3 narzedzia/build_zdania.py zdania.js [--sjp slowa-sjp.txt]
      --sjp: sprawdź każdy wyraz w słowniku do gier SJP.pl (plik z https://sjp.pl/sl/growy/)
"""
import json, os, shutil, subprocess, sys, unicodedata

TU = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TU)
from build_words import na_karty, KARTY, wczytaj_slowa, klucz_sortowania  # noqa: E402
import zdania_dane as D                                                    # noqa: E402

PRZYIMKI = {"w", "na", "pod", "nad", "za", "przy", "u", "przed"}
bledy = []


def blad(tekst):
    bledy.append(tekst)


def rozwin(spec, nazwa="?"):
    """„@grupa|na stole|je zupę” -> (grupy miejsc, grupy czynności, pojedyncze miejsca, pojedyncze czynności)"""
    gm, gc, m, c = [], [], [], []
    for el in spec.split("|"):
        el = " ".join(el.split())
        if not el:
            continue
        if el.startswith("@"):
            k = el[1:]
            if k in D.M:
                gm.append(k)
            elif k in D.C:
                gc.append(k)
            else:
                blad(f"nieznana grupa @{k} (w: {nazwa})")
        else:
            if len(el.split()) != 2:
                blad(f"wyrażenie musi mieć 2 wyrazy: {el!r} (w: {nazwa})")
            (m if el.split()[0] in PRZYIMKI else c).append(el)
    return gm, gc, m, c


def lista_fraz(spec):
    return [" ".join(x.split()) for x in spec.split("|") if x.strip()]


def podmioty_z(spec, nazwa="?"):
    """„@koty pies” -> lista podmiotów"""
    out = []
    for el in spec.split():
        if el.startswith("@"):
            if el[1:] not in D.KAT:
                blad(f"nieznana kategoria {el} (w: {nazwa})")
                continue
            out += D.KAT[el[1:]].split()
        else:
            out.append(el)
    return out


def rodzaj(s):
    for r, lista in D.RODZAJ_WYJATKI.items():
        if s in lista.split():
            return r
    if s[-1] == "a":
        return "ż"
    if s[-1] in "oeę":
        return "n"
    return "m"


def formy_przymiotnika(m):
    """mały -> (mały, mała, małe); wysoki -> (wysoki, wysoka, wysokie)"""
    rdzen = m[:-1]
    if m[-1] == "i" and rdzen[-1] in "kg":
        return m, rdzen + "a", rdzen + "ie"
    return m, rdzen + "a", rdzen + "e"


def bez_ogonkow(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.replace("ł", "l")) if unicodedata.category(c) != "Mn")


def zbuduj():
    # --- podmioty i ich miejsca / czynności ---
    pod = {}
    for podmioty, spec in D.P:
        gm, gc, m, c = rozwin(spec, podmioty)
        for p in podmioty.split():
            x = pod.setdefault(p, {"mg": [], "m": [], "cg": [], "c": [], "v": [], "a": [], "p": []})
            for klucz, nowe in (("mg", gm), ("m", m), ("cg", gc), ("c", c)):
                x[klucz] += [e for e in nowe if e not in x[klucz]]
    wszystkie = set(pod)
    for nazwa, lista in D.KAT.items():
        for p in lista.split():
            if p not in wszystkie:
                blad(f"kategoria {nazwa}: nieznany podmiot {p}")
    for p in pod:
        if not any(p in l.split() for l in D.KAT.values()):
            blad(f"podmiot {p} nie należy do żadnej kategorii (KAT)")
    slowa = set(wczytaj_slowa())
    for p in pod:
        if p not in slowa and p not in D.LICZBA_MNOGA:
            blad(f"podmiot {p}: nie ma go w narzedzia/slowa.txt")

    # --- rodzaj, liczba, „żywe”, ludzie ---
    zywe, ludzie = set(podmioty_z(D.ZYWE)), set(podmioty_z(D.LUDZIE))
    for p, x in pod.items():
        if p in D.LICZBA_MNOGA:
            x["mn"] = 1
        else:
            x["r"] = rodzaj(p)
        if p in zywe:
            x["z"] = 1
        if p in ludzie:
            x["l"] = 1

    # --- czasowniki ---
    for podmioty, spec in D.PV:
        for el in lista_fraz(spec):
            czas, _, regula = el.partition(":")
            regula = regula or D.DOMYSLNA.get(czas, "*")
            if regula not in ("*", "-") and regula not in D.REG:
                blad(f"nieznana reguła {regula} ({czas}, {podmioty})")
            for p in podmioty_z(podmioty, spec):
                if p not in pod:
                    blad(f"PV: nieznany podmiot {p}"); continue
                if "mn" in pod[p]:
                    blad(f"PV: {p} jest w liczbie mnogiej – bez czasowników"); continue
                if not any(v.split(":")[0] == czas for v in pod[p]["v"]):
                    pod[p]["v"].append(f"{czas}:{regula}")

    # --- przymiotniki ---
    for podmioty, spec in D.PA:
        for a in spec.split():
            if a not in D.PRZYMIOTNIKI:
                blad(f"PA: nieznany przymiotnik {a} ({podmioty})")
        for p in podmioty_z(podmioty, spec):
            if p not in pod:
                blad(f"PA: nieznany podmiot {p}"); continue
            if "mn" in pod[p]:
                continue
            pod[p]["a"] += [a for a in spec.split() if a not in pod[p]["a"]]

    # --- pary do „i” ---
    def para(a, b):
        for x, y in ((a, b), (b, a)):
            if x in pod and y in pod and y not in pod[x]["p"]:
                pod[x]["p"].append(y)
    for nazwa in D.PARY_W_KATEGORIACH:
        lista = D.KAT[nazwa].split()
        for i, a in enumerate(lista):
            for b in lista[i + 1:]:
                if (bez_ogonkow(a)[:2] != bez_ogonkow(b)[:2] and f"{a}-{b}" not in D.NIE_PARY
                        and f"{b}-{a}" not in D.NIE_PARY and a not in D.BEZ_PAR_AUTO and b not in D.BEZ_PAR_AUTO):
                    para(a, b)
    for el in D.PARY_DODATKOWE:
        a, b = el.split("-")
        if a not in pod or b not in pod:
            blad(f"PARY_DODATKOWE: nieznany podmiot w {el}")
        para(a, b)

    # --- wykluczone połączenia podmiot + wyrażenie ---
    wykl = {}
    for p, fraza in sorted(D.WYKLUCZONE_PARY):
        wykl.setdefault(p, []).append(fraza)

    for k in D.GDZIE:
        if k not in D.C:
            blad(f"GDZIE: nieznana grupa czynności {k}")

    # porządek: usuń puste pola
    for x in pod.values():
        for k in [k for k, v in x.items() if v == []]:
            del x[k]

    return {
        "M": {k: lista_fraz(v) for k, v in D.M.items()},
        "C": {k: lista_fraz(v) for k, v in D.C.items()},
        "reg": {k: sorted(v, key=klucz_sortowania) for k, v in D.REG.items()},
        "przym": {a: list(formy_przymiotnika(a)) for a in D.PRZYMIOTNIKI},
        "zlePary": D.ZLE_PARY,
        "gdzie": {k: lista_fraz(v) for k, v in D.GDZIE.items()},
        "bezOdwracania": sorted(D.BEZ_ODWRACANIA, key=klucz_sortowania),
        "wymagaMiejsca": sorted(D.WYMAGA_MIEJSCA),
        "zleAV": [x.replace("_", " ") for x in D.ZLE_AV],
        "bezPar": sorted(D.PARY_BEZ_MIEJSC, key=klucz_sortowania),
        "smieszne": {"miejsca": sorted(D.SMIESZNE_MIEJSCA, key=klucz_sortowania),
                     "przymLudzie": D.SMIESZNE_PRZYM_LUDZIE, "przymReszta": D.SMIESZNE_PRZYM_RESZTA,
                     "vZwierzece": D.SMIESZNE_V_ZWIERZECE, "vLudzkie": D.SMIESZNE_V_LUDZKIE,
                     "bezSlow": sorted(D.SMIESZNE_BEZ_SLOW)},
        "wykl": wykl,
        "podmioty": dict(sorted(pod.items(), key=lambda kv: klucz_sortowania(kv[0]))),
    }


def wszystkie_wyrazy(dane):
    w = set("to jest tu i".split())
    for grupy in (dane["M"], dane["C"], dane["gdzie"]):
        for l in grupy.values():
            for f in l:
                w.update(f.split())
    for f in dane["przym"].values():
        w.update(f)
    for p, x in dane["podmioty"].items():
        w.add(p)
        for f in x.get("m", []) + x.get("c", []):
            w.update(f.split())
        for v in x.get("v", []):
            w.update(v.split(":")[0].split())
    return w


if __name__ == "__main__":
    arg = sys.argv[1:]
    sjp = None
    if "--sjp" in arg:
        i = arg.index("--sjp")
        with open(arg[i + 1], encoding="utf-8") as f:
            sjp = set(l.strip() for l in f)
        del arg[i:i + 2]

    dane = zbuduj()
    wyrazy = wszystkie_wyrazy(dane)
    for w in sorted(wyrazy):
        for k in na_karty(w):
            if k not in KARTY:
                blad(f"{w}: brak karty „{k}”")
    if sjp is not None:
        jednoliterowe = {"w", "u", "z", "i", "a", "o"}   # słownik do gier nie ma wyrazów 1-literowych
        brak = sorted(w for w in wyrazy if w not in sjp and w not in jednoliterowe)
        if brak:
            blad("wyrazów nie ma w słowniku do gier SJP.pl: " + ", ".join(brak))
    # miejsca z reguł, których nie ma żaden podmiot (zwykle literówka)
    znane = {f for l in dane["M"].values() for f in l} | {f for x in dane["podmioty"].values() for f in x.get("m", [])}
    for nazwa, l in dane["reg"].items():
        obce = [f for f in l if f not in znane]
        if obce:
            blad(f"reguła {nazwa}: miejsca, których nie ma żaden podmiot: {', '.join(obce)}")
    for nazwa, l in (("BEZ_ODWRACANIA", dane["bezOdwracania"]), ("PARY_BEZ_MIEJSC", dane["bezPar"]),
                     ("SMIESZNE_MIEJSCA", dane["smieszne"]["miejsca"])):
        for f in l:
            if f not in znane:
                blad(f"{nazwa}: nieznane miejsce {f}")
    czasowniki = {v.split(":")[0] for x in dane["podmioty"].values() for v in x.get("v", [])}
    for v in dane["smieszne"]["vZwierzece"] + dane["smieszne"]["vLudzkie"] + dane["wymagaMiejsca"] + [x.split("-")[1] for x in dane["zleAV"]]:
        if v not in czasowniki:
            blad(f"nieznany czasownik {v} (listy śmiesznych / WYMAGA_MIEJSCA / ZLE_AV)")
    for x in dane["zleAV"] + dane["zlePary"]:
        for a in x.split("-")[:1] + ([] if x in dane["zleAV"] else x.split("-")[1:]):
            if a not in dane["przym"]:
                blad(f"nieznany przymiotnik {a} w {x}")
    for a in dane["smieszne"]["przymLudzie"] + dane["smieszne"]["przymReszta"]:
        if a not in dane["przym"]:
            blad(f"nieznany przymiotnik {a} (śmieszne)")
    if bledy:
        print("\n".join(bledy)); sys.exit(1)

    pod = dane["podmioty"]
    print(f"Podmiotów: {len(pod)} (w liczbie mnogiej: {sum('mn' in x for x in pod.values())}) | "
          f"wyrazów: {len(wyrazy)} | przymiotników: {len(dane['przym'])} | "
          f"czasowników: {len({v.split(':')[0] for x in pod.values() for v in x.get('v', [])})}")
    bez_v = [p for p, x in pod.items() if "v" not in x and "mn" not in x]
    bez_a = [p for p, x in pod.items() if "a" not in x and "mn" not in x]
    if bez_v: print("bez czasownika:", " ".join(bez_v))
    if bez_a: print("bez przymiotnika:", " ".join(bez_a))

    if arg:
        with open(arg[0], "w", encoding="utf-8") as f:
            f.write("// Składniki zdań dla aplikacji Geniuszek od Pieluszek (wygenerowane przez narzedzia/build_zdania.py\n")
            f.write("// z narzedzia/zdania_dane.py – nie edytować ręcznie). Zdania układa z nich generator.js.\n")
            f.write("window.ZDANIA = ")
            json.dump(dane, f, ensure_ascii=False, separators=(",", ":"))
            f.write(";\n")
        narzedzie = os.path.join(TU, "zdania_narzedzie.js")
        if shutil.which("node") and os.path.exists(narzedzie):
            subprocess.run(["node", narzedzie], check=True)
        else:
            print("Uwaga: brak node – nie przeliczono puli zdań (zdania-liczby.js).")
