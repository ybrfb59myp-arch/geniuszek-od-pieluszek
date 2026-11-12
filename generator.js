// Generator zdań dla aplikacji Geniuszek od Pieluszek.
// Układa zdania z 2–5 wyrazów ze składników w zdania.js (podmioty, miejsca, czynności, czasowniki,
// przymiotniki) i sprawdza, czy zdanie da się ułożyć z talii (talia.js).
// Zdania sensowne: podmiot + elementy, które są do niego przypisane („kot śpi na kanapie”).
// Zdania śmieszne: podmiot + element, który NIE jest do niego przypisany („krowa miauczy na szafie”).
// Ten sam plik działa w przeglądarce (window.GeneratorZdan) i w node (narzedzia/zdania_narzedzie.js).
(function (root) {
"use strict";

function utworz(D, TALIA, losowa) {
  const rnd = losowa || Math.random;
  const los = n => Math.floor(rnd() * n);
  const uniq = t => [...new Set(t)];

  // ----- karty -----
  const WIELOZNAKI = Object.keys(TALIA).filter(k => k.length > 1).sort((a, b) => b.length - a.length);
  const pamiecKart = new Map();
  // Dzieli wyraz na karty: najpierw dzi, potem dwuznaki, potem pojedyncze litery (jak build_words.py).
  function naKarty(wyraz) {
    let k = pamiecKart.get(wyraz);
    if (!k) {
      k = [];
      for (let i = 0; i < wyraz.length;) {
        const z = WIELOZNAKI.find(x => wyraz.startsWith(x, i)) || wyraz[i];
        k.push(z); i += z.length;
      }
      pamiecKart.set(wyraz, k);
    }
    return k;
  }
  // Z ilu talii da się ułożyć wyrazy (1, 2, …; maks + 1 = potrzeba więcej niż maks).
  function ileTalii(wyrazy, maks = 2) {
    const ile = {};
    let t = 1;
    for (const w of wyrazy) for (const k of naKarty(w)) {
      ile[k] = (ile[k] || 0) + 1;
      const trzeba = Math.ceil(ile[k] / (TALIA[k] || 0.001));
      if (trzeba > t) { t = trzeba; if (t > maks) return maks + 1; }
    }
    return t;
  }
  const maDwuznak = wyrazy => wyrazy.some(w => naKarty(w).some(k => k.length > 1));
  const pasuje = (wyrazy, f) => ileTalii(wyrazy, f.talie) <= f.talie && !(f.bez && maDwuznak(wyrazy));

  // ----- przygotowanie danych -----
  const RODZ = { m: 0, "ż": 1, n: 2 };
  const idPrzym = {};                                  // forma -> forma męska (identyfikator)
  for (const [id, formy] of Object.entries(D.przym)) for (const x of formy) idPrzym[x] = id;
  const zlePary = new Set();
  for (const p of D.zlePary) { const [a, b] = p.split("-"); zlePary.add(a + "|" + b); zlePary.add(b + "|" + a); }
  const zlaPara = (a, b) => a === b || zlePary.has(idPrzym[a] + "|" + idPrzym[b]);
  const bezOdwr = new Set(D.bezOdwracania), bezPar = new Set(D.bezPar), wymagaMiejsca = new Set(D.wymagaMiejsca);
  const zleAV = new Set(D.zleAV);                      // „wesoły-płacze”
  const pasujeAV = (przym, czas) => !zleAV.has(idPrzym[przym] + "-" + czas);
  const REG = {};
  for (const [k, l] of Object.entries(D.reg)) REG[k] = new Set(l);

  const NAZWY = Object.keys(D.podmioty);
  const P = {};
  for (const n of NAZWY) {
    const x = D.podmioty[n], wykl = new Set(D.wykl[n] || []);
    const M = uniq([...(x.mg || []).flatMap(g => D.M[g]), ...(x.m || [])]).filter(f => !wykl.has(f));
    const cg = {};
    for (const g of (x.cg || [])) cg[g] = D.C[g].filter(f => !wykl.has(f));
    const C = uniq([...Object.values(cg).flat(), ...(x.c || [])]).filter(f => !wykl.has(f));
    const V = (x.v || []).map(s => {
      const [v, r] = s.split(":");
      return { v, m: r === "*" ? M : r === "-" ? [] : M.filter(f => REG[r].has(f)) };
    });
    const wgCzasownika = {};                           // „je” -> [„zupę”, „chleb”, …]
    for (const f of C) { const i = f.indexOf(" "); (wgCzasownika[f.slice(0, i)] = wgCzasownika[f.slice(0, i)] || []).push(f.slice(i + 1)); }
    P[n] = {
      n, mn: !!x.mn, r: x.r, zy: !!x.z, lu: !!x.l,
      M, Mset: new Set(M), Modwr: M.filter(f => !bezOdwr.has(f)),
      C, Cset: new Set(C), cg, dop: Object.entries(wgCzasownika).filter(e => e[1].length > 1),
      V, Vn: V.map(v => v.v).filter(v => !wymagaMiejsca.has(v)), Vset: new Set(V.map(v => v.v)),
      A: x.mn ? [] : (x.a || []).map(id => D.przym[id][RODZ[x.r]]), Aset: new Set(x.a || []),
      pary: x.p || [],
    };
  }

  // ----- wzory zdań sensownych -----
  // Wzór zwraca listę „iloczynów”: { cz: [opcje1, opcje2, …], ok? } – zdanie to po jednej opcji z każdej listy.
  const WZORY = {
    // 2–3 wyrazy
    SV:        S => S.Vn.length ? [{ cz: [[S.n], S.Vn] }] : [],                                  // kot śpi
    AS:        S => S.A.length ? [{ cz: [S.A, [S.n]] }] : [],                                    // mały kot
    TO_S:      S => [{ cz: [["to"], [S.n]] }],                                                   // to kot
    SM:        S => S.M.length ? [{ cz: [[S.n], S.M] }] : [],                                    // kot na stole
    SC:        S => S.C.length ? [{ cz: [[S.n], S.C] }] : [],                                    // mama je zupę
    S_JEST_A:  S => S.A.length ? [{ cz: [[S.n], ["jest"], S.A] }] : [],                          // kot jest mały
    ASV:       S => S.A.length && S.Vn.length ? [{ cz: [S.A, [S.n], S.Vn], ok: c => pasujeAV(c[0], c[2]) }] : [],   // mały kot śpi
    TO_JEST_S: S => S.mn ? [] : [{ cz: [["to jest"], [S.n]] }],                                  // to jest kot
    TU_JEST_S: S => S.mn ? [] : [{ cz: [["tu jest"], [S.n]] }],                                  // tu jest dom
    TO_AS:     S => S.A.length ? [{ cz: [["to"], S.A, [S.n]] }] : [],                            // to mały kot
    S_I_S:     S => S.pary.length ? [{ cz: [[S.n], ["i"], S.pary] }] : [],                       // kot i pies
    // 4–5 wyrazów
    SVM:       S => S.V.filter(v => v.m.length).map(v => ({ cz: [[S.n], [v.v], v.m] })),         // kot śpi na kanapie
    ASM:       S => S.A.length && S.M.length ? [{ cz: [S.A, [S.n], S.M] }] : [],                 // mały kot na stole
    ASC:       S => S.A.length && S.C.length ? [{ cz: [S.A, [S.n], S.C] }] : [],                 // mały kot pije mleko
    S_JEST_M:  S => !S.mn && S.M.length ? [{ cz: [[S.n], ["jest"], S.M] }] : [],                 // kot jest na stole
    M_JEST_S:  S => !S.mn && S.Modwr.length ? [{ cz: [S.Modwr, ["jest"], [S.n]] }] : [],         // na stole jest kubek
    TO_JEST_AS: S => S.A.length ? [{ cz: [["to jest"], S.A, [S.n]] }] : [],                      // to jest mały kot
    TU_JEST_AS: S => S.A.length ? [{ cz: [["tu jest"], S.A, [S.n]] }] : [],                      // tu jest duży dom
    TO_S_I_S:  S => S.pary.length ? [{ cz: [["to"], [S.n], ["i"], S.pary] }] : [],               // to mama i tata
    ASVM:      S => S.A.length ? S.V.filter(v => v.m.length).map(v => ({ cz: [S.A, [S.n], [v.v], v.m],     // mały kot śpi na kanapie
                 ok: c => pasujeAV(c[0], c[2]) })) : [],
    SCM:       S => Object.keys(S.cg).filter(g => D.gdzie[g]).map(g => ({                        // mama je zupę w kuchni
                 cz: [[S.n], S.cg[g], D.gdzie[g].filter(f => S.Mset.has(f))] })).filter(p => p.cz[1].length && p.cz[2].length),
    S_I_S_M:   S => S.pary.map(p => ({ cz: [[S.n], ["i"], [p], S.M.filter(f => P[p].Mset.has(f) && !bezPar.has(f))] }))
                 .filter(p => p.cz[3].length),                                                   // kot i pies w domu
    SC_I_O:    S => S.dop.map(([v, o]) => ({ cz: [[S.n], [v], o, ["i"], o], ok: c => c[2] !== c[4] })),   // mama je zupę i chleb
    S_JEST_A_I_A: S => S.A.length > 1 ? [{ cz: [[S.n], ["jest"], S.A, ["i"], S.A], ok: c => !zlaPara(c[2], c[4]) }] : [],
    AS_JEST_M: S => S.A.length && S.M.length ? [{ cz: [S.A, [S.n], ["jest"], S.M] }] : [],       // mały kot jest na stole
    M_JEST_AS: S => S.A.length && S.Modwr.length ? [{ cz: [S.Modwr, ["jest"], S.A, [S.n]] }] : [],   // w domu jest mały kot
  };

  // ----- zdania śmieszne -----
  const SM = D.smieszne, bezSlow = new Set(SM.bezSlow);
  const czyste = f => !f.split(" ").some(w => bezSlow.has(w));
  const SM_M = SM.miejsca, SM_M_ODWR = SM_M.filter(f => !bezOdwr.has(f));
  // Czynności „ludzkie” (dla zwierząt: „krowa czyta książkę”) i „zwierzęce” (dla ludzi: „tata znosi jajka”).
  const C_LUDZKIE = uniq([...Object.values(D.C).flat(), ...NAZWY.filter(n => P[n].lu).flatMap(n => D.podmioty[n].c || [])]).filter(czyste);
  const ludzkie = new Set(C_LUDZKIE);
  const C_INNE = uniq(NAZWY.filter(n => !P[n].lu).flatMap(n => D.podmioty[n].c || [])).filter(f => czyste(f) && !ludzkie.has(f));
  const ZYWE = NAZWY.filter(n => P[n].zy && !P[n].mn);
  const zPuli = (pula, wlasne) => { for (let i = 0; i < 8; i++) { const x = pula[los(pula.length)]; if (!wlasne.has(x)) return x; } return null; };
  const jeden = t => t[los(t.length)];
  const zywy = S => S.zy && !S.mn;
  const smC = S => zywy(S) ? zPuli(S.lu || rnd() < 0.3 ? C_INNE : C_LUDZKIE, S.Cset) : null;       // śmieszna czynność
  const smV = S => zywy(S) ? zPuli(S.lu || rnd() < 0.5 ? SM.vZwierzece : SM.vLudzkie, S.Vset) : null; // śmieszny czasownik
  const smM = S => zPuli(SM_M, S.Mset);                                                              // śmieszne miejsce
  function smA(S) {                                    // śmieszny przymiotnik w rodzaju podmiotu
    if (S.mn) return null;
    const id = zPuli(S.lu ? SM.przymLudzie : SM.przymLudzie.concat(SM.przymReszta), S.Aset);
    return id && D.przym[id][RODZ[S.r]];
  }
  const WZORY_SM = {
    // 2–3 wyrazy
    zV:    S => [S.n, smV(S)],                                                                   // krowa miauczy
    zM:    S => [S.n, smM(S)],                                                                   // krowa na szafie
    zC:    S => [S.n, smC(S)],                                                                   // ryba czyta książkę
    zA:    S => [smA(S), S.n],                                                                   // zielony kot
    zJA:   S => S.mn ? null : [S.n, "jest", smA(S)],                                             // kot jest zielony
    zAV:   S => S.Vn.length ? [smA(S), S.n, jeden(S.Vn)] : null,                                 // zielony kot śpi
    zToA:  S => ["to", smA(S), S.n],                                                             // to różowy słoń
    // 4–5 wyrazów
    zVM:   S => [S.n, smV(S), jeden(SM_M)],                                                      // krowa miauczy na szafie
    zSVM:  S => S.V.length ? [S.n, jeden(S.V).v, smM(S)] : null,                                 // kot śpi na księżycu
    zAM:   S => S.M.length ? [smA(S), S.n, jeden(S.M)] : null,                                   // zielony kot na szafie
    zAM2:  S => S.A.length ? [jeden(S.A), S.n, smM(S)] : null,                                   // mały kot na księżycu
    zAC:   S => zywy(S) ? [smA(S), S.n, S.C.length && rnd() < 0.5 ? jeden(S.C) : smC(S)] : null,  // różowy tata czyta gazetę
    zMJ:   S => S.mn ? null : [zPuli(SM_M_ODWR, S.Mset), "jest", S.n],                           // na szafie jest krowa
    zToJA: S => S.mn ? null : ["to jest", smA(S), S.n],                                          // to jest różowy słoń
    zPara: S => { const T = P[jeden(ZYWE)];                                                      // krowa i tata na szafie
                  return zywy(S) && T !== S && !S.pary.includes(T.n) ? [S.n, "i", T.n, jeden(SM_M)] : null; },
    zJAA:  S => { const a = smA(S), b = smA(S);                                                  // kot jest zielony i wielki
                  return a && b && !zlaPara(a, b) ? [S.n, "jest", a, "i", b] : null; },
    zCM:   S => [S.n, smC(S), jeden(SM_M)],                                                      // ryba je lody na szafie
  };

  // ----- tryby: zdania krótkie (2–3 wyrazy) i długie (4–5 wyrazów); liczby to wagi losowania wzoru -----
  const TRYBY = {
    k: { min: 2, max: 3,
         wzory: { SV: 3, AS: 2, TO_S: 0.7, SM: 3, SC: 3, S_JEST_A: 2, ASV: 2, TO_JEST_S: 0.7, TU_JEST_S: 0.7, TO_AS: 0.7, S_I_S: 1.5 },
         smieszne: { zV: 3, zM: 3, zC: 3, zA: 2, zJA: 1, zAV: 1, zToA: 0.5 } },
    d: { min: 4, max: 5,
         wzory: { SVM: 3, ASM: 2, ASC: 2, S_JEST_M: 1.5, M_JEST_S: 1.5, TO_JEST_AS: 0.8, TU_JEST_AS: 0.8, TO_S_I_S: 0.6, ASV: 0.4,
                  ASVM: 2, SCM: 2, S_I_S_M: 1.5, SC_I_O: 1.5, S_JEST_A_I_A: 1, AS_JEST_M: 1, M_JEST_AS: 1 },
         smieszne: { zVM: 3, zSVM: 2, zAM: 1.5, zAM2: 1.5, zAC: 1.5, zMJ: 1.5, zToJA: 0.5, zPara: 1.5, zJAA: 0.7, zCM: 2 } },
  };

  // ----- losowanie -----
  function wazony(wagi) {
    const klucze = Object.keys(wagi);
    let r = rnd() * klucze.reduce((s, k) => s + wagi[k], 0);
    for (const k of klucze) { r -= wagi[k]; if (r < 0) return k; }
    return klucze[klucze.length - 1];
  }
  function tasuj(t) {
    for (let i = t.length - 1; i > 0; i--) { const j = los(i + 1); [t[i], t[j]] = [t[j], t[i]]; }
    return t;
  }
  // Podmioty losujemy z „worka” – każdy tak samo często, bez powtórzeń, dopóki worek się nie opróżni.
  const worki = {};
  function zWorka(klucz, zrodlo) {
    let w = worki[klucz];
    if (!w || !w.length) w = worki[klucz] = tasuj(zrodlo.slice());
    return P[w.pop()];
  }
  const pamiecWzorow = new Map();
  function iloczyny(wz, S) {
    const k = wz + "|" + S.n;
    let p = pamiecWzorow.get(k);
    if (!p) pamiecWzorow.set(k, p = WZORY[wz](S));
    return p;
  }
  const wZakresie = (w, T) => w.length >= T.min && w.length <= T.max;

  function losujSensowne(tryb, f) {
    const T = TRYBY[tryb];
    for (let i = 0; i < 500; i++) {
      const wz = wazony(T.wzory), S = zWorka("s" + tryb, NAZWY), il = iloczyny(wz, S);
      if (!il.length) continue;
      for (let j = 0; j < 12; j++) {
        const p = jeden(il), cz = p.cz.map(jeden);
        if (p.ok && !p.ok(cz)) continue;
        const w = cz.join(" ").split(" ");
        if (wZakresie(w, T) && pasuje(w, f)) return { w, wzor: wz, smieszne: false };
      }
    }
    return null;
  }
  function losujSmieszne(tryb, f) {
    const T = TRYBY[tryb];
    for (let i = 0; i < 1500; i++) {
      const wz = wazony(T.smieszne);
      const S = rnd() < 0.7 ? zWorka("z" + tryb, ZYWE) : zWorka("w" + tryb, NAZWY);   // częściej o ludziach i zwierzętach
      const cz = WZORY_SM[wz](S);
      if (!cz || cz.some(x => !x)) continue;
      const w = cz.join(" ").split(" ");
      if (wZakresie(w, T) && pasuje(w, f)) return { w, wzor: wz, smieszne: true };
    }
    return null;
  }
  // tryb: "k" (krótkie) albo "d" (długie); opcje: { talie: 1|2, bezDwuznakow: bool, smieszne: 0..1 }
  function losuj(tryb, opcje = {}) {
    const f = { talie: opcje.talie || 1, bez: !!opcje.bezDwuznakow };
    const udzial = opcje.smieszne === undefined ? 0.25 : opcje.smieszne;
    const r = rnd() < udzial ? (losujSmieszne(tryb, f) || losujSensowne(tryb, f))
                             : (losujSensowne(tryb, f) || (udzial > 0 ? losujSmieszne(tryb, f) : null));
    return r && { s: r.w.join(" "), w: r.w, wzor: r.wzor, smieszne: r.smieszne };
  }

  // Wylicza wszystkie zdania sensowne danego trybu: wywoluje(wyrazy, wzór).
  function wylicz(tryb, wywolaj) {
    const T = TRYBY[tryb];
    for (const wz of Object.keys(T.wzory)) for (const n of NAZWY) for (const p of WZORY[wz](P[n])) {
      const cz = new Array(p.cz.length);
      (function dalej(i) {
        if (i === cz.length) {
          if (p.ok && !p.ok(cz)) return;
          const w = cz.join(" ").split(" ");
          if (wZakresie(w, T)) wywolaj(w, wz);
          return;
        }
        for (const x of p.cz[i]) { cz[i] = x; dalej(i + 1); }
      })(0);
    }
  }

  return { naKarty, ileTalii, maDwuznak, losuj, losujSensowne, losujSmieszne, wylicz, TRYBY, podmioty: P };
}

if (typeof module !== "undefined" && module.exports) module.exports = { utworz };
else root.GeneratorZdan = { utworz };
})(typeof window !== "undefined" ? window : this);
