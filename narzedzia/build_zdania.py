"""Buduje zdania.js: proste zdania z trzech wyrazów do nauki czytania.

Zdania powstają z połączenia PODMIOTU (forma podstawowa, np. „kot”) z WYRAŻENIEM
z dwóch wyrazów – miejscem („na stole”, „pod kocem”) albo czynnością („pije mleko”).
Każdy podmiot ma przypisane tylko te grupy wyrażeń, które do niego pasują
(kot może być „na szafie”, ale krowa już nie), więc zdania mają sens.
Zdania, których nie da się ułożyć z TALIE zestawów kart (build_words.py, domyślnie 2), są pomijane.

Edycja: dopisz podmiot do istniejącej grupy albo nowe wyrażenie do grupy w słownikach
poniżej. Grupę wyrażeń wstawia się do listy pisząc @nazwa. Elementy oddziela się znakiem |.

Użycie:
  python3 narzedzia/build_zdania.py zdania.js [--sjp slowa-sjp.txt] [--lista narzedzia/zdania-lista.txt]
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_words import TALIE, na_karty, miesci_sie, klucz_sortowania  # noqa: E402

# ---------------------------------------------------------------------------------------------
# MIEJSCA – grupy wyrażeń „przyimek + rzeczownik”
# ---------------------------------------------------------------------------------------------
M = {
    "siedzi": "na krześle|na kanapie|na fotelu|na łóżku|w łóżku|na ławce|na kocu|na dywanie|na podłodze|"
              "na schodach|na balkonie|na tarasie|przy stole|przy biurku|przy oknie|przy kominku",
    "pokoje": "w domu|w pokoju|w kuchni|w łazience|w sypialni|w salonie|w przedpokoju|na strychu|w piwnicy|w garażu",
    "ogród_ludzie": "w ogrodzie|na podwórku|na trawie|na trawniku|pod drzewem|w sadzie|pod parasolem|za domem|przed domem",
    "miasto": "w mieście|na ulicy|w sklepie|w parku|w kinie|w teatrze|w muzeum|w zoo|na basenie|na placu|na rynku|"
              "w autobusie|w tramwaju|w pociągu|w samochodzie|w aucie|na dworcu|na przystanku|na moście|na poczcie|"
              "w bibliotece|w restauracji|na lotnisku|na stacji|w kawiarni|w aptece|w banku|na targu|w cukierni|"
              "w piekarni|w księgarni|u lekarza|u dentysty|u fryzjera|na koncercie|na weselu",
    "wycieczka": "w górach|na wsi|na farmie|na plaży|na spacerze|na wycieczce|na wakacjach|na łące|w lesie|"
                 "nad morzem|nad jeziorem|nad rzeką|na polanie|na rowerze|na koniu|na statku|na łódce|w namiocie|"
                 "na kempingu|przy ognisku|w hotelu",
    "zima": "na śniegu|na sankach|na nartach|na łyżwach|na lodowisku|na górce",
    "kąpiel": "w wodzie|w morzu|w jeziorze|w rzece|w basenie|w wannie|pod prysznicem",
    "rodzina": "u babci|u dziadka|u cioci|u wujka|u sąsiada|u sąsiadki",
    "dzieci": "w przedszkolu|w szkole|na boisku|w piaskownicy|na huśtawce|na zjeżdżalni|na karuzeli|w klasie|"
              "pod stołem|pod kocem|pod kołdrą|w szafie|na drzewie|w kałuży|w krzakach|na hulajnodze|na kucyku|"
              "na urodzinach|na balu|w lunaparku|w cyrku|na trampolinie|na rolkach|na deskorolce|za drzewem|"
              "za kanapą|za drzwiami|za szafą",
    "niemowlę": "w łóżeczku|w wózku|w kołysce|na kocu|w foteliku|w kąpieli|u mamy|w pokoju|w sypialni|na spacerze",
    "meble_na": "na stole|na krześle|na kanapie|na fotelu|na łóżku|na półce|na szafie|na parapecie|na biurku|"
                "na stoliku|na komodzie|na dywanie|na podłodze|na schodach|na poduszce",
    "meble_pod": "pod stołem|pod łóżkiem|pod krzesłem|pod kanapą|pod kocem|pod kołdrą|pod biurkiem|pod szafą|"
                 "pod fotelem|pod poduszką|pod stolikiem|za szafą|za kanapą",
    "schowki": "w szafie|w szufladzie|w pudełku|w koszu|w koszyku|w plecaku|w torbie|w walizce|w skrzyni|w kartonie",
    "las": "w lesie|na łące|na polu|na polanie|pod drzewem|pod krzakiem|w krzakach|w trawie",
    "niebo": "na niebie|nad domem|nad lasem|nad morzem|nad łąką|nad miastem|nad górami",
    "farma": "na farmie|na łące|na pastwisku|na polu|na podwórku|w zagrodzie|w stodole|na wsi",
    "bajka": "w zamku|na zamku|w pałacu|na wieży|w wieży|w karecie|na balu|w ogrodzie|w bajce",
    "kosmos": "w kosmosie|na księżycu|w rakiecie|na planecie",
    "naczynia": "na stole|w szafce|w zlewie|na półce|w kuchni|w zmywarce|na tacy",
    "sztućce": "na stole|w szufladzie|w zlewie|w zmywarce|na talerzu|w misce|w kuchni|na tacy|na serwetce",
    "pieczywo": "na stole|na talerzu|w koszyku|w piekarni|w torbie|w kuchni|na tacy|w sklepie",
    "owoce": "na stole|na talerzu|w koszyku|w misce|w lodówce|w plecaku|w torbie|w sklepie|na straganie|na targu",
    "owoce_drzewo": "na drzewie|na gałęzi|w ogrodzie|w sadzie|pod drzewem|na trawie",
    "jagody": "w lesie|w misce|w koszyku|na krzaku|w ogrodzie|na talerzu|w jogurcie|na torcie",
    "lodówka": "w lodówce|na stole|na talerzu|w sklepie",
    "garnek": "w garnku|na talerzu|w misce|na stole|w kuchni|na kuchence",
    "napoje": "w kubku|w szklance|w butelce|w dzbanku|w lodówce|na stole|w kubeczku",
    "warzywa": "w ogrodzie|w koszyku|na talerzu|w lodówce|w misce|w sklepie|w garnku|na straganie|na targu",
    "ubrania": "w szafie|na wieszaku|w szufladzie|na krześle|na łóżku|na podłodze|w walizce|w przedpokoju|"
               "na półce|w plecaku|w praniu|w pralce|w sklepie",
    "obuwie": "w przedpokoju|pod łóżkiem|w szafie|na półce|w szafce|w pudełku|na podłodze|pod stołem|w walizce|"
              "w sklepie|przy drzwiach",
    "szkolne": "na biurku|na stole|w plecaku|w torbie|na półce|w szufladzie|na podłodze|w szkole|w klasie|na ławce",
    "piórnik": "w piórniku",
    "ulica": "na ulicy|na drodze|w garażu|na parkingu|na moście|w mieście|na autostradzie|na stacji|w myjni|"
             "pod domem|przed domem|w tunelu|na skrzyżowaniu",
    "łodzie": "na morzu|na jeziorze|na rzece|na wodzie|w porcie|na stawie|na brzegu|na plaży|w zatoce|na falach",
    "powietrze": "na niebie|w chmurach|nad domem|nad lasem|nad morzem|nad miastem|nad łąką|nad górami",
    "kwiaty": "w ogrodzie|na łące|w wazonie|w doniczce|na parapecie|na balkonie|w bukiecie",
    "drzewa": "w ogrodzie|w lesie|w parku|na łące|na polu|na podwórku|na górce|przy drodze|na wzgórzu",
    "zabawki": "w pokoju|w łóżku|w łóżeczku|w wózku|na kocu|w ogrodzie|na trawie|w piaskownicy|na huśtawce|w wannie",
    "plac_zabaw": "w ogrodzie|w parku|na podwórku|na placu",
    "sprzęt": "w garażu|w piwnicy|na podwórku|w parku|na ścieżce|na chodniku|w przedpokoju|na balkonie|pod domem",
    "owady": "na kwiatku|na liściu|w trawie|na łące|w ogrodzie",
    "ptaki": "na drzewie|na gałęzi|na dachu|na płocie|w ogrodzie|na parapecie|na balkonie",
    "ryby": "w rzece|w jeziorze|w stawie|w wodzie|w sieci",
    "morze": "w morzu|w oceanie|w wodzie|pod wodą",
    "sawanna": "w zoo|na sawannie",
    "dżungla": "w zoo|w dżungli|na drzewie|na gałęzi",
}

# ---------------------------------------------------------------------------------------------
# CZYNNOŚCI – grupy wyrażeń „czasownik + dopełnienie”
# ---------------------------------------------------------------------------------------------
C = {
    "je": "je zupę|je chleb|je bułkę|je jabłko|je gruszkę|je śliwkę|je ser|je jajko|je ciastko|je tort|je lody|"
          "je kanapkę|je pizzę|je kaszę|je ryż|je makaron|je sałatkę|je marchewkę|je ogórek|je pomidor|je rybę|"
          "je kotlet|je naleśnik|je pierogi|je rosół|je jogurt|je owsiankę|je budyń|je kisiel|je galaretkę|"
          "je czekoladę|je jagody|je truskawki|je maliny|je czereśnie|je winogrona|je frytki|je placki|je sernik|"
          "je szarlotkę|je obiad|je śniadanie|je kolację|je podwieczorek|je drożdżówkę|je mandarynkę|"
          "je pomarańczę|je jajecznicę|je omlet|je barszcz|je bigos|je gulasz|je popcorn|je żelki|je chrupki|"
          "je paluszki|je płatki|je racuchy|je kluski|je kopytka|je pyzy|je gołąbki|je banana|je arbuza",
    "pije": "pije mleko|pije wodę|pije sok|pije kakao|pije kompot|pije lemoniadę|pije herbatę|pije oranżadę|"
            "pije kefir|pije koktajl",
    "czyta": "czyta książkę|czyta bajkę|czyta list|czyta wierszyk|czyta książeczkę|czyta komiks|czyta mapę|"
             "czyta kartkę|czyta zagadkę",
    "rysuje": "rysuje dom|rysuje kota|rysuje psa|rysuje słońce|rysuje drzewo|rysuje kwiatek|rysuje auto|"
              "rysuje rybę|rysuje konia|rysuje smoka|rysuje zamek|rysuje statek|rysuje tęczę|rysuje chmurę|"
              "rysuje gwiazdę|rysuje serce|rysuje mamę|rysuje tatę|rysuje misia|rysuje motyla|rysuje biedronkę|"
              "rysuje bałwana|rysuje choinkę|rysuje rakietę|rysuje pociąg|rysuje samolot|rysuje kółko|"
              "rysuje literę|rysuje mapę|rysuje rodzinę|rysuje babcię|rysuje dziadka|rysuje dinozaura|"
              "rysuje księżyc|rysuje słonia|rysuje żyrafę|rysuje królewnę|rysuje rycerza|rysuje pirata|"
              "rysuje robota|rysuje morze|rysuje góry|rysuje las|rysuje ptaka|rysuje jeża|rysuje wiewiórkę|"
              "rysuje lisa|rysuje zająca|rysuje kreskę|rysuje kwadrat|rysuje trójkąt|maluje obraz|"
              "maluje pisankę|maluje kwiatek|maluje tęczę|maluje domek",
    "porządki": "sprząta pokój|sprząta kuchnię|sprząta dom|sprząta zabawki|myje okno|myje auto|myje naczynia|"
                "myje talerz|myje kubek|myje ręce|myje zęby|myje podłogę|myje wannę|myje psa|myje głowę|"
                "myje twarz|myje uszy|wyciera stół|wyciera talerz|wyciera ręce|wyciera nos|zamiata podłogę|"
                "zamiata podwórko|wiesza pranie|ściele łóżko|zmywa naczynia|odkurza dywan|odkurza pokój|"
                "podlewa kwiaty|karmi rybki",
    "kuchnia": "gotuje zupę|gotuje obiad|gotuje makaron|gotuje jajko|gotuje kaszę|gotuje rosół|gotuje kompot|"
               "gotuje barszcz|gotuje pierogi|piecze ciasto|piecze chleb|piecze tort|piecze ciasteczka|"
               "piecze pizzę|piecze sernik|piecze szarlotkę|piecze pierniki|piecze babeczki|piecze rogaliki|"
               "kroi chleb|kroi ser|kroi tort|kroi ogórek|kroi pomidor|kroi jabłko|kroi ciasto|kroi cebulę|"
               "kroi marchewkę|kroi arbuz|smaży jajecznicę|smaży naleśniki|smaży kotlet|smaży placki|"
               "smaży racuchy|robi kanapkę|robi herbatę|robi obiad|robi kakao|robi sałatkę|robi kanapki|"
               "robi śniadanie|robi kolację|robi budyń|robi galaretkę|nakrywa stół|nalewa zupę|nalewa sok|"
               "nalewa mleko|nalewa herbatę|miesza zupę|miesza ciasto|lepi pierogi",
    "zabawa": "buduje zamek|buduje wieżę|buduje domek|buduje most|buduje namiot|lepi bałwana|lepi babkę|"
              "układa klocki|układa puzzle|rzuca piłkę|kopie piłkę|łapie piłkę|odbija piłkę|puszcza latawiec|"
              "puszcza bańki|dmucha balon|dmucha bańki|dmucha świeczki|ciągnie sanki|ciągnie wózek|pcha wózek|"
              "huśta lalkę|ubiera lalkę|czesze lalkę|karmi lalkę|przytula misia|przytula lalkę|przytula kota|"
              "przytula mamę|przytula tatę|przytula babcię|przytula pieska|przytula kotka|łapie motyla|"
              "łapie bańki|goni kota|goni psa|goni piłkę|goni gołębie|goni motyla|goni brata|goni siostrę|"
              "liże lody|liże lizaka|ogląda bajkę|ogląda gwiazdy|ogląda książeczkę|liczy owce|liczy gwiazdy|"
              "liczy palce|liczy kredki|robi babkę|ma urodziny",
    "zwierzaki": "głaszcze kota|głaszcze psa|głaszcze konia|głaszcze królika|głaszcze kotka|głaszcze pieska|"
                 "karmi kota|karmi psa|karmi kury|karmi kaczki|karmi konia|karmi królika|karmi ptaki|"
                 "karmi chomika|karmi łabędzie",
    "zbiera": "zbiera grzyby|zbiera kasztany|zbiera jagody|zbiera maliny|zbiera kwiaty|zbiera liście|"
              "zbiera muszelki|zbiera kamyki|zbiera zabawki|zbiera truskawki|zbiera szyszki|zbiera żołędzie|"
              "zbiera jabłka|szuka kota|szuka piłki|szuka mamy|szuka taty|szuka skarbu|szuka misia|szuka klucza|"
              "szuka kapci|szuka jajek|szuka grzybów|łowi ryby",
    "codzienne": "śpiewa piosenkę|śpiewa kołysankę|śpiewa kolędę|ogląda film|ogląda zdjęcia|słucha bajki|"
                 "słucha muzyki|słucha mamy|słucha taty|słucha radia|słucha piosenki|otwiera prezent|"
                 "otwiera okno|otwiera drzwi|otwiera pudełko|otwiera książkę|otwiera lodówkę|otwiera parasol|"
                 "zamyka okno|zamyka drzwi|zamyka szafę|zamyka książkę|zakłada czapkę|zakłada buty|"
                 "zakłada kurtkę|zakłada kapcie|zakłada szalik|zakłada rękawiczki|zakłada piżamę|"
                 "zakłada kalosze|zdejmuje buty|zdejmuje czapkę|zdejmuje kurtkę|wącha kwiatek|wącha różę|"
                 "wącha kwiaty|niesie torbę|niesie plecak|niesie koszyk|niesie prezent|niesie wiadro|"
                 "niesie kwiaty|niesie tort|niesie talerz|nosi okulary|nosi kapelusz|nosi czapkę|pisze list|"
                 "pisze literę|pisze kartkę|robi zdjęcie",
    "dorośli": "prowadzi auto|prowadzi samochód|naprawia auto|naprawia rower|naprawia kran|naprawia zegar|"
               "naprawia dach|naprawia zabawkę|kosi trawę|sadzi drzewo|sadzi kwiaty|sadzi ziemniaki|sadzi róże|"
               "podlewa ogród|podlewa trawnik|rąbie drewno|grabi liście|kupuje chleb|kupuje mleko|kupuje lody|"
               "kupuje buty|kupuje prezent|kupuje kwiaty|kupuje bilet|kupuje owoce|kupuje warzywa|"
               "kupuje choinkę|szyje sukienkę|szyje spodnie|czyta gazetę|pije kawę|ubiera choinkę|wiesza obraz|"
               "niesie dziecko|pcha wózek|karmi dziecko|kąpie dziecko|kąpie psa|ubiera dziecko|budzi dziecko|"
               "usypia dziecko|prasuje koszulę|prasuje spodnie|maluje płot|maluje ścianę|maluje pokój|"
               "maluje paznokcie|liczy pieniądze",
    "ma_dzieci": "ma piłkę|ma misia|ma lalkę|ma balon|ma rower|ma hulajnogę|ma latawiec|ma klocki|ma kota|"
                 "ma psa|ma chomika|ma królika|ma rybkę|ma papugę|ma żółwia|ma kotka|ma pieska|ma czapkę|"
                 "ma kurtkę|ma plecak|ma kredki|ma książkę|ma lody|ma prezent|ma tort|ma sanki|ma narty|"
                 "ma łyżwy|ma rolki|ma okulary|ma parasol|ma gitarę|ma bębenek|ma trąbkę|ma piórnik|ma zeszyt|"
                 "ma koronę|ma różdżkę|ma robota|ma pluszaka|ma samochodzik|ma pociąg|ma kolejkę|ma skakankę|"
                 "ma puzzle|ma bańki|ma jabłko|ma kanapkę|ma brata|ma siostrę|ma katar|ma piegi|ma warkocze",
    "ma_dorośli": "ma parasol|ma okulary|ma auto|ma rower|ma telefon|ma klucz|ma książkę|ma kapelusz|ma kota|"
                  "ma psa|ma ogród|ma gitarę|ma torbę|ma zegarek|ma laptop|ma kurtkę|ma szalik|ma koszyk|"
                  "ma prezent|ma tort|ma urodziny|ma katar",
    "ma_brodę": "ma brodę|ma wąsy",
    "lubi": "lubi lody|lubi czekoladę|lubi zupę|lubi pizzę|lubi naleśniki|lubi jabłka|lubi truskawki|"
            "lubi kakao|lubi koty|lubi psy|lubi konie|lubi bajki|lubi książki|lubi śnieg|lubi deszcz|lubi lato|"
            "lubi zimę|lubi wiosnę|lubi jesień|lubi morze|lubi góry|lubi las|lubi muzykę|lubi taniec|"
            "lubi kąpiel|lubi spacery|lubi zwierzęta|lubi kwiaty|lubi słońce|lubi kanapki|lubi makaron|"
            "lubi pierogi|lubi placki|lubi ciasto|lubi sernik|lubi szarlotkę|lubi warzywa|lubi owoce|"
            "lubi marchewkę|lubi ogórki|lubi pomidory|lubi banany|lubi arbuzy|lubi cukierki|lubi żelki|"
            "lubi chrupki|lubi popcorn|lubi mleko|lubi wakacje|lubi święta|lubi urodziny|lubi prezenty|"
            "lubi zagadki|lubi wierszyki|lubi piosenki|lubi zabawki|lubi klocki|lubi puzzle|lubi basen|"
            "lubi plażę|lubi dinozaury|lubi smoki|lubi rakiety|lubi pociągi|lubi samochody|lubi motyle|"
            "lubi biedronki|lubi ptaki",
    "lubi_dzieci": "lubi przedszkole|lubi szkołę",
    "widzi": "widzi kota|widzi psa|widzi ptaka|widzi motyla|widzi tęczę|widzi gwiazdę|widzi księżyc|"
             "widzi samolot|widzi statek|widzi pociąg|widzi wiewiórkę|widzi bociana|widzi zająca|widzi sarnę|"
             "widzi rybę|widzi żabę|widzi ślimaka|widzi biedronkę|widzi chmurę|widzi słońce|widzi morze|"
             "widzi góry|widzi las|widzi tramwaj|widzi karetkę|widzi koparkę|widzi traktor|widzi jeża|"
             "widzi lisa|widzi konia|widzi krowę|widzi kaczkę|widzi łabędzia|widzi mrówkę|widzi pająka|"
             "widzi rakietę|widzi balon|widzi latawiec|widzi bałwana|widzi śnieg|widzi kałużę|widzi smoka|"
             "widzi ducha",
}

# ---------------------------------------------------------------------------------------------
# PODMIOTY – (podmioty oddzielone spacją, wyrażenia/grupy oddzielone |)
# ---------------------------------------------------------------------------------------------
P = [
    # --- ludzie ---
    ("mama tata babcia dziadek ciocia wujek pani pan sąsiad sąsiadka",
     "@siedzi|@pokoje|@ogród_ludzie|@miasto|@wycieczka|@zima|@kąpiel|@rodzina"),
    ("mama tata babcia dziadek ciocia wujek",
     "@je|@pije|@czyta|@porządki|@kuchnia|@codzienne|@dorośli|@ma_dorośli|@lubi|@widzi|@zwierzaki|@zbiera"),
    ("tata dziadek wujek", "@ma_brodę"),
    ("dziecko chłopiec dziewczynka brat siostra braciszek siostrzyczka maluch synek córeczka przedszkolak",
     "@siedzi|@pokoje|@ogród_ludzie|@miasto|@wycieczka|@zima|@kąpiel|@rodzina|@dzieci"),
    ("dziecko chłopiec dziewczynka brat siostra synek córeczka",
     "@je|@pije|@czyta|@rysuje|@zabawa|@zwierzaki|@zbiera|@codzienne|@ma_dzieci|@lubi|@lubi_dzieci|@widzi|"
     "myje ręce|myje zęby|sprząta pokój|sprząta zabawki|wyciera nos|podlewa kwiaty|karmi rybki|ściele łóżko"),
    ("uczeń uczennica pierwszak",
     "w szkole|w klasie|na boisku|w bibliotece|na lekcji|w autobusie|przy biurku|na wycieczce|w stołówce|"
     "w szatni|przy tablicy|czyta książkę|pisze literę|rysuje mapę|ma plecak|ma piórnik|ma zeszyt|ma kredki|"
     "liczy kredki|niesie plecak|czyta wierszyk"),
    ("niemowlę bobas dzidziuś maluszek", "@niemowlę|ma grzechotkę|pije mleko|ma smoczek|ma katar|ma ząbek"),
    # --- zawody ---
    ("lekarz lekarka", "w szpitalu|w przychodni|w karetce|przy łóżku|bada dziecko|leczy dzieci|ma słuchawki|"
                       "ma stetoskop|daje lekarstwo|daje zastrzyk|ogląda gardło"),
    ("pielęgniarka", "w szpitalu|w przychodni|w karetce|przy łóżku|daje zastrzyk|daje lekarstwo"),
    ("weterynarz", "w zoo|na farmie|w stajni|w oborze|w schronisku|w przychodni|leczy psa|leczy kota|bada konia|"
                   "bada krowę|leczy konia"),
    ("dentysta", "w przychodni|leczy zęby|leczy ząb|ogląda zęby|bada zęby"),
    ("strażak", "na dachu|na drabinie|w remizie|w lesie|na ulicy|na wieży|w budynku|przy pożarze|gasi ogień|"
                "gasi pożar|ratuje kota|ma hełm|ma drabinę"),
    ("policjant policjantka", "na ulicy|w radiowozie|na drodze|w parku|na moście|na skrzyżowaniu|na rowerze|"
                              "na koniu|w mieście|na rynku|łapie złodzieja|goni złodzieja|ma radiowóz|ma czapkę|"
                              "ma gwizdek|pomaga dzieciom"),
    ("kucharz kucharka", "w kuchni|w restauracji|w stołówce|przy kuchence|w kawiarni|@kuchnia"),
    ("piekarz", "w piekarni|w kuchni|przy piecu|piecze chleb|piecze bułki|piecze rogale|piecze ciasto|"
                "piecze pączki"),
    ("pilot", "w samolocie|na lotnisku|w helikopterze|w chmurach|w kabinie|nad morzem|nad miastem|"
              "prowadzi samolot|leci samolotem|ma czapkę"),
    ("rolnik", "na polu|na farmie|w stodole|na traktorze|w oborze|w stajni|na łące|w sadzie|na wsi|w kurniku|"
               "w zagrodzie|kosi trawę|sieje zboże|zbiera ziemniaki|ma traktor|ma krowę|doi krowę|karmi kury|"
               "orze pole|karmi świnie|zbiera zboże|ma konia|ma kozę|sadzi ziemniaki|zbiera jabłka|ma farmę|"
               "karmi krowy|zbiera siano"),
    ("nauczyciel nauczycielka", "w szkole|w klasie|w przedszkolu|na boisku|w bibliotece|przy tablicy|"
                                "przy biurku|na wycieczce|na lekcji|czyta bajkę|czyta książkę|uczy dzieci|"
                                "ma kredę|sprawdza zeszyty|pisze literę|ma okulary|czyta wierszyk|ma globus|ma mapę"),
    ("listonosz", "na poczcie|na rowerze|na ulicy|w mieście|na wsi|przy skrzynce|pod domem|niesie list|"
                  "niesie paczkę|ma torbę|przynosi list|przynosi paczkę|roznosi listy|ma rower|przynosi gazetę"),
    ("marynarz", "na statku|w porcie|na morzu|na łodzi|na łódce|na żaglówce|w kajucie"),
    ("kierowca", "w autobusie|w samochodzie|w aucie|na drodze|w ciężarówce|w taksówce|w tramwaju|na parkingu|"
                 "na stacji|w garażu|prowadzi autobus|prowadzi ciężarówkę|prowadzi auto|prowadzi tramwaj|"
                 "prowadzi taksówkę|prowadzi karetkę"),
    ("taksówkarz", "w taksówce|na ulicy|na lotnisku|na dworcu|prowadzi taksówkę"),
    ("sprzedawca", "w sklepie|na targu|na rynku|w kiosku|w piekarni|na straganie|w księgarni|w cukierni|"
                   "sprzedaje chleb|sprzedaje lody|sprzedaje owoce|sprzedaje kwiaty|sprzedaje bilety|"
                   "liczy pieniądze|sprzedaje warzywa|sprzedaje ryby|sprzedaje zabawki|sprzedaje buty|"
                   "sprzedaje gazety|sprzedaje balony"),
    ("ogrodnik", "w ogrodzie|w szklarni|na trawniku|w sadzie|w parku|pod drzewem|podlewa kwiaty|kosi trawę|"
                 "sadzi drzewo|sadzi róże|grabi liście|sadzi kwiaty|podlewa ogród|przycina róże|ma konewkę|"
                 "ma łopatę"),
    ("rybak wędkarz", "na łodzi|na łódce|na jeziorze|na rzece|nad rzeką|nad jeziorem|nad morzem|nad stawem|"
                      "na molo|na brzegu|łowi ryby|łowi rybę|ma wędkę|ma sieć|ma łódkę|łowi karpia|"
                      "łowi szczupaka|łowi pstrąga"),
    ("kosmonauta astronauta", "@kosmos|w skafandrze|ma skafander|ma hełm|widzi gwiazdy|widzi ziemię|"
                              "leci rakietą|widzi księżyc|ma rakietę"),
    ("pirat", "na statku|na wyspie|w porcie|na morzu|na plaży|w jaskini|na łodzi|w kajucie|na maszcie|"
              "ma skarb|szuka skarbu|ma mapę|ma statek|ma papugę|ma lunetę|kopie dół|ma szablę|ma kapelusz|"
              "ma brodę|ma opaskę|chowa skarb|zakopuje skarb"),
    ("rycerz", "w zamku|na koniu|na wieży|w lesie|na moście|w zbroi|w pałacu|ma miecz|ma tarczę|ma konia|"
               "ma hełm|ratuje królewnę|ratuje księżniczkę|pokonuje smoka|nosi zbroję|ma zbroję"),
    ("król królowa", "w zamku|na zamku|w pałacu|na wieży|w karecie|na balu|w ogrodzie|w bajce|na tronie|"
                     "w koronie|ma koronę|nosi koronę|ma zamek|ma berło"),
    ("król", "na koniu|ma brodę"),
    ("królewna księżniczka", "@bajka|na tronie|na koniu|w koronie|ma koronę|nosi koronę|ma suknię|nosi suknię|"
                             "całuje żabę|czesze włosy|ma pantofelek|gubi pantofelek"),
    ("książę królewicz", "@bajka|na koniu|ratuje królewnę|ma konia|ma miecz|szuka królewny|ma koronę"),
    ("czarownica wiedźma czarodziej czarodziejka",
     "w lesie|w chatce|na miotle|w wieży|w zamku|w jaskini|na strychu|w kapeluszu|w bajce|ma różdżkę|"
     "ma kapelusz|warzy miksturę|warzy eliksir|ma kocioł"),
    ("czarownica wiedźma", "ma miotłę|ma kota"),
    ("czarodziej magik iluzjonista", "ma pelerynę|wyciąga królika"),
    ("magik iluzjonista", "w cyrku|na arenie|w teatrze|na urodzinach|ma różdżkę|ma kapelusz"),
    ("wróżka", "w lesie|na kwiatku|na łące|w ogrodzie|w zamku|na tęczy|w bajce|ma różdżkę|ma skrzydła|"
               "spełnia życzenia|ma koronę"),
    ("krasnal krasnoludek skrzat", "w lesie|pod grzybem|w ogrodzie|pod liściem|na pniu|w mchu|w norce|w chatce|"
                                   "pod drzewem|w bajce|ma czapkę|niesie latarkę|ma brodę|ma kilof|ma latarkę"),
    ("smok", "w jaskini|w zamku|na wieży|na niebie|w górach|nad lasem|nad zamkiem|w bajce|nad górami|"
             "zieje ogniem|pilnuje skarbu|ma skrzydła|porywa królewnę|lubi złoto|ma ogon|pilnuje zamku|"
             "pilnuje królewny"),
    ("duch", "w zamku|na strychu|w piwnicy|w szafie|pod łóżkiem|w wieży|w bajce|w lesie"),
    ("olbrzym wielkolud", "w górach|w lesie|w zamku|na górze|w bajce|w jaskini"),
    ("klaun pajac", "w cyrku|na arenie|na balu|na urodzinach|ma perukę|ma balony|rozśmiesza dzieci|ma kapelusz"),
    ("tancerz tancerka baletnica balerina", "w teatrze|na balu|na weselu"),
    ("aktor aktorka", "w teatrze|w filmie|w bajce"),
    ("muzyk", "w orkiestrze|w teatrze|w parku|na weselu|na balu|na koncercie|ma gitarę|ma skrzypce|ma trąbkę|"
              "ma bęben|ma flet|ma akordeon|ma nuty"),
    ("piłkarz", "na boisku|na stadionie|na meczu|kopie piłkę|ma piłkę"),
    ("bramkarz", "w bramce|na boisku|na stadionie|na meczu|łapie piłkę"),
    ("kowboj", "na koniu|na ranczu|na prerii|w kapeluszu|na pustyni|przy ognisku|ma konia|ma kapelusz|ma lasso"),
    ("mechanik", "w garażu|w warsztacie|pod autem|pod samochodem|przy aucie|naprawia auto|naprawia samochód|"
                 "naprawia rower|naprawia silnik|naprawia oponę|ma klucz|naprawia motor|naprawia ciężarówkę"),
    ("hydraulik", "w łazience|w kuchni|w piwnicy|pod zlewem|przy wannie|naprawia kran|naprawia rurę|"
                  "naprawia pralkę|naprawia wannę|naprawia zlew"),
    ("elektryk", "na drabinie|w piwnicy|na słupie|w kuchni"),
    ("malarz", "na drabinie|w pracowni|maluje obraz|maluje ścianę|maluje płot|maluje dom|ma pędzel|ma farby|"
               "maluje portret|maluje kwiaty|maluje morze|maluje pokój"),
    ("fryzjer fryzjerka", "w salonie|przy lustrze|ma nożyczki|ma grzebień"),
    ("krawiec krawcowa szwaczka", "szyje sukienkę|szyje spodnie|szyje płaszcz|szyje koszulę|szyje kurtkę|"
                                  "szyje suknię|ma nożyczki|ma igłę|ma nitkę"),
    ("harcerz harcerka", "w lesie|w namiocie|przy ognisku|na biwaku|na polanie|na wycieczce|rozpala ognisko|"
                         "ma plecak|ma mapę|ma kompas|śpiewa piosenkę|ma namiot|niesie plecak|rozbija namiot"),
    ("turysta", "w górach|na szlaku|w hotelu|na plaży|na wycieczce|w muzeum|na dworcu|w namiocie|ma mapę|"
                "ma plecak|robi zdjęcie"),
    ("alpinista", "w górach|na skale|na szczycie|na górze|ma linę"),
    ("narciarz", "na nartach|na stoku|w górach|na wyciągu|na śniegu"),
    ("kolarz rowerzysta", "na rowerze|na drodze|na ścieżce|w parku|na wyścigu"),
    ("robot", "na stole|na półce|na podłodze|na dywanie|w pudełku|w pokoju|w kuchni|w kosmosie|pod łóżkiem|"
              "w fabryce|sprząta pokój|myje podłogę|ma antenę|niesie pudło|myje naczynia|ma przycisk|ma baterię"),
    ("kosmita", "@kosmos|w ogrodzie|na dachu|w lesie|ma antenę"),
    ("syrenka", "w morzu|na skale|w wodzie|na plaży|pod wodą|w oceanie|ma ogon|czesze włosy"),
    ("jednorożec", "na łące|w lesie|na tęczy|w bajce|na polanie|w chmurach|ma róg"),
    ("dinozaur tyranozaur", "w muzeum|w lesie|w dżungli|w bajce|na wyspie"),
    ("potwór straszydło", "pod łóżkiem|w szafie|w jaskini|w lesie|w jeziorze|w piwnicy|na strychu|w bajce"),
    ("mumia", "w muzeum|w piramidzie"),
    ("troll", "pod mostem|w jaskini|w górach|w lesie|w bajce"),
    ("elf goblin", "w lesie|w jaskini|w bajce|w górach|pod drzewem"),
    ("bałwan bałwanek", "w ogrodzie|na podwórku|na śniegu|w parku|na górce|przed domem|za domem|"
                        "ma marchewkę|ma garnek|ma szalik|ma miotłę|ma guziki"),
    # --- zwierzęta domowe ---
    ("kot kotek kociak koteczek kocur kotka",
     "@meble_na|@meble_pod|w domu|w pokoju|w kuchni|w koszu|w koszyku|w pudełku|w kartonie|w szafie|na oknie|"
     "na drzewie|na płocie|na dachu|za piecem|przy kominku|u weterynarza|w ogrodzie|na podwórku|na trawie|"
     "w trawie|w krzakach|na strychu|w piwnicy|w walizce|w praniu|na słońcu|"
     "pije mleko|je rybę|łapie mysz|goni mysz|łapie muchę|myje łapkę|drapie kanapę|drapie fotel|goni piłkę|"
     "goni ptaka|lubi mleko|lubi rybę|widzi mysz|widzi ptaka|ma kłębek|goni kłębek|łapie motyla|liże łapkę"),
    ("pies piesek szczeniak psiak",
     "w budzie|na spacerze|w parku|w lesie|na łące|w wodzie|w kałuży|na plaży|w samochodzie|w aucie|w domu|"
     "w pokoju|w kuchni|na kanapie|na fotelu|na łóżku|na dywanie|na podłodze|na schodach|pod stołem|"
     "pod łóżkiem|pod kocem|w koszu|u weterynarza|przy drzwiach|na smyczy|za płotem|w śniegu|na śniegu|"
     "przy kominku|na balkonie|w ogrodzie|na podwórku|na trawie|w krzakach|pod drzewem|"
     "je kość|gryzie kość|gryzie kapeć|gryzie but|niesie patyk|niesie gazetę|niesie kapcie|goni kota|"
     "goni piłkę|goni zająca|goni listonosza|kopie dół|pilnuje domu|liże rękę|pije wodę|łapie piłkę|"
     "merda ogonem|ma kość|ma budę|ma smycz|ma obrożę|szuka kości"),
    ("chomik", "w klatce|w kołowrotku|w pudełku|na dywanie|pod szafą|pod łóżkiem|w kieszeni|na stole|w norce"),
    ("królik króliczek", "w klatce|w trawie|na łące|w ogrodzie|w norze|w kapuście|na trawie|w kapeluszu|w polu|"
                         "pod krzakiem|na trawniku|w koszyku|je marchewkę|je sałatę|je kapustę|je trawę|"
                         "gryzie marchewkę|lubi marchewkę|kopie norę"),
    ("mysz myszka", "w norce|w norze|w kuchni|pod szafą|w serze|w spiżarni|w piwnicy|w stodole|w trawie|"
                    "pod podłogą|na strychu|w szafie|w szufladzie|w młynie|w polu|je ser|gryzie ser|gryzie chleb|"
                    "je ziarno|lubi ser|ma norkę|je okruszki|ma ogonek|niesie ser"),
    ("papuga papużka", "w klatce|na drzewie|na gałęzi|na ramieniu|na szafie|w dżungli|na głowie|w zoo"),
    ("rybka", "w akwarium|w wodzie|w stawie|w jeziorze|w rzece|w morzu|w sieci"),
    ("żółw", "w trawie|w ogrodzie|w wodzie|na piasku|na plaży|w morzu|pod liściem|w akwarium|na kamieniu|"
             "w stawie|je sałatę|ma skorupę"),
    # --- zwierzęta z farmy ---
    ("krowa krówka", "@farma|w oborze|je trawę|je siano|daje mleko|skubie trawę|pije wodę|ma cielę|ma rogi|"
                     "ma dzwonek"),
    ("byk cielę cielak cielaczek", "na łące|na pastwisku|w oborze|na farmie|w zagrodzie|na wsi"),
    ("byk", "ma rogi"),
    ("koń konik źrebak źrebię kucyk",
     "w stajni|na łące|na pastwisku|na farmie|na polu|w zagrodzie|w cyrku|na wsi|na wyścigu|w lesie|na plaży|"
     "na prerii|je owies|je siano|je jabłko|je marchewkę|je trawę|pije wodę|ma grzywę|ma siodło"),
    ("koń", "ciągnie wóz|ciągnie sanie|ciągnie bryczkę|ciągnie karetę|ma podkowy"),
    ("osioł osiołek", "na łące|w stajni|na farmie|w zagrodzie|na pastwisku|na wsi|w górach|w szopce|je siano|"
                      "je marchewkę|niesie worek"),
    ("koza kózka koziołek", "na łące|w zagrodzie|na farmie|na pastwisku|w górach|na skale|na wsi|w ogrodzie|"
                            "je trawę|skubie trawę|je kapustę|je liście|ma rogi|ma bródkę"),
    ("koza", "daje mleko"),
    ("owca owieczka baranek", "na łące|na pastwisku|w zagrodzie|na farmie|w górach|na wsi|w szopce|je trawę|"
                              "skubie trawę|ma wełnę"),
    ("owca", "daje wełnę"),
    ("świnia prosiak prosiaczek prosię", "w chlewie|w błocie|w kałuży|na farmie|w zagrodzie|na podwórku|na wsi|"
                                         "je ziemniaki|je jabłka|je kapustę|lubi błoto"),
    ("kura kurka kogut kurczak kurczaczek", "w kurniku|na podwórku|na farmie|na płocie|w trawie|w ogrodzie|"
                                            "na wsi|na łące|w zagrodzie|dziobie ziarno|je ziarno|je robaka"),
    ("kura kurka", "w gnieździe|znosi jajko|znosi jajka|ma kurczęta"),
    ("kogut", "na dachu|budzi rolnika|budzi dzieci|budzi dziadka|ma grzebień"),
    ("kaczka kaczuszka kaczątko kaczor", "w stawie|na stawie|w wodzie|na wodzie|na podwórku|na farmie|"
                                         "w kałuży|na jeziorze|na łące|w trzcinie|na rzece|je chleb"),
    ("kaczka", "ma kaczątka"),
    ("kaczuszka", "w wannie"),
    ("gęś gąska gąsior", "na łące|na podwórku|na farmie|w stawie|na stawie|na wsi|w zagrodzie|je trawę"),
    ("indyk", "na podwórku|na farmie|w zagrodzie|na wsi"),
    # --- zwierzęta leśne i polne ---
    ("lis lisek", "w lesie|w norze|na łące|na polu|w kurniku|pod krzakiem|na polanie|w krzakach|na śniegu|"
                  "w zoo|w bajce|goni zająca|łapie kurę|kradnie kurę|ma ogon|ma norę|łapie mysz|goni kurę"),
    ("wilk wilczek", "w lesie|na polanie|w górach|pod drzewem|na śniegu|w bajce|w zoo|w jaskini|goni zająca"),
    ("jeż jeżyk", "w lesie|w ogrodzie|w liściach|w trawie|pod krzakiem|na ścieżce|w parku|pod liściem|"
                  "na trawie|je jabłko|niesie jabłko|ma kolce"),
    ("zając zajączek", "w polu|na łące|w lesie|w ogrodzie|w kapuście|w trawie|pod krzakiem|na polanie|"
                       "na śniegu|je marchewkę|je kapustę|je trawę"),
    ("zajączek", "w koszyku|niesie jajka|ma koszyk"),
    ("sarna jeleń jelonek łoś", "w lesie|na łące|na polanie|w polu|na polu|je trawę"),
    ("jeleń łoś", "ma poroże"),
    ("dzik", "w lesie|w błocie|na polu|w krzakach|na polanie|w kałuży"),
    ("niedźwiedź niedźwiadek", "w lesie|w jaskini|w górach|w rzece|pod drzewem|na drzewie|w zoo|w bajce|"
                               "je miód|lubi miód|je maliny|łowi ryby|zbiera maliny|je ryby|je jagody|szuka miodu"),
    ("miś", "je miód|lubi miód|ma miód|szuka miodu"),
    ("wiewiórka", "na drzewie|na gałęzi|w dziupli|w lesie|w parku|na sośnie|w ogrodzie|na płocie|na trawie|"
                  "je orzech|zbiera orzechy|je żołądź|zbiera żołędzie|chowa orzechy|zbiera szyszki|ma ogon|"
                  "niesie orzech"),
    ("borsuk", "w norze|w lesie|pod drzewem"),
    ("kret", "w ziemi|pod ziemią|w ogrodzie|w kopcu|kopie kopiec"),
    ("bóbr", "w rzece|w wodzie|w stawie|na brzegu|w lesie|nad rzeką|buduje tamę|gryzie drzewo|ścina drzewo|"
             "ma ogon"),
    ("sowa sówka", "na drzewie|na gałęzi|w dziupli|w lesie|na wieży|na strychu|w stodole|w bajce|łapie mysz|"
                   "widzi mysz"),
    ("ślimak", "na liściu|w trawie|w ogrodzie|na kamieniu|na sałacie|na drodze|na ścieżce|na kapuście|na murze|"
               "je sałatę|je liść|niesie domek|ma domek|ma muszlę|je kapustę"),
    ("żaba żabka", "w stawie|w wodzie|na liściu|na kamieniu|w trawie|na łące|w kałuży|w rzece|na brzegu|"
                   "w trzcinie|w bajce|łapie muchę|łapie komara|je muchę|je komara|ma koronę"),
    # --- owady i małe stworzenia ---
    ("mrówka", "@owady|w mrowisku|na ścieżce|na stole|w kuchni|na drzewie|na kanapce|w lesie|niesie liść|"
               "niesie gałązkę|buduje mrowisko|niesie ziarenko|niesie okruszek|niesie listek|niesie patyczek"),
    ("pszczoła pszczółka", "@owady|w ulu|na róży|na kwiecie|na słoneczniku|nad łąką|zbiera nektar|robi miód|"
                           "ma żądło|lubi kwiaty|szuka kwiatów"),
    ("osa", "na jabłku|na kwiatku|w ogrodzie|na oknie|w kuchni|na ścianie|na lodach|na ciastku|ma żądło"),
    ("trzmiel", "@owady|na róży|nad łąką"),
    ("biedronka", "@owady|na ręce|na palcu|na oknie|na róży|na nosie|ma kropki"),
    ("motyl motylek", "@owady|na róży|nad łąką|na nosie|na kwiecie|w parku|pije nektar|lubi kwiaty|ma skrzydła"),
    ("mucha", "na ścianie|na oknie|na szybie|na suficie|na stole|w kuchni|na lampie|na nosie|na ciastku|w zupie|"
              "na jabłku|w pokoju"),
    ("komar", "na ścianie|w pokoju|na suficie|na ręce|na nosie|nad stawem|w lesie|w namiocie|nad wodą"),
    ("pająk pajączek", "w sieci|na pajęczynie|na ścianie|na suficie|w kąciku|w piwnicy|na strychu|w łazience|"
                       "w wannie|pod łóżkiem|w szafie|na lampie|w garażu|plecie sieć|łapie muchę|robi sieć"),
    ("żuk chrząszcz", "w trawie|na liściu|na ścieżce|w lesie|pod kamieniem|na kwiatku|w ziemi"),
    ("chrząszcz", "w trzcinie"),
    ("ważka", "nad stawem|nad wodą|na trzcinie|na liściu|nad rzeką|nad jeziorem|nad łąką"),
    ("świetlik", "w lesie|w trawie|na łące|w ogrodzie|w słoiku"),
    ("gąsienica", "na liściu|na jabłku|w jabłku|na kapuście|w ogrodzie|na gałęzi|je liść|je jabłko|"
                  "je kapustę|je liście"),
    ("robak robaczek dżdżownica", "w jabłku|w ziemi|w trawie|w ogrodzie|na ścieżce|pod kamieniem|w kałuży|"
                                  "na chodniku"),
    ("świerszcz", "w trawie|na łące|za piecem|w ogrodzie|za kominem"),
    ("pasikonik", "w trawie|na łące|na liściu|w ogrodzie"),
    # --- ptaki ---
    ("ptak ptaszek ptaszyna", "@ptaki|w gnieździe|na niebie|w klatce|w lesie|na łące|na drucie|nad łąką|"
                              "nad lasem|na kominie|je ziarno|dziobie ziarno|je robaka|buduje gniazdo|je okruszki|"
                              "śpiewa piosenkę|je ziarenka|niesie gałązkę|ma gniazdo|ma skrzydła|karmi pisklęta"),
    ("wróbel wróbelek", "@ptaki|na chodniku|w parku|na podwórku|w krzakach|na drucie|je ziarno|je okruszki|"
                        "dziobie ziarno"),
    ("bocian", "na łące|na kominie|w gnieździe|na dachu|na polu|w stawie|na niebie|na słupie|nad łąką|"
               "łapie żabę|je żabę|buduje gniazdo|niesie dziecko|ma gniazdo"),
    ("wrona sroka kruk", "na drzewie|na płocie|na polu|na dachu|na gałęzi|na łące|na śniegu|na słupie"),
    ("gołąb gołąbek", "na dachu|na rynku|na placu|w parku|na parapecie|na ulicy|na chodniku|na ławce|"
                      "na balkonie|na pomniku|je okruszki"),
    ("sikorka", "@ptaki|je ziarno"),
    ("dzięcioł", "na drzewie|na sośnie|w lesie|na pniu|w dziupli|na gałęzi"),
    ("kukułka", "w lesie|w zegarze|na drzewie|na gałęzi"),
    ("jaskółka", "na niebie|w gnieździe|na dachu|pod dachem|nad łąką|w stajni|na drucie|nad wodą"),
    ("orzeł sokół jastrząb", "na niebie|w górach|na skale|w gnieździe|nad lasem|na drzewie|nad górami|w zoo"),
    ("łabędź", "na stawie|na jeziorze|w wodzie|na wodzie|na rzece|w parku"),
    ("mewa", "nad morzem|na plaży|na piasku|na falach|na statku|w porcie|na molo|na morzu|na dachu"),
    ("paw", "w zoo|w ogrodzie|w parku|na trawie|na murze"),
    ("pingwin", "na lodzie|na śniegu|w wodzie|w morzu|w zoo|na krze|łapie rybę|je rybę|je ryby"),
    ("struś", "na pustyni|w zoo|na sawannie|w piasku"),
    ("flaming", "w wodzie|w zoo|w jeziorze"),
    ("pelikan", "nad morzem|na plaży|w wodzie|w zoo|na molo|łapie rybę"),
    ("tukan", "w dżungli|na drzewie|w zoo"),
    # --- zwierzęta wodne ---
    ("foka", "na lodzie|w wodzie|w morzu|na plaży|w zoo|na krze|na skale|w cyrku|łapie rybę|je rybę|je ryby|"
             "łapie piłkę|ma piłkę|ma wąsy"),
    ("delfin", "w morzu|w wodzie|w oceanie|w basenie|pod wodą|łapie rybę|je ryby"),
    ("rekin wieloryb kaszalot ośmiornica kałamarnica meduza", "@morze"),
    ("ośmiornica", "w akwarium|w jaskini"),
    ("meduza", "na plaży"),
    ("krab rozgwiazda", "na plaży|na piasku|w morzu|na skale|w wodzie"),
    ("krab", "pod kamieniem"),
    ("rak", "w rzece|w stawie|w wodzie|pod kamieniem"),
    ("ryba", "@ryby|w morzu|w akwarium|pod wodą|w oceanie"),
    ("łosoś pstrąg karp szczupak okoń sum węgorz", "@ryby"),
    ("karp", "w wannie"),
    ("hipopotam", "w wodzie|w rzece|w zoo|w błocie|w jeziorze"),
    ("krokodyl aligator", "w wodzie|w rzece|w zoo|w błocie|na brzegu|na piasku"),
    # --- zwierzęta egzotyczne ---
    ("lew lwica", "@sawanna|w klatce|w cyrku|w trawie|pod drzewem|na skale"),
    ("tygrys tygrysek tygrysica", "w zoo|w dżungli|w klatce|w cyrku|w trawie|w wodzie|ma paski"),
    ("słoń", "@sawanna|w cyrku|w dżungli|w wodzie|w rzece|w błocie|pije wodę|je trawę|je siano|ma trąbę|"
             "niesie kłodę"),
    ("żyrafa", "@sawanna|pod drzewem|je liście|ma plamy"),
    ("zebra", "@sawanna|ma paski|je trawę"),
    ("nosorożec", "@sawanna|w błocie|ma róg"),
    ("antylopa gepard", "@sawanna"),
    ("lampart pantera jaguar", "@dżungla"),
    ("małpa małpka małpeczka", "@dżungla|w klatce|na lianie|w cyrku|je banana|lubi banany|ma ogon"),
    ("goryl szympans orangutan", "@dżungla|w klatce"),
    ("lemur koala", "na drzewie|na gałęzi|w zoo"),
    ("koala", "je liście|lubi liście"),
    ("leniwiec", "@dżungla"),
    ("panda", "w zoo|w lesie|na drzewie|je bambus|lubi bambus"),
    ("kangur", "w zoo|na łące|ma torbę"),
    ("wielbłąd", "na pustyni|w zoo|w cyrku|na piasku|ma garb|pije wodę|niesie bagaż"),
    ("wąż", "w trawie|w dżungli|na drzewie|w zoo|na kamieniu|na piasku|pod kamieniem|na gałęzi|w koszyku"),
    ("jaszczurka", "na kamieniu|w trawie|na piasku|na murze|pod kamieniem|na słońcu"),
    ("kameleon", "na gałęzi|na drzewie|na liściu|w zoo"),
    # --- zabawki ---
    ("miś misiek misiaczek pluszak lalka laleczka", "@meble_na|@meble_pod|@schowki|@zabawki"),
    ("lalka laleczka", "w domku"),
    ("piłka piłeczka", "@meble_pod|na podłodze|na dywanie|w koszu|w szafie|na boisku|w bramce|na trawie|"
                       "w ogrodzie|na podwórku|w krzakach|na drzewie|na dachu|w kałuży|w wodzie|w basenie|"
                       "w piaskownicy|w parku|pod samochodem|za płotem|w plecaku|na plaży|w przedpokoju"),
    ("klocki", "na podłodze|na dywanie|na stole|w pudełku|w koszu|w skrzyni|pod łóżkiem|pod kanapą|w pokoju|"
               "na półce|w kartonie"),
    ("balon balonik", "na niebie|w chmurach|na suficie|na drzewie|w pokoju|nad domem|nad łąką|nad miastem|"
                      "na urodzinach"),
    ("latawiec", "na niebie|na drzewie|w chmurach|nad łąką|nad domem|nad morzem|na plaży|na łące"),
    ("samochodzik autko", "na podłodze|na dywanie|na stole|w pudełku|pod łóżkiem|pod kanapą|w piaskownicy|"
                          "w kieszeni|na półce"),
    ("bączek jojo kostka", "na podłodze|na stole|w pudełku|w kieszeni|na dywanie"),
    ("puzzle", "na stole|na podłodze|na dywanie|w pudełku|na półce"),
    ("kredki kredka", "@piórnik|na stole|w pudełku|na biurku|na podłodze|w plecaku|w szufladzie|pod stołem"),
    ("grzechotka", "w łóżeczku|w wózku|na podłodze|na kocu"),
    ("sanki", "na śniegu|w piwnicy|w garażu|na górce|na strychu"),
    ("narty łyżwy", "w piwnicy|w garażu|w szafie|na strychu"),
    ("narty", "na śniegu"),
    ("łyżwy", "na lodzie"),
    ("rower rowerek hulajnoga rolki deskorolka", "@sprzęt"),
    ("huśtawka zjeżdżalnia piaskownica trampolina", "@plac_zabaw"),
    ("karuzela", "w lunaparku|na jarmarku|w parku"),
    ("zabawki", "na podłodze|na dywanie|w pudełku|w koszu|w skrzyni|pod łóżkiem|w pokoju|na półce"),
    # --- kuchnia i jedzenie ---
    ("łyżka łyżeczka widelec nóż sztućce", "@sztućce"),
    ("łyżka", "w zupie|w słoiku|w garnku"),
    ("łyżeczka", "w kubku|w herbacie|w jogurcie"),
    ("nóż", "na desce"),
    ("talerz talerzyk miska miseczka kubek kubeczek szklanka filiżanka dzbanek", "@naczynia"),
    ("miska", "na podłodze"),
    ("garnek patelnia czajnik", "na kuchence|w szafce|w zlewie|w kuchni|na półce"),
    ("chleb bułka bułeczka rogal rogalik chała pączek drożdżówka precel ciasto ciastko tort sernik szarlotka piernik",
     "@pieczywo"),
    ("chleb ciasto pizza", "w piekarniku"),
    ("tort ciasto", "na urodzinach|w lodówce"),
    ("ciastko", "w pudełku|w słoiku"),
    ("piernik", "na choince"),
    ("pączek tort", "w cukierni"),
    ("jabłko gruszka śliwka banan pomarańcza mandarynka cytryna brzoskwinia jabłuszko morela arbuz melon ananas "
     "kiwi winogrono", "@owoce"),
    ("jabłko gruszka śliwka jabłuszko czereśnia wiśnia brzoskwinia morela", "@owoce_drzewo"),
    ("cytryna", "w herbacie"),
    ("truskawka malina jagoda poziomka borówka czereśnia wiśnia porzeczka", "@jagody"),
    ("ser masło szynka kiełbasa parówka jogurt serek", "@lodówka"),
    ("ser masło szynka", "na chlebie|na bułce|na kanapce"),
    ("kiełbasa", "na grillu"),
    ("parówka", "w bułce"),
    ("jajko jajeczko", "w lodówce|w koszyku|w kurniku|w gnieździe|na talerzu|w misce|na stole|w garnku|na patelni"),
    ("pisanka", "w koszyku|na stole|w trawie|na talerzu"),
    ("zupa rosół barszcz kasza makaron ryż gulasz bigos owsianka kisiel budyń", "@garnek"),
    ("owsianka kisiel budyń", "w miseczce"),
    ("pizza kanapka naleśnik kotlet frytki hamburger pierogi placki", "na talerzu|na stole|w pudełku|w kuchni"),
    ("kotlet naleśnik placki", "na patelni"),
    ("kanapka", "w plecaku|w torbie"),
    ("frytki", "w torebce"),
    ("pierogi", "w garnku"),
    ("lody", "w lodówce|w zamrażarce|w wafelku|na patyku|w miseczce|w kubeczku|na talerzu|w lodziarni"),
    ("cukierek lizak czekolada batonik żelki ciasteczko", "w kieszeni|w torbie|w plecaku|w szufladzie|"
                                                          "w pudełku|na stole|w słoiku|w sklepie|w torebce"),
    ("miód dżem marmolada keczup majonez musztarda", "w słoiku|na stole|w lodówce|na chlebie|na kanapce|na bułce"),
    ("miód dżem", "na naleśniku"),
    ("miód", "w ulu"),
    ("mleko sok woda kakao herbata kawa kompot lemoniada oranżada", "@napoje"),
    ("mleko", "w misce"),
    ("woda", "w czajniku|w wannie|w basenie|w stawie|w kranie|w wiadrze|w konewce"),
    ("herbata kawa kakao", "w filiżance|w termosie"),
    ("marchewka marchew ogórek pomidor ziemniak cebula kapusta sałata papryka dynia burak groszek rzodkiewka "
     "kukurydza czosnek", "@warzywa"),
    ("marchewka ziemniak burak cebula rzodkiewka", "w ziemi"),
    ("ziemniak kapusta kukurydza dynia burak", "na polu"),
    ("marchewka", "w zupie"),
    ("ogórek pomidor papryka rzodkiewka", "w sałatce|na kanapce"),
    ("pomidor ogórek", "w szklarni"),
    # --- ubrania ---
    ("czapka czapeczka szalik kurtka sweter sweterek bluza bluzka koszula koszulka sukienka spódnica spódniczka "
     "płaszcz piżama spodnie spodenki szlafrok kombinezon", "@ubrania"),
    ("czapka", "na głowie|na bałwanie"),
    ("szalik", "na szyi|na bałwanie"),
    ("piżama", "pod poduszką"),
    ("buty but bucik buciki kapcie kalosze trampki sandały kozaki botki", "@obuwie"),
    ("buty kalosze", "w kałuży|na wycieraczce"),
    ("skarpetka skarpetki rękawiczka rękawiczki", "w szafie|w szufladzie|na podłodze|pod łóżkiem|w walizce|"
                                                  "w praniu|w pralce|na kaloryferze"),
    ("rękawiczki", "w kieszeni|na śniegu"),
    ("okulary", "na nosie|na stole|na półce|w kieszeni|w torbie|na biurku|na głowie"),
    ("kapelusz", "na głowie|na wieszaku|w szafie|na stole|na półce|w pudełku"),
    ("parasol parasolka", "w przedpokoju|w torbie|w samochodzie|w szafie|na wieszaku|w deszczu"),
    ("parasol", "na plaży"),
    # --- szkoła ---
    ("książka książeczka zeszyt ołówek długopis gumka linijka nożyczki klej kartka kolorowanka pędzel farby "
     "plastelina temperówka", "@szkolne"),
    ("ołówek długopis gumka linijka nożyczki klej temperówka", "@piórnik"),
    ("książka książeczka", "w bibliotece|pod poduszką|w księgarni"),
    ("kartka", "w zeszycie"),
    ("plecak", "w szkole|w klasie|na krześle|w przedpokoju|na plecach|pod biurkiem|pod ławką|w szafie|"
               "na podłodze|w autobusie"),
    ("piórnik", "w plecaku|na biurku|na ławce|na stole|w szufladzie|w torbie"),
    ("tablica", "w klasie|w szkole|na ścianie"),
    ("globus mapa", "na biurku|na półce|w klasie|na stole|w szkole"),
    ("mapa", "na ścianie|w plecaku"),
    # --- dom ---
    ("lampa lampka", "na stole|na biurku|w pokoju|na komodzie|na półce|w salonie|przy łóżku|na stoliku"),
    ("lampa", "na suficie"),
    ("zegar", "na ścianie|na półce|w kuchni|na wieży|w salonie|na komodzie|w pokoju"),
    ("zegarek", "na ręce|w kieszeni|na stole|na biurku|w szufladzie|na półce"),
    ("obraz obrazek", "na ścianie|w muzeum|w pokoju|w ramce|w salonie|nad łóżkiem|nad kanapą"),
    ("lustro lusterko", "na ścianie|w łazience|w przedpokoju|w szafie"),
    ("lusterko", "w torebce"),
    ("telefon", "na stole|w kieszeni|w torbie|na biurku|w plecaku|na półce|w samochodzie|pod poduszką|"
                "w torebce|na kanapie"),
    ("klucz kluczyk", "w kieszeni|w zamku|w drzwiach|na stole|w torbie|w szufladzie|pod wycieraczką|w torebce|"
                      "na stoliku"),
    ("ręcznik", "w łazience|na wieszaku|w szafie|na plaży|na piasku|w torbie|na kaloryferze"),
    ("mydło szampon szczoteczka pasta grzebień szczotka", "w łazience|na umywalce|w szafce|w kosmetyczce"),
    ("mydło", "w wannie"),
    ("szczoteczka", "w kubku"),
    ("grzebień", "w torebce|w kieszeni"),
    ("poduszka koc kocyk kołdra", "na łóżku|na kanapie|w szafie|na fotelu|na podłodze"),
    ("kocyk", "w łóżeczku"),
    ("koc", "na trawie|na plaży"),
    ("kwiat kwiatek kwiaty róża tulipan stokrotka mak słonecznik fiołek bratek konwalia niezapominajka", "@kwiaty"),
    ("mak słonecznik", "na polu"),
    ("konwalia fiołek", "w lesie"),
    ("stokrotka mlecz dmuchawiec", "w trawie|na trawniku|na łące"),
    ("świeczka świeca", "na torcie|na stole|na oknie"),
    ("prezent", "pod choinką|na stole|w pudełku|w szafie|w torbie|na urodzinach|w worku"),
    ("paczka", "na poczcie|na stole|pod drzwiami|w samochodzie|na wycieraczce"),
    ("choinka", "w pokoju|w salonie|w lesie|w domu|na rynku|na placu"),
    ("bombka", "na choince|w pudełku"),
    ("list kartka pocztówka", "w kopercie|w skrzynce|na stole|na poczcie|w torbie|w szufladzie"),
    ("pieniądze moneta pieniążek grosik", "w portfelu|w skarbonce|w kieszeni|w torebce|w banku|na stole"),
    ("skarb", "w skrzyni|w jaskini|na wyspie|w piasku|pod drzewem|w zamku|w ziemi|w kufrze"),
    ("korona", "na głowie|w zamku|na poduszce|w skrzyni|w muzeum"),
    ("miotła", "w kuchni|w szafie|w przedpokoju|w piwnicy|w garażu|na podwórku"),
    ("wiadro wiaderko łopatka grabki foremka", "w piaskownicy|na plaży|w ogrodzie|na piasku|w szopie|w garażu"),
    # --- przyroda ---
    ("słońce", "@niebo|za chmurą"),
    ("księżyc gwiazda gwiazdka chmura chmurka tęcza", "@niebo"),
    ("księżyc", "za chmurą"),
    ("gwiazda gwiazdka", "na choince"),
    ("śnieg", "na dachu|w ogrodzie|na drzewie|w górach|na ulicy|na polu|w lesie|na łące|na czapce"),
    ("mgła", "nad łąką|w lesie|nad jeziorem|nad rzeką|w górach|nad polem"),
    ("drzewo drzewko krzak krzew brzoza sosna dąb klon świerk jodła lipa wierzba jabłoń grusza buk", "@drzewa"),
    ("jabłoń grusza", "w sadzie"),
    ("wierzba", "nad rzeką|nad stawem"),
    ("grzyb grzybek", "w lesie|w trawie|pod drzewem|w koszyku|w mchu|pod sosną|na polanie|na pniu"),
    ("liść liście listek", "na drzewie|na gałęzi|na trawie|w kałuży|na wodzie|na ścieżce|w parku|na ławce|"
                           "na chodniku|w ogrodzie"),
    ("kasztan żołądź szyszka orzech", "pod drzewem|w parku|na trawie|w kieszeni|w koszyku|na ścieżce|na drzewie"),
    ("żołądź szyszka orzech", "w lesie"),
    ("szyszka", "na sośnie"),
    ("orzech", "w dziupli"),
    ("kamień kamyk muszla muszelka", "na plaży|na piasku|w wodzie|w kieszeni|na ścieżce"),
    ("kamień kamyk", "w rzece|w ogrodzie"),
    ("muszla muszelka", "w morzu"),
    ("muszelka", "w wiaderku"),
    ("sopel", "na dachu|na drzewie|na rynnie|na oknie|na gałęzi"),
    ("kałuża", "na ulicy|na drodze|na chodniku|na podwórku|w parku|na ścieżce"),
    ("ogień", "w kominku|w piecu|w ognisku"),
    ("ognisko", "w lesie|na plaży|na polanie|w ogrodzie|nad jeziorem|nad rzeką|na łące"),
    # --- pojazdy ---
    ("auto samochód", "@ulica"),
    ("autobus tramwaj taksówka", "na ulicy|na przystanku|na drodze|w mieście|na moście|w zajezdni|"
                                 "na skrzyżowaniu"),
    ("autobus", "na dworcu"),
    ("karetka radiowóz", "na ulicy|na drodze|w mieście|przy szpitalu|w garażu|na skrzyżowaniu|na moście"),
    ("motor motocykl skuter", "na ulicy|na drodze|w garażu|na parkingu|na autostradzie|pod domem"),
    ("ciężarówka wywrotka", "na drodze|na autostradzie|na budowie|na parkingu|w garażu|na moście|na ulicy|"
                            "w tunelu"),
    ("koparka dźwig betoniarka walec spychacz", "na budowie|na drodze|na placu|na ulicy"),
    ("koparka", "w piasku"),
    ("pociąg lokomotywa wagon kolejka", "na torach|na stacji|na dworcu|na moście|w tunelu|w górach"),
    ("łódka łódź jacht żaglówka kajak ponton tratwa", "@łodzie"),
    ("statek okręt", "na morzu|na jeziorze|na rzece|na wodzie|w porcie|w zatoce|na falach"),
    ("samolot helikopter śmigłowiec odrzutowiec szybowiec sterowiec", "@powietrze"),
    ("samolot helikopter śmigłowiec", "na lotnisku|w hangarze"),
    ("helikopter śmigłowiec", "na dachu"),
    ("rakieta", "w kosmosie|na niebie|na księżycu|w chmurach"),
    ("traktor ciągnik kombajn", "na polu|na farmie|w stodole|na łące|na drodze|w garażu|na wsi"),
]


def rozwin(spec, nazwa="?"):
    out = []
    for el in spec.split("|"):
        el = " ".join(el.split())
        if not el:
            continue
        if el.startswith("@"):
            klucz = el[1:]
            if klucz in M:
                out += rozwin(M[klucz], klucz)
            elif klucz in C:
                out += rozwin(C[klucz], klucz)
            else:
                raise KeyError(f"nieznana grupa @{klucz} (w: {nazwa})")
        else:
            out.append(el)
    return out


# Zdania, których nie chcemy mimo pasujących grup (np. „babcia u babci”).
WYKLUCZONE_PARY = {("babcia", "u babci"), ("dziadek", "u dziadka"), ("ciocia", "u cioci"), ("wujek", "u wujka"),
                   ("sąsiad", "u sąsiada"), ("sąsiadka", "u sąsiadki"), ("brat", "goni brata"),
                   ("siostra", "goni siostrę"), ("brat", "ma brata"), ("siostra", "ma siostrę"),
                   ("mama", "słucha mamy"), ("mama", "szuka mamy"), ("mama", "przytula mamę"),
                   ("mama", "rysuje mamę"), ("tata", "słucha taty"), ("tata", "szuka taty"),
                   ("tata", "przytula tatę"), ("tata", "rysuje tatę"), ("chłopiec", "ma warkocze"),
                   ("brat", "ma warkocze"), ("synek", "ma warkocze"), ("babcia", "przytula babcię"),
                   ("babcia", "rysuje babcię"), ("dziadek", "rysuje dziadka"), ("dziadek", "budzi dziadka")}


def zbuduj():
    zdania, bledy = [], []
    for podmioty, spec in P:
        wyrazenia = rozwin(spec, podmioty)
        for p in podmioty.split():
            for w in wyrazenia:
                if (p, w) in WYKLUCZONE_PARY:
                    continue
                z = f"{p} {w}"
                if len(z.split()) != 3:
                    bledy.append(f"nie 3 wyrazy: {z!r}")
                zdania.append(z)
    if bledy:
        print("\n".join(bledy)); sys.exit(1)
    return sorted(set(zdania), key=klucz_sortowania)


def karty_zdania(zdanie):
    return [k for w in zdanie.split() for k in na_karty(w)]


if __name__ == "__main__":
    arg = sys.argv[1:]
    sjp, lista = None, None
    if "--sjp" in arg:
        i = arg.index("--sjp")
        with open(arg[i + 1], encoding="utf-8") as f:
            sjp = set(l.strip() for l in f)
        del arg[i:i + 2]
    if "--lista" in arg:
        i = arg.index("--lista"); lista = arg[i + 1]; del arg[i:i + 2]

    zdania = zbuduj()
    if sjp is not None:
        jednoliterowe = {"w", "u", "z", "i", "a", "o"}  # słownik do gier nie ma wyrazów 1-literowych
        brak = sorted({w for z in zdania for w in z.split() if w not in sjp and w not in jednoliterowe})
        if brak:
            print("Wyrazów nie ma w słowniku do gier SJP.pl:", ", ".join(brak)); sys.exit(1)
    wszystkie = len(zdania)
    zdania = [z for z in zdania if miesci_sie(karty_zdania(z))]
    # [zdanie, mieści się w 1 talii, ma dwuznak/zmiękczenie]
    dane = [[z, int(miesci_sie(karty_zdania(z), 1)), int(any(len(k) > 1 for k in karty_zdania(z)))] for z in zdania]
    n = len(dane)
    print(f"Zdań: {n} (pominięte, bo nie mieszczą się w {TALIE} taliach: {wszystkie - n}) | "
          f"z 1 talii: {sum(x[1] for x in dane)} | bez dwuznaków: {sum(not x[2] for x in dane)}")
    if arg:
        # Pogrupowane po podmiocie, żeby aplikacja mogła najpierw losować podmiot (inaczej ponad połowa
        # zdań zaczynałaby się od „mama”, „dziecko” itp., bo ludzie mają najwięcej pasujących wyrażeń).
        grupy = {}
        for z, _, dw in dane:
            p, reszta = z.split(" ", 1)
            grupy.setdefault(p, []).append([reszta, dw])
        with open(arg[0], "w", encoding="utf-8") as f:
            f.write("// Zdania z 3 wyrazów dla aplikacji Geniuszek od Pieluszek (wygenerowane przez narzedzia/build_zdania.py)\n")
            f.write(f"// {{ podmiot: [[reszta zdania, d], ...] }}: d = 1 jeśli zdanie ma dwuznak/zmiękczenie.\n")
            f.write(f"// Są tylko zdania, które da się ułożyć z {TALIE} zestawów kart.\n")
            f.write("window.ZDANIA = ")
            json.dump(grupy, f, ensure_ascii=False, separators=(",", ":"))
            f.write(";\n")
    if lista:
        with open(lista, "w", encoding="utf-8") as f:
            f.write("# Wszystkie zdania (wygenerowane przez build_zdania.py – nie edytować ręcznie).\n")
            f.write(f"# Wszystkie mieszczą się w {TALIE} taliach. Znaczniki: [1T] = mieści się nawet w jednej talii,\n")
            f.write("# [D] = ma dwuznak lub zmiękczenie.\n\n")
            for z, zt, dw in dane:
                f.write(f"{z}{'  [1T]' if zt else ''}{'  [D]' if dw else ''}\n")
