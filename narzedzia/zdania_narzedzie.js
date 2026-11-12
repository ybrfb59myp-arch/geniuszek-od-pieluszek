// Liczy pulę zdań i zapisuje przykłady do przejrzenia. Uruchamiane przez build_zdania.py
// (albo ręcznie: node narzedzia/zdania_narzedzie.js [--wszystkie plik.txt]).
//  - zdania-liczby.js: ile jest zdań sensownych w każdym trybie, dla 1 i 2 talii, z dwuznakami i bez
//  - narzedzia/zdania-przyklady.txt: po kilkadziesiąt przykładów każdego wzoru zdania
//  - --wszystkie plik.txt: zapisz wszystkie zdania sensowne (duży plik, do kontroli)
"use strict";
const fs = require("fs"), path = require("path");
const KAT = path.join(__dirname, "..");
global.window = {};
require(path.join(KAT, "talia.js"));
require(path.join(KAT, "zdania.js"));
const { utworz } = require(path.join(KAT, "generator.js"));

function losowa(ziarno) {            // powtarzalne losowanie, żeby plik przykładów nie zmieniał się bez powodu
  return () => { ziarno |= 0; ziarno = ziarno + 0x6D2B79F5 | 0; let t = Math.imul(ziarno ^ ziarno >>> 15, 1 | ziarno);
                 t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
const rnd = losowa(20261112);
const G = utworz(window.ZDANIA, window.TALIA, rnd);
const NAZWY_TRYBOW = { k: "Zdania krótkie (2–3 wyrazy)", d: "Zdania długie (4–5 wyrazów)" };
const ILE_PRZYKLADOW = 30;

const argWszystkie = process.argv.indexOf("--wszystkie");
const plikWszystkie = argWszystkie > 0 ? fs.createWriteStream(process.argv[argWszystkie + 1]) : null;

const liczby = {}, przyklady = [];
for (const tryb of ["k", "d"]) {
  const wzory = {};                                    // wzór -> { n, t1, t2, probka }
  const razem = { n: 0, 1: [0, 0], 2: [0, 0], slowa: {}, slowa1: {}, slowa2: {} };
  G.wylicz(tryb, (w, wz) => {
    const x = wzory[wz] = wzory[wz] || { n: 0, t1: 0, t2: 0, probka: [] };
    const t = G.ileTalii(w, 2), dw = G.maDwuznak(w);
    x.n++; razem.n++;
    razem.slowa[w.length] = (razem.slowa[w.length] || 0) + 1;
    if (t <= 1) { x.t1++; razem[1][0]++; if (!dw) razem[1][1]++; razem.slowa1[w.length] = (razem.slowa1[w.length] || 0) + 1; }
    if (t <= 2) { x.t2++; razem[2][0]++; if (!dw) razem[2][1]++; razem.slowa2[w.length] = (razem.slowa2[w.length] || 0) + 1; }
    if (x.probka.length < ILE_PRZYKLADOW) x.probka.push(w.join(" "));           // próbka losowa (reservoir)
    else { const j = Math.floor(rnd() * x.n); if (j < ILE_PRZYKLADOW) x.probka[j] = w.join(" "); }
    if (plikWszystkie) plikWszystkie.write(w.join(" ") + "\n");
  });
  liczby[tryb] = { wszystkie: razem.n, 1: razem[1], 2: razem[2] };
  const proc = (a, b) => (100 * a / b).toFixed(1) + "%";
  console.log(`${NAZWY_TRYBOW[tryb]}: ${razem.n} zdań sensownych | 1 talia: ${razem[1][0]} (${proc(razem[1][0], razem.n)}) | ` +
              `2 talie: ${razem[2][0]} (${proc(razem[2][0], razem.n)}) | bez dwuznaków: 1 talia ${razem[1][1]}, 2 talie ${razem[2][1]} | ` +
              `wg liczby wyrazów: ${JSON.stringify(razem.slowa)}, z tego 1 talia ${JSON.stringify(razem.slowa1)}, 2 talie ${JSON.stringify(razem.slowa2)}`);
  przyklady.push("", "=".repeat(90), `${NAZWY_TRYBOW[tryb]} – SENSOWNE: ${razem.n} zdań (1 talia: ${razem[1][0]}, 2 talie: ${razem[2][0]})`, "=".repeat(90));
  for (const [wz, x] of Object.entries(wzory)) {
    console.log(`   ${wz.padEnd(13)} ${String(x.n).padStart(8)} | 1 talia ${String(x.t1).padStart(7)} | 2 talie ${String(x.t2).padStart(8)}`);
    przyklady.push("", `--- wzór ${wz}: ${x.n} zdań (1 talia: ${x.t1}, 2 talie: ${x.t2})`, ...x.probka);
  }
  // śmieszne: próbka wg wzoru
  const sm = {};
  for (let i = 0; i < 6000; i++) {
    const r = G.losujSmieszne(tryb, { talie: 2, bez: false });
    if (r) (sm[r.wzor] = sm[r.wzor] || new Set()).add(r.w.join(" "));
  }
  przyklady.push("", "=".repeat(90), `${NAZWY_TRYBOW[tryb]} – ŚMIESZNE (przykłady; w aplikacji mniej więcej co czwarte zdanie)`, "=".repeat(90));
  for (const [wz, s] of Object.entries(sm)) przyklady.push("", `--- wzór ${wz}`, ...[...s].slice(0, ILE_PRZYKLADOW));
}
if (plikWszystkie) plikWszystkie.end();

// kontrola losowania: czy zawsze coś się losuje i ile zdań jest śmiesznych
for (const tryb of ["k", "d"]) for (const talie of [1, 2]) for (const bez of [false, true]) {
  let brak = 0, sm = 0, talia1 = 0; const N = 3000, t0 = Date.now();
  for (let i = 0; i < N; i++) {
    const r = G.losuj(tryb, { talie, bezDwuznakow: bez });
    if (!r) brak++; else { if (r.smieszne) sm++; if (G.ileTalii(r.w, 2) > talie || (bez && G.maDwuznak(r.w))) throw new Error("zły filtr: " + r.s); }
  }
  console.log(`losowanie tryb=${tryb} talie=${talie} bezDwuznaków=${bez}: brak ${brak}/${N}, śmieszne ${(100 * sm / (N - brak)).toFixed(0)}%, ` +
              `${((Date.now() - t0) / N).toFixed(2)} ms/zdanie`);
}

fs.writeFileSync(path.join(KAT, "zdania-liczby.js"),
  "// Liczba zdań sensownych: tryb (k = krótkie, d = długie) -> liczba talii -> [wszystkie, bez dwuznaków]\n" +
  "// (wygenerowane przez narzedzia/zdania_narzedzie.js)\n" +
  "window.ZDANIA_LICZBY = " + JSON.stringify(liczby) + ";\n");
fs.writeFileSync(path.join(__dirname, "zdania-przyklady.txt"),
  "# Przykłady zdań układanych przez aplikację (wygenerowane – nie edytować ręcznie).\n" +
  "# Zdania sensowne są wyliczone w całości, tu jest losowa próbka każdego wzoru.\n" + przyklady.join("\n") + "\n");
