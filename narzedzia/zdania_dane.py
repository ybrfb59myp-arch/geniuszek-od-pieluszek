"""Dane do zdań dla aplikacji Geniuszek od Pieluszek (edytuje się ten plik, potem build_zdania.py).

Zdania składają się z PODMIOTU w formie podstawowej (np. „kot”) i pasujących do niego elementów:
  M  – miejsca („na stole”, „pod kocem”),
  C  – czynności z dopełnieniem („pije mleko”),
  V  – czasowniki bez dopełnienia („śpi”, „miauczy”, „bawi się”) wraz z regułą, gdzie to może się dziać,
  A  – przymiotniki („mały”, „rudy”).
Każdy podmiot ma przypisane tylko te elementy, które do niego pasują (kot może być „na szafie”,
krowa już nie) – z nich powstają zdania sensowne. Zdania śmieszne aplikacja układa sama,
łącząc podmiot z elementami, które do niego NIE są przypisane.

Zapis: elementy oddziela się znakiem |, grupę wstawia się pisząc @nazwa.
"""

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


# Zdania, których nie chcemy mimo pasujących grup (np. „babcia u babci”).
WYKLUCZONE_PARY = {("babcia", "u babci"), ("dziadek", "u dziadka"), ("ciocia", "u cioci"), ("wujek", "u wujka"),
                   ("sąsiad", "u sąsiada"), ("sąsiadka", "u sąsiadki"), ("brat", "goni brata"),
                   ("siostra", "goni siostrę"), ("brat", "ma brata"), ("siostra", "ma siostrę"),
                   ("mama", "słucha mamy"), ("mama", "szuka mamy"), ("mama", "przytula mamę"),
                   ("mama", "rysuje mamę"), ("tata", "słucha taty"), ("tata", "szuka taty"),
                   ("tata", "przytula tatę"), ("tata", "rysuje tatę"), ("chłopiec", "ma warkocze"),
                   ("brat", "ma warkocze"), ("synek", "ma warkocze"), ("babcia", "przytula babcię"),
                   ("babcia", "rysuje babcię"), ("dziadek", "rysuje dziadka"), ("dziadek", "budzi dziadka")}


# =============================================================================================
# CZĘŚĆ 2 – dane do zdań z 2–5 wyrazów: nowe podmioty, kategorie, rodzaje, czasowniki, przymiotniki
# =============================================================================================

P += [
    ("deszcz", "w ogrodzie|w lesie|w górach|w mieście|nad morzem|na wsi|za oknem"),
    ("śnieg", "za oknem"),
    ("wiatr", "w lesie|w górach|nad morzem|na polu|za oknem|w ogrodzie"),
    ("rzeka", "w lesie|w górach|w mieście|pod mostem|za domem"),
    ("dom domek", "w lesie|w mieście|na wsi|w górach|nad morzem|nad jeziorem|na wzgórzu|przy drodze|nad rzeką"),
    ("domek", "w ogrodzie|na drzewie"),
    ("stół stolik", "w kuchni|w pokoju|w ogrodzie|na tarasie|w salonie|na balkonie"),
    ("krzesło fotel", "przy stole|w kuchni|w pokoju|na balkonie|w salonie|przy oknie|przy biurku|na tarasie|przy kominku"),
    ("łóżko łóżeczko", "w sypialni|w pokoju|w hotelu"),
    ("kanapa", "w salonie|w pokoju|w domu"),
    ("szafa", "w pokoju|w sypialni|w przedpokoju"),
]

# ---------------------------------------------------------------------------------------------
# KATEGORIE podmiotów – skróty używane niżej jako @nazwa
# ---------------------------------------------------------------------------------------------
KAT = {
    "dorośli": "mama tata babcia dziadek ciocia wujek pani pan sąsiad sąsiadka",
    "dzieci": "dziecko chłopiec dziewczynka brat siostra braciszek siostrzyczka maluch synek córeczka przedszkolak "
              "uczeń uczennica pierwszak",
    "niemowlęta": "niemowlę bobas dzidziuś maluszek",
    "zawody": "lekarz lekarka pielęgniarka weterynarz dentysta strażak policjant policjantka kucharz kucharka piekarz "
              "pilot rolnik nauczyciel nauczycielka listonosz marynarz kierowca taksówkarz sprzedawca ogrodnik rybak "
              "wędkarz kosmonauta astronauta mechanik hydraulik elektryk malarz fryzjer fryzjerka krawiec krawcowa "
              "szwaczka harcerz harcerka turysta alpinista narciarz kolarz rowerzysta tancerz tancerka baletnica "
              "balerina aktor aktorka muzyk piłkarz bramkarz kowboj",
    "bajka": "pirat rycerz król królowa królewna księżniczka książę królewicz czarownica wiedźma czarodziej "
             "czarodziejka magik iluzjonista wróżka krasnal krasnoludek skrzat olbrzym wielkolud klaun pajac syrenka elf",
    "stwory": "smok duch robot kosmita jednorożec dinozaur tyranozaur potwór straszydło mumia troll goblin bałwan bałwanek",
    "koty": "kot kotek kociak koteczek kocur kotka",
    "psy": "pies piesek szczeniak psiak",
    "domowe": "chomik królik króliczek mysz myszka papuga papużka rybka żółw",
    "farma": "krowa krówka byk cielę cielak cielaczek koń konik źrebak źrebię kucyk osioł osiołek koza kózka koziołek "
             "owca owieczka baranek świnia prosiak prosiaczek prosię kura kurka kogut kurczak kurczaczek kaczka "
             "kaczuszka kaczątko kaczor gęś gąska gąsior indyk",
    "leśne": "lis lisek wilk wilczek jeż jeżyk zając zajączek sarna jeleń jelonek łoś dzik niedźwiedź niedźwiadek "
             "wiewiórka borsuk kret bóbr sowa sówka ślimak żaba żabka",
    "owady": "mrówka pszczoła pszczółka osa trzmiel biedronka motyl motylek mucha komar pająk pajączek żuk chrząszcz "
             "ważka świetlik gąsienica robak robaczek dżdżownica świerszcz pasikonik",
    "ptaki": "ptak ptaszek ptaszyna wróbel wróbelek bocian wrona sroka kruk gołąb gołąbek sikorka dzięcioł kukułka "
             "jaskółka orzeł sokół jastrząb łabędź mewa paw pingwin struś flaming pelikan tukan",
    "wodne": "foka delfin rekin wieloryb kaszalot ośmiornica kałamarnica meduza krab rozgwiazda rak ryba łosoś pstrąg "
             "karp szczupak okoń sum węgorz hipopotam krokodyl aligator",
    "egzotyczne": "lew lwica tygrys tygrysek tygrysica słoń żyrafa zebra nosorożec antylopa gepard lampart pantera "
                  "jaguar małpa małpka małpeczka goryl szympans orangutan lemur koala leniwiec panda kangur wielbłąd "
                  "wąż jaszczurka kameleon",
    "pluszaki": "miś misiek misiaczek pluszak lalka laleczka",
    "zabawki": "piłka piłeczka klocki balon balonik latawiec samochodzik autko bączek jojo kostka puzzle kredki kredka "
               "grzechotka sanki narty łyżwy rower rowerek hulajnoga rolki deskorolka huśtawka zjeżdżalnia "
               "piaskownica trampolina karuzela zabawki",
    "naczynia": "łyżka łyżeczka widelec nóż sztućce talerz talerzyk miska miseczka kubek kubeczek szklanka filiżanka "
                "dzbanek garnek patelnia czajnik",
    "pieczywo": "chleb bułka bułeczka rogal rogalik chała pączek drożdżówka precel ciasto ciastko tort sernik "
                "szarlotka piernik pizza",
    "owoce": "jabłko gruszka śliwka banan pomarańcza mandarynka cytryna brzoskwinia jabłuszko morela arbuz melon ananas "
             "kiwi winogrono czereśnia wiśnia truskawka malina jagoda poziomka borówka porzeczka",
    "nabiał": "ser masło szynka kiełbasa parówka jogurt serek jajko jajeczko pisanka",
    "dania": "zupa rosół barszcz kasza makaron ryż gulasz bigos owsianka kisiel budyń kanapka naleśnik kotlet frytki "
             "hamburger pierogi placki",
    "słodycze": "lody cukierek lizak czekolada batonik żelki ciasteczko miód dżem marmolada keczup majonez musztarda",
    "napoje": "mleko sok woda kakao herbata kawa kompot lemoniada oranżada",
    "warzywa": "marchewka marchew ogórek pomidor ziemniak cebula kapusta sałata papryka dynia burak groszek rzodkiewka "
               "kukurydza czosnek",
    "ubrania": "czapka czapeczka szalik kurtka sweter sweterek bluza bluzka koszula koszulka sukienka spódnica "
               "spódniczka płaszcz piżama spodnie spodenki szlafrok kombinezon",
    "dodatki": "buty but bucik buciki kapcie kalosze trampki sandały kozaki botki skarpetka skarpetki rękawiczka "
               "rękawiczki okulary kapelusz parasol parasolka",
    "szkolne": "książka książeczka zeszyt ołówek długopis gumka linijka nożyczki klej kartka kolorowanka pędzel farby "
               "plastelina temperówka plecak piórnik tablica globus mapa",
    "sprzęty": "lampa lampka zegar zegarek obraz obrazek lustro lusterko telefon klucz kluczyk ręcznik mydło szampon "
               "szczoteczka pasta grzebień szczotka poduszka koc kocyk kołdra",
    "meble": "stół stolik krzesło fotel łóżko łóżeczko kanapa szafa dom domek",
    "kwiaty": "kwiat kwiatek kwiaty róża tulipan stokrotka mak słonecznik fiołek bratek konwalia niezapominajka mlecz "
              "dmuchawiec",
    "różne": "świeczka świeca prezent paczka choinka bombka list pocztówka pieniądze moneta pieniążek grosik skarb "
             "korona miotła wiadro wiaderko łopatka grabki foremka",
    "niebo": "słońce księżyc gwiazda gwiazdka chmura chmurka tęcza śnieg mgła deszcz wiatr rzeka",
    "drzewa": "drzewo drzewko krzak krzew brzoza sosna dąb klon świerk jodła lipa wierzba jabłoń grusza buk",
    "znaleziska": "grzyb grzybek liść liście listek kasztan żołądź szyszka orzech kamień kamyk muszla muszelka sopel "
                  "kałuża ogień ognisko",
    "auta": "auto samochód autobus tramwaj taksówka karetka radiowóz motor motocykl skuter ciężarówka wywrotka koparka "
            "dźwig betoniarka walec spychacz traktor ciągnik kombajn",
    "kolej": "pociąg lokomotywa wagon kolejka",
    "łodzie": "łódka łódź jacht żaglówka kajak ponton tratwa statek okręt",
    "samoloty": "samolot helikopter śmigłowiec odrzutowiec szybowiec sterowiec rakieta",
}

# Kto „żyje” – tylko takie podmioty dostają w zdaniach śmiesznych cudze czynności i odgłosy („krowa miauczy”).
ZYWE = "@dorośli @dzieci @niemowlęta @zawody @bajka @stwory @koty @psy @domowe @farma @leśne @owady @ptaki @wodne @egzotyczne @pluszaki"
# Ludzie – w zdaniach śmiesznych dostają tylko „bezpieczne” przymiotniki (kolory itp.).
LUDZIE = "@dorośli @dzieci @niemowlęta @zawody @bajka"

# ---------------------------------------------------------------------------------------------
# RODZAJ GRAMATYCZNY – ustalany z końcówki, poniżej wyjątki
# ---------------------------------------------------------------------------------------------
LICZBA_MNOGA = set("klocki puzzle kredki sanki narty łyżwy rolki zabawki sztućce frytki pierogi placki lody żelki "
                   "spodnie spodenki buty buciki kapcie kalosze trampki sandały kozaki botki skarpetki rękawiczki "
                   "okulary nożyczki farby kwiaty pieniądze grabki liście".split())
RODZAJ_WYJATKI = {
    "m": "tata kierowca sprzedawca kosmonauta astronauta turysta alpinista rowerzysta dentysta iluzjonista kosmita "
         "książę koala",
    "ż": "pani mysz gęś łódź marchew jabłoń żołądź",
    "n": "kiwi",
}

# ---------------------------------------------------------------------------------------------
# PRZYMIOTNIKI – forma męska; żeńską i nijaką skrypt tworzy sam (mały → mała, małe; wysoki → wysoka, wysokie)
# ---------------------------------------------------------------------------------------------
PRZYMIOTNIKI = ("mały duży wielki malutki wysoki długi gruby ciężki lekki "
                "biały czarny czerwony zielony niebieski żółty różowy szary brązowy rudy złoty srebrny kolorowy "
                "pomarańczowy fioletowy nowy stary młody czysty brudny mokry suchy pusty pełny ładny piękny "
                "wesoły smutny zmęczony głodny śpiący zdrowy miły dobry kochany mądry silny odważny grzeczny groźny "
                "dziki zły leniwy ciekawy pracowity cichy głośny szybki wolny puszysty miękki twardy ostry ciepły "
                "zimny gorący smaczny pyszny słodki kwaśny świeży soczysty chrupiący dojrzały okrągły jasny ciemny "
                "pachnący głęboki gęsty").split()
KOLORY = "biały czarny czerwony zielony niebieski żółty różowy szary brązowy rudy złoty srebrny pomarańczowy fioletowy".split()
# Pary, których nie łączymy w „kot jest … i …” (przeciwieństwa i prawie to samo).
ZLE_PARY = ("mały-duży mały-wielki mały-malutki malutki-duży malutki-wielki duży-wielki nowy-stary młody-stary "
            "czysty-brudny pusty-pełny wesoły-smutny szybki-wolny miękki-twardy ciepły-zimny gorący-zimny "
            "ciepły-gorący słodki-kwaśny jasny-ciemny cichy-głośny dobry-zły miły-zły lekki-ciężki mokry-suchy "
            "leniwy-pracowity ładny-piękny smaczny-pyszny grzeczny-zły miły-groźny dobry-groźny miły-dobry "
            "kochany-zły kochany-groźny śpiący-zmęczony złoty-żółty mały-długi mały-wysoki malutki-długi "
            "malutki-wysoki mały-gruby malutki-gruby lekki-gruby duży-długi wielki-długi wielki-wysoki "
            "duży-wysoki duży-gruby wielki-gruby wielki-ciężki mały-ciężki młody-nowy").split()

# ---------------------------------------------------------------------------------------------
# REGUŁY MIEJSC dla czasowników – „kot śpi …”: tylko miejsca z listy, które kot ma też w swoich miejscach
# ---------------------------------------------------------------------------------------------
def _m(**kw):
    """_m(na="stole półce", w="domu") -> {"na stole", "na półce", "w domu"}"""
    return {f"{p} {x}" for p, s in kw.items() for x in s.split()}

_NAD = "domem górami jeziorem kanapą lasem miastem morzem polem rzeką stawem wodą zamkiem łóżkiem łąką"
_POD = ("autem biurkiem choinką drzewem drzwiami fotelem grzybem kamieniem kanapą kocem kołdrą krzakiem krzesłem "
        "liściem mostem parasolem poduszką podłogą samochodem sosną stolikiem stołem szafą wycieraczką ławką łóżkiem")
_U = "babci cioci dziadka wujka sąsiada sąsiadki mamy"

REG = {
    "SPANIE": _m(
        na="dywanie fotelu kanapie kocu krześle łóżku poduszce podłodze parapecie szafie trawie słońcu gałęzi drzewie "
           "plaży piasku kamieniu liściu ławce stole komodzie półce biurku balkonie tarasie strychu łące polanie "
           "skale lodzie krze brzegu dachu",
        w="budzie chatce domku domu dziupli foteliku gnieździe hotelu jaskini kartonie klatce kołysce koszu koszyku "
          "kurniku chlewie kąciku lesie łóżeczku łóżku mchu namiocie norce norze oborze ogrodzie pokoju pudełku "
          "salonie schronisku stajni stodole sypialni szafie szopie trawie wózku zagrodzie zoo krzakach liściach "
          "samochodzie aucie autobusie pociągu wodzie morzu oceanie jeziorze rzece stawie akwarium trzcinie błocie "
          "pałacu wieży zamku szufladzie ziemi kopcu kajucie piramidzie",
        pod="biurkiem drzewem fotelem kanapą kocem kołdrą krzakiem krzesłem liściem łóżkiem stołem stolikiem szafą "
            "grzybem kamieniem mostem sosną parasolem ziemią podłogą",
        przy="kominku piecu ognisku", za="piecem kanapą szafą", u="babci cioci dziadka wujka mamy"),
    "LEŻENIE": _m(
        na="biurku chodniku desce drodze dywanie fotelu kanapie kocu komodzie krześle ławce łóżku parapecie piasku "
           "plaży poduszce podłodze podwórku półce schodach serwetce stole stoliku straganie tacy talerzu trawie "
           "trawniku ulicy umywalce wycieraczce śniegu ścieżce szafie łące słońcu kamieniu brzegu kaloryferze "
           "patelni chlebie bułce kanapce lodzie krze skale balkonie tarasie boisku dachu polu grillu",
        w="błocie budzie kartonie kieszeni koszu koszyku krzakach kufrze lodówce łóżeczku łóżku misce miseczce "
          "ogrodzie piaskownicy piasku piórniku plecaku pokoju przedpokoju pudełku skrzyni skrzynce szafce szafie "
          "szufladzie torbie torebce trawie walizce wózku wiaderku zamrażarce zlewie kałuży kuchni łazience piwnicy "
          "garażu salonie sypialni wannie śniegu słoiku kopercie portfelu skarbonce worku wodzie rzece morzu "
          "jaskini zamku muzeum piramidzie lesie górach parku domu sklepie",
        pod=_POD, przy="drzwiach kominku łóżku oknie ognisku", za="kanapą szafą płotem piecem"),
    "SIEDZENIE": _m(
        na="balkonie brzegu dachu drzewie fotelu gałęzi kamieniu kanapie kocu krześle ławce łóżku murze oknie "
           "parapecie piasku plaży płocie pniu podłodze poduszce dywanie schodach skale stole szafie tarasie trawie "
           "trawniku tronie huśtawce karuzeli koniu kucyku sankach traktorze ramieniu głowie liściu kwiatku kwiecie "
           "róży słoneczniku drucie słupie lianie molo pomniku palcu ręce nosie ścianie suficie szybie lampie "
           "pajęczynie trzcinie łódce łodzi polanie łące sośnie komodzie półce biurku stoliku",
        w="aucie autobusie budzie domku domu dziupli foteliku gnieździe jaskini kabinie kajucie karecie karetce "
          "kartonie kawiarni kinie klasie klatce koszu koszyku krzakach kuchni kąciku łóżeczku łóżku namiocie norce "
          "norze ogrodzie parku piaskownicy pociągu pokoju przedszkolu pudełku radiowozie rakiecie restauracji "
          "salonie samochodzie samolocie szafie szkole taksówce teatrze tramwaju trawie wannie wieży wózku zamku "
          "trzcinie kałuży szufladzie ciężarówce kapeluszu kieszeni sieci szopie stodole bibliotece błocie",
        pod="biurkiem drzewem grzybem kanapą krzakiem krzesłem liściem łóżkiem mostem parasolem sosną stołem "
            "stolikiem szafą kamieniem fotelem",
        przy="biurku kominku ognisku oknie stole łóżku piecu", za="drzewem kanapą piecem płotem szafą kominem",
        u="babci cioci dentysty dziadka fryzjera lekarza mamy sąsiada sąsiadki wujka weterynarza",
        nad="wodą rzeką jeziorem stawem morzem"),
    "STANIE": _m(
        na="balkonie biurku boisku brzegu budowie chodniku dachu drabinie drodze dworcu dywanie górce kamieniu "
           "komodzie kuchence lodzie lotnisku łące moście molo parapecie parkingu placu plaży podłodze podwórku "
           "polanie polu półce przystanku rynku schodach skale skrzyżowaniu stacji stole stoliku tarasie torach "
           "trawie trawniku ulicy wieży wzgórzu śniegu ścieżce pastwisku szczycie górze kominie",
        w="bramce garażu hangarze kuchni kałuży kąciku łazience ogrodzie parku piwnicy pokoju porcie przedpokoju "
          "salonie stajni oborze szafce szopie sypialni wazonie wodzie zagrodzie zajezdni zlewie śniegu lesie domu "
          "doniczce lodówce myjni mieście klasie stawie jeziorze hotelu górach",
        pod="drzewem domem biurkiem ławką parasolem sosną",
        przy="aucie biurku drodze drzwiach kominku kuchence lustrze ognisku oknie piecu skrzynce stole szpitalu "
             "tablicy wannie łóżku",
        przed="domem", za="domem drzewem drzwiami kanapą płotem szafą", nad="rzeką stawem jeziorem morzem wodą"),
    "WISI": _m(
        na="wieszaku ścianie suficie drzewie gałęzi choince krześle lianie pajęczynie dachu rynnie szyi sośnie",
        w="szafie przedpokoju łazience pokoju salonie kuchni klasie szkole muzeum sypialni sieci", nad=_NAD),
    "ZABAWA": _m(
        na="balkonie boisku dywanie kocu łące plaży piasku placu podwórku podłodze polanie tarasie trawie trawniku "
           "śniegu zjeżdżalni trampolinie górce urodzinach wakacjach wsi",
        w="domu ogrodzie parku piaskownicy pokoju przedszkolu lunaparku wodzie basenie kałuży wannie śniegu salonie "
          "namiocie trawie klatce pudełku kartonie morzu",
        pod="stołem drzewem", u="babci cioci dziadka wujka sąsiada sąsiadki", za="domem", przed="domem",
        nad="morzem jeziorem rzeką"),
    "BIEG": _m(
        na="boisku łące plaży placu podwórku polanie polu trawie trawniku śniegu piasku pastwisku prerii sawannie "
           "stadionie górce ścieżce pustyni",
        w="ogrodzie parku lesie zagrodzie klatce kołowrotku kuchni trawie piwnicy stodole spiżarni dżungli górach "
          "śniegu sadzie domu",
        pod="stołem drzewem", za="domem płotem", przed="domem", nad="rzeką jeziorem morzem"),
    "PŁYWANIE": _m(w="wodzie morzu oceanie jeziorze rzece stawie basenie akwarium wannie zatoce",
                   na="basenie stawie jeziorze rzece wodzie morzu", pod="wodą"),
    "NURK": _m(w="wodzie morzu oceanie jeziorze rzece basenie stawie", pod="wodą"),
    "KĄPIEL": _m(w="wodzie morzu jeziorze rzece stawie basenie wannie kałuży błocie piasku", pod="prysznicem",
                 na="basenie"),
    "LOT": _m(na="niebie miotle", nad=_NAD, w="chmurach kosmosie rakiecie"),
    "LATANIE": _m(na="niebie łące polanie", nad=_NAD, w="chmurach pokoju kuchni ogrodzie parku lesie sadzie dżungli"),
    "JAZDA": _m(
        na="autostradzie rowerze koniu kucyku hulajnodze sankach nartach łyżwach rolkach deskorolce traktorze "
           "stoku wyścigu",
        w="tunelu mieście górach autobusie aucie samochodzie pociągu tramwaju taksówce karetce radiowozie "
          "ciężarówce karecie wózku"),
    "PŁYNIĘCIE": _m(na="morzu jeziorze rzece wodzie stawie falach statku łodzi łódce żaglówce niebie",
                    w="zatoce lesie górach mieście", pod="mostem", nad=_NAD, za="domem"),
    "PORT": _m(w="porcie zatoce", na="brzegu plaży"),
    "WZROST": _m(
        w="ogrodzie lesie parku sadzie doniczce szklarni trawie mchu ziemi górach",
        na="balkonie górce łące parapecie polanie polu pniu podwórku trawniku wzgórzu",
        pod="drzewem sosną", przy="drodze", nad="rzeką stawem"),
    "WZROST_OWOCE": _m(na="drzewie gałęzi krzaku", w="ogrodzie sadzie lesie"),
    "WZROST_WARZYWA": _m(w="ogrodzie ziemi szklarni", na="polu"),
    "WZROST_KWIATY": _m(w="ogrodzie doniczce lesie trawie", na="łące parapecie balkonie polu trawniku"),
    "PRACA": _m(
        w="aptece banku bibliotece cukierni cyrku domu fabryce garażu hotelu kawiarni kinie kiosku księgarni kuchni "
          "lesie mieście muzeum ogrodzie piekarni pracowni przedszkolu przychodni restauracji sadzie sklepie stajni "
          "stodole szklarni szkole szpitalu teatrze warsztacie zoo oborze remizie schronisku stołówce lodziarni "
          "porcie kosmosie",
        na="budowie farmie lotnisku poczcie polu statku targu wsi ranczu straganie", przy="biurku"),
    "ROBOTY": _m(na="polu farmie łące wsi budowie drodze placu ulicy", w="piasku lesie"),
    "ODPOCZYNEK": _m(
        na="balkonie fotelu kanapie kocu ławce łóżku plaży tarasie trawie łące wsi wakacjach kempingu polanie piasku",
        w="domu ogrodzie parku górach hotelu lesie namiocie pokoju sadzie łóżku salonie sypialni",
        pod="drzewem parasolem", przy="kominku ognisku", nad="morzem jeziorem rzeką stawem wodą",
        u="babci dziadka cioci wujka"),
    "SPACER": _m(w="parku lesie ogrodzie mieście górach zoo sadzie", na="plaży łące polanie",
                 nad="morzem jeziorem rzeką stawem"),
    "TANIEC": _m(na="balu weselu urodzinach koncercie trawie łące arenie lodzie tęczy",
                 w="pokoju kuchni domu salonie teatrze przedszkolu ogrodzie cyrku zamku pałacu"),
    "ŚPIEW": _m(w="kuchni łazience domu pokoju przedszkolu szkole teatrze ogrodzie lesie wannie orkiestrze aucie "
                  "samochodzie klasie",
                na="koncercie balu weselu urodzinach lekcji biwaku", pod="prysznicem", przy="ognisku kominku"),
    "NAUKA": _m(w="domu pokoju szkole przedszkolu klasie bibliotece łóżku ogrodzie salonie pociągu",
                na="kanapie fotelu łóżku dywanie podłodze balkonie tarasie ławce lekcji kocu",
                przy="biurku stole oknie tablicy kominku", u="babci cioci dziadka wujka",
                pod="drzewem kołdrą kocem parasolem"),
    "KUCHNIA": _m(w="kuchni domu restauracji stołówce piekarni", na="kempingu biwaku", przy="kuchence piecu ognisku",
                  u="babci"),
    "SPRZĄTANIE": _m(w="domu pokoju kuchni łazience garażu piwnicy przedpokoju salonie sypialni ogrodzie hotelu",
                     na="strychu balkonie tarasie podwórku", u="babci cioci dziadka wujka"),
    "ŁAZIENKA": _m(w="łazience wannie domu pokoju przedpokoju sypialni", pod="prysznicem", przy="lustrze"),
    "KRYJÓWKA": _m(
        pod=_POD + " wodą ziemią", za="chmurą domem drzewem drzwiami kanapą kominem piecem płotem szafą",
        w="szafie krzakach norze norce budzie pudełku kartonie koszu koszyku trawie jaskini dziupli lesie namiocie "
          "liściach piasku szufladzie kąciku piwnicy stodole trzcinie mchu ziemi kopcu skrzyni błocie domku",
        na="drzewie strychu szafie"),
    "HUŚTANIE": _m(na="huśtawce gałęzi lianie drzewie placu", w="ogrodzie parku"),
    "ŚLIZG": _m(na="lodzie lodowisku śniegu górce zjeżdżalni krze stoku"),
    "PASTWISKO": _m(na="łące pastwisku polu polanie farmie górce wsi sawannie prerii", w="zagrodzie górach"),
    "SUSZENIE": _m(na="kaloryferze krześle balkonie wieszaku słońcu tarasie", w="łazience przedpokoju"),
    "GAR": _m(w="garnku kuchni czajniku", na="kuchence"),
    "PIEC": _m(w="piekarniku kuchni piekarni piecu", na="grillu"),
    "PATELNIA": _m(na="patelni", w="kuchni"),
    "STYG": _m(na="stole talerzu tacy", w="kubku filiżance misce miseczce garnku kuchni kubeczku"),
    "NAD": _m(nad=_NAD),
    "LOTNISKO": _m(na="lotnisku księżycu dachu planecie łące wodzie", w="ogrodzie lesie"),
    "KOPANIE": _m(w="ziemi ogrodzie piasku piaskownicy", na="budowie plaży podwórku wyspie", pod="ziemią drzewem"),
    "PEŁZ": _m(w="trawie ogrodzie lesie ziemi", pod="liściem kamieniem"),
    "RACZKI": _m(na="dywanie podłodze kocu trawie", w="pokoju domu ogrodzie salonie"),
    "JEDZENIE": _m(
        w="kuchni domu ogrodzie kurniku chlewie oborze stajni zagrodzie klatce lesie trawie zoo restauracji kawiarni "
          "stołówce przedszkolu szkole stodole",
        na="łące pastwisku podwórku farmie polu polanie trawie parapecie balkonie tarasie drzewie gałęzi liściu "
           "sawannie kempingu",
        przy="stole ognisku", pod="drzewem stołem", u="babci cioci dziadka wujka"),
    "CZEKANIE": _m(
        na="przystanku dworcu stacji lotnisku ławce ulicy moście schodach balkonie poczcie parkingu wieży",
        w="aucie samochodzie domu kuchni parku szkole przedszkolu sklepie kawiarni restauracji autobusie pokoju "
          "przedpokoju ogrodzie wieży zamku budzie",
        u="lekarza dentysty fryzjera weterynarza babci cioci dziadka wujka", przy="drzwiach oknie stole łóżku aucie",
        przed="domem", pod="drzewem domem parasolem drzwiami", za="drzwiami domem płotem"),
    "MIESZKANIE": _m(
        w="lesie chatce wieży zamku jaskini domu domku norze norce budzie dziupli gnieździe pałacu ogrodzie mieście "
          "górach morzu oceanie jeziorze rzece stawie wodzie akwarium klatce stajni oborze chlewie kurniku zagrodzie "
          "zoo dżungli mrowisku ulu ziemi trawie bajce kosmosie kopcu mchu zegarze",
        na="wsi farmie drzewie strychu wyspie księżycu planecie sawannie pustyni łące",
        pod="ziemią mostem grzybem podłogą wodą łóżkiem kamieniem liściem", za="piecem",
        nad="morzem rzeką jeziorem stawem"),
    "POLOWANIE": _m(
        w="lesie dżungli trawie wodzie morzu oceanie rzece jeziorze górach krzakach kurniku stodole piwnicy "
          "ogrodzie sieci",
        na="łące polu sawannie polanie pustyni strychu śniegu podwórku pajęczynie", nad=_NAD, pod="wodą"),
    "ULICA": _m(
        na="ulicy drodze moście skrzyżowaniu autostradzie parkingu przystanku stacji dworcu torach",
        w="mieście tunelu górach", pod="domem", przed="domem"),
    "OPAD": _m(w="ogrodzie górach lesie mieście parku", nad=_NAD, za="oknem", na="wsi"),
}

# Reguła, gdy przy czasowniku nie podano innej. Czasowniki spoza tej listy: dowolne miejsce podmiotu („*”).
DOMYSLNA = {
    "śpi": "SPANIE", "chrapie": "SPANIE", "leży": "LEŻENIE", "siedzi": "SIEDZENIE", "stoi": "STANIE", "wisi": "WISI",
    "bawi się": "ZABAWA", "biega": "BIEG", "skacze": "BIEG", "galopuje": "BIEG", "kica": "BIEG",
    "pływa": "PŁYWANIE", "nurkuje": "NURK", "kąpie się": "KĄPIEL", "leci": "LOT", "krąży": "LOT",
    "lata": "LATANIE", "fruwa": "LATANIE", "jedzie": "JAZDA", "pędzi": "JAZDA", "płynie": "PŁYNIĘCIE",
    "kołysze się": "PŁYNIĘCIE", "rośnie": "WZROST", "kwitnie": "WZROST", "dojrzewa": "WZROST_OWOCE",
    "pracuje": "PRACA", "odpoczywa": "ODPOCZYNEK", "spaceruje": "SPACER", "tańczy": "TANIEC", "śpiewa": "ŚPIEW",
    "czyta": "NAUKA", "pisze": "NAUKA", "rysuje": "NAUKA", "maluje": "NAUKA", "liczy": "NAUKA",
    "gotuje": "KUCHNIA", "piecze": "KUCHNIA", "sprząta": "SPRZĄTANIE", "myje się": "ŁAZIENKA",
    "czesze się": "ŁAZIENKA", "ubiera się": "ŁAZIENKA", "chowa się": "KRYJÓWKA", "huśta się": "HUŚTANIE",
    "ślizga się": "ŚLIZG", "pasie się": "PASTWISKO", "schnie": "SUSZENIE", "gotuje się": "GAR",
    "piecze się": "PIEC", "smaży się": "PATELNIA", "stygnie": "STYG", "wschodzi": "NAD", "zachodzi": "NAD",
    "startuje": "LOTNISKO", "ląduje": "LOTNISKO", "kopie": "KOPANIE", "pełznie": "PEŁZ", "raczkuje": "RACZKI",
    "je": "JEDZENIE", "pije": "JEDZENIE", "czeka": "CZEKANIE", "mieszka": "MIESZKANIE", "poluje": "POLOWANIE",
    "pada": "OPAD", "trąbi": "ULICA", "dzwoni": "*", "idzie": "-", "ucieka": "-", "spada": "-", "pęka": "-",
    "ziewa": "EMOCJE", "śmieje się": "EMOCJE", "cieszy się": "EMOCJE", "płacze": "EMOCJE", "kipi": "-",
}
REG["EMOCJE"] = REG["SIEDZENIE"] | REG["ZABAWA"] | REG["CZEKANIE"]

# Czasowniki, które bez miejsca brzmią niepełnie („kot mieszka”) – używane tylko razem z miejscem.
WYMAGA_MIEJSCA = {"mieszka"}

# Przymiotnik + czasownik, które do siebie nie pasują („wesołe dziecko płacze”). Spacja w czasowniku jako _.
ZLE_AV = ("wesoły-płacze smutny-śmieje_się smutny-cieszy_się śpiący-biega śpiący-skacze śpiący-tańczy "
          "śpiący-galopuje śpiący-kica śpiący-pędzi śpiący-bawi_się zimny-stygnie zimny-gotuje_się zimny-grzeje "
          "zimny-pali_się zimny-płonie suchy-schnie cichy-ryczy cichy-krzyczy cichy-szczeka cichy-trąbi "
          "cichy-warczy cichy-piszczy wolny-pędzi wolny-biega wolny-galopuje głodny-je zdrowy-kipi "
          "nowy-topnieje stary-rośnie").split()

# ---------------------------------------------------------------------------------------------
# CZASOWNIKI bez dopełnienia: (podmioty, czasowniki). „czasownik:REGUŁA” nadpisuje regułę, „:-” = bez miejsca,
# „:*” = każde miejsce podmiotu.
# ---------------------------------------------------------------------------------------------
PV = [
    # --- ludzie ---
    ("@dorośli", "śpi|je|pije|czyta|pisze|gotuje|sprząta|pracuje|odpoczywa|śpiewa|tańczy|biega|pływa|siedzi|stoi|"
                 "czeka|spaceruje|jedzie|leży|ziewa|śmieje się|cieszy się|kąpie się|myje się|czesze się|ubiera się"),
    ("tata dziadek wujek", "chrapie"),
    ("@dzieci", "śpi|je|pije|czyta|pisze|rysuje|maluje|śpiewa|tańczy|biega|skacze|pływa|siedzi|stoi|leży|płacze|"
                "śmieje się|cieszy się|bawi się|kąpie się|myje się|czesze się|ubiera się|huśta się|chowa się|"
                "ślizga się|ziewa|czeka|jedzie|rośnie:-|liczy"),
    ("@niemowlęta", "śpi|je:-|pije:-|płacze|śmieje się|raczkuje|leży|ziewa|bawi się|rośnie:-|kąpie się"),
    ("lekarz lekarka pielęgniarka weterynarz dentysta", "pracuje:*|odpoczywa:-"),
    ("strażak", "pracuje:*|jedzie:-|odpoczywa:-"),
    ("policjant policjantka", "pracuje:*|stoi|jedzie|czeka"),
    ("kucharz kucharka", "gotuje|piecze|pracuje:*|miesza:-"),
    ("piekarz", "piecze|pracuje:*"),
    ("pilot", "leci|ląduje|startuje|pracuje:-"),
    ("rolnik", "pracuje:*|orze:-|sieje:-|jedzie|odpoczywa"),
    ("nauczyciel nauczycielka", "uczy|czyta|pisze|pracuje:*|śpiewa"),
    ("listonosz", "jedzie|idzie|pracuje:*"),
    ("marynarz", "płynie|pracuje:*|śpiewa:-|odpoczywa:-"),
    ("kierowca taksówkarz", "jedzie|czeka|pracuje:-|trąbi:-"),
    ("sprzedawca", "pracuje:*|sprzedaje:-|liczy:-"),
    ("ogrodnik", "pracuje:*|kopie|odpoczywa|sadzi:-|podlewa:-"),
    ("rybak wędkarz", "łowi|siedzi|czeka:*|płynie|odpoczywa"),
    ("kosmonauta astronauta", "leci|ląduje|pracuje:*|śpi:-"),
    ("mechanik hydraulik elektryk", "pracuje:*|naprawia:-"),
    ("malarz", "maluje:*|pracuje:*"),
    ("fryzjer fryzjerka", "pracuje:*|czesze:-|strzyże:-"),
    ("krawiec krawcowa szwaczka", "szyje:-|pracuje:-"),
    ("harcerz harcerka", "śpiewa|idzie|maszeruje:-|śpi|odpoczywa"),
    ("turysta", "idzie|odpoczywa|śpi|zwiedza:-|czeka"),
    ("alpinista", "odpoczywa:-|stoi|idzie"),
    ("narciarz", "jedzie|zjeżdża:-|skacze:-"),
    ("kolarz rowerzysta", "jedzie|pędzi|odpoczywa:-"),
    ("tancerz tancerka baletnica balerina", "tańczy|ćwiczy:-|skacze:-"),
    ("aktor aktorka", "gra|śpiewa:-|tańczy:-"),
    ("muzyk", "gra|śpiewa"),
    ("piłkarz", "gra|biega|strzela:-"),
    ("bramkarz", "stoi|broni:-|skacze:-"),
    ("kowboj", "jedzie|śpi:-|śpiewa"),
    # --- bajka ---
    ("pirat", "płynie|śpiewa:-|kopie|śpi"),
    ("rycerz", "walczy:-|jedzie|stoi|czuwa:-"),
    ("król królowa", "rządzi:-|śpi|siedzi|tańczy|odpoczywa"),
    ("królewna księżniczka", "śpi|tańczy|śpiewa|płacze|czeka|siedzi|czesze się:-|śmieje się"),
    ("książę królewicz", "jedzie|tańczy|śpi|czeka|śpiewa"),
    ("czarownica wiedźma czarodziej czarodziejka", "czaruje|leci|śpi|mieszka|gotuje:-"),
    ("magik iluzjonista", "czaruje"),
    ("wróżka", "czaruje|leci|tańczy|śpiewa:-|mieszka"),
    ("krasnal krasnoludek skrzat", "pracuje:-|śpi|śpiewa:-|mieszka|chowa się"),
    ("smok", "leci|śpi|ryczy|mieszka"),
    ("duch", "straszy|mieszka|leci:-|chowa się"),
    ("olbrzym wielkolud", "śpi|chrapie|mieszka|je:-|idzie"),
    ("klaun pajac", "tańczy|skacze:*|śmieje się|śpiewa:-|żongluje"),
    ("robot", "pracuje|sprząta|tańczy|jedzie:-|stoi|liczy:-"),
    ("kosmita", "leci|ląduje|mieszka|śpi:-"),
    ("syrenka", "pływa|śpiewa:*|mieszka|siedzi|czesze się:-"),
    ("jednorożec", "biega|skacze|galopuje|mieszka|śpi"),
    ("dinozaur tyranozaur", "ryczy|biega|śpi|je:-|mieszka|poluje"),
    ("potwór straszydło", "ryczy|straszy|śpi|mieszka|chowa się"),
    ("mumia", "śpi|leży|straszy"),
    ("troll", "śpi|mieszka|je:-|ryczy"),
    ("elf goblin", "śpiewa:-|tańczy:-|pracuje:-|mieszka|chowa się|śpi"),
    ("bałwan bałwanek", "stoi|topnieje|śmieje się:-"),
    # --- zwierzęta domowe ---
    ("@koty", "śpi|je|pije|miauczy|mruczy|biega|skacze|bawi się|myje się:*|chowa się|leży|siedzi|ziewa|poluje|czeka"),
    ("@psy", "śpi|je|pije|szczeka|warczy|biega|skacze|bawi się|leży|siedzi|pływa|kopie|wyje|czeka|chowa się|ziewa"),
    ("chomik", "śpi|je|biega|chowa się|mieszka"),
    ("królik króliczek", "śpi|je|skacze|kica|biega|chowa się|mieszka|siedzi"),
    ("mysz myszka", "śpi|je|piszczy|biega|chowa się|ucieka|mieszka|siedzi"),
    ("papuga papużka", "śpi|je|lata|leci:-|śpiewa:*|gada|skrzeczy|mieszka|siedzi"),
    ("rybka", "pływa|je:-|mieszka|śpi:-"),
    ("żółw", "śpi|je|pływa|idzie|chowa się|mieszka|leży"),
    # --- farma ---
    ("krowa krówka", "muczy|ryczy|je|pije|śpi|stoi|leży|pasie się|mieszka"),
    ("byk cielę cielak cielaczek", "je|pije|śpi|stoi|leży|biega|pasie się|skacze"),
    ("byk", "ryczy"), ("cielę cielak cielaczek", "muczy"),
    ("koń konik źrebak źrebię kucyk", "rży|biega|galopuje|skacze|je|pije|śpi|stoi|pasie się|mieszka"),
    ("osioł osiołek", "ryczy|stoi|je|pije|śpi|idzie|pasie się"),
    ("koza kózka koziołek", "beczy|meczy|skacze|je|pije|biega|pasie się|śpi|stoi"),
    ("owca owieczka baranek", "beczy|je|pije|śpi|pasie się|stoi|biega|leży"),
    ("świnia prosiak prosiaczek prosię", "chrumka|kwiczy|je|pije|śpi|leży|mieszka|kąpie się|biega"),
    ("kura kurka", "gdacze|je|śpi|biega|siedzi|mieszka"),
    ("kogut", "pieje|je|biega|stoi|śpi|siedzi"),
    ("kurczak kurczaczek", "piszczy|je|biega|śpi"),
    ("kaczka kaczuszka kaczątko kaczor", "kwacze|pływa|je|śpi|nurkuje|leci:-|kąpie się"),
    ("gęś gąska gąsior", "gęga|syczy|je|pływa|biega|śpi|pasie się"),
    ("indyk", "gulgocze|je|biega|śpi|stoi"),
    # --- leśne ---
    ("lis lisek", "biega|śpi|poluje|chowa się|je|mieszka|ucieka"),
    ("wilk wilczek", "wyje|biega|poluje|śpi|je|mieszka|warczy"),
    ("jeż jeżyk", "śpi|je|tupie|chowa się|mieszka|idzie"),
    ("zając zajączek", "skacze|kica|biega|ucieka|je|śpi|chowa się|mieszka"),
    ("sarna jeleń jelonek łoś", "biega|skacze|je|pije|śpi|stoi|pasie się|ucieka|mieszka"),
    ("dzik", "biega|je|śpi|chrumka|mieszka|kąpie się"),
    ("niedźwiedź niedźwiadek", "ryczy|śpi|je|biega|pływa|mieszka|poluje|chrapie"),
    ("miś", "śpi|leży|siedzi"),
    ("wiewiórka", "skacze:*|biega|je|śpi|chowa się|mieszka|siedzi"),
    ("borsuk", "śpi|je:-|kopie|mieszka"), ("kret", "kopie|śpi|mieszka"),
    ("bóbr", "pływa|pracuje:-|mieszka|nurkuje|buduje:-|śpi"),
    ("sowa sówka", "huka|leci:-|lata|śpi|poluje|siedzi|mieszka"),
    ("ślimak", "pełznie|śpi|je|chowa się|mieszka|idzie"),
    ("żaba żabka", "kumka|rechocze|skacze:*|pływa|je:-|śpi|siedzi|mieszka|nurkuje"),
    # --- owady ---
    ("mrówka", "pracuje:-|idzie|biega|je:-|mieszka"),
    ("pszczoła pszczółka", "bzyczy|lata|leci:-|pracuje:-|mieszka|siedzi"),
    ("osa trzmiel", "bzyczy|lata|leci:-|siedzi"),
    ("biedronka", "leci:-|lata|idzie|śpi|siedzi|mieszka"),
    ("motyl motylek", "leci:-|lata|fruwa|siedzi|tańczy:-|śpi"),
    ("mucha", "bzyczy|lata|leci:-|siedzi"),
    ("komar", "bzyczy|lata|leci:-|gryzie:-|siedzi"),
    ("pająk pajączek", "wisi|czeka:*|śpi|siedzi|mieszka|pracuje:-|poluje"),
    ("żuk chrząszcz", "idzie|leci:-|bzyczy|mieszka|śpi"),
    ("ważka", "leci:-|lata|siedzi|poluje"),
    ("świetlik", "świeci|leci:-|lata"),
    ("gąsienica", "pełznie|je|śpi|mieszka"), ("robak robaczek dżdżownica", "pełznie|mieszka|je:-|chowa się"),
    ("świerszcz", "gra|cyka|skacze|mieszka"), ("pasikonik", "skacze|gra|siedzi|mieszka"),
    # --- ptaki ---
    ("ptak ptaszek ptaszyna", "śpiewa:*|leci:-|lata|fruwa|ćwierka|je|śpi|siedzi|mieszka"),
    ("wróbel wróbelek", "ćwierka|leci:-|lata|skacze:*|je|siedzi|kąpie się"),
    ("bocian", "klekocze|leci|stoi|je|mieszka|śpi"),
    ("wrona kruk", "kracze|leci:-|lata|siedzi|je"), ("sroka", "skrzeczy|leci:-|lata|siedzi|kradnie:-"),
    ("gołąb gołąbek", "grucha|leci:-|lata|je|siedzi|mieszka"),
    ("sikorka", "śpiewa:*|ćwierka|leci:-|lata|je|siedzi"),
    ("dzięcioł", "stuka|leci:-|pracuje:-|mieszka|siedzi"),
    ("kukułka", "kuka|leci:-|lata|siedzi|mieszka"),
    ("jaskółka", "leci|lata|ćwierka|mieszka|śpiewa:*"),
    ("orzeł sokół jastrząb", "leci|lata|krąży|poluje|siedzi|mieszka"),
    ("łabędź", "pływa|leci:-|syczy|śpi|je:-"),
    ("mewa", "leci|lata|krzyczy|pływa|je:-|siedzi"),
    ("paw", "krzyczy|stoi|spaceruje|je:-"),
    ("pingwin", "pływa|idzie|stoi|je:-|ślizga się|nurkuje|mieszka"),
    ("struś", "biega|je:-|stoi|mieszka|ucieka"),
    ("flaming", "stoi|śpi|je:-|mieszka"), ("pelikan", "leci|pływa|je:-|łowi"), ("tukan", "leci:-|lata|je:-|siedzi|mieszka"),
    # --- wodne ---
    ("foka", "pływa|śpi|je:-|leży|szczeka|nurkuje|bawi się|mieszka"),
    ("delfin", "pływa|skacze:*|bawi się|nurkuje|mieszka"),
    ("rekin", "pływa|poluje|je:-|mieszka"), ("wieloryb kaszalot", "pływa|nurkuje|śpi|mieszka|śpiewa:-"),
    ("ośmiornica kałamarnica meduza", "pływa|mieszka|chowa się"),
    ("krab rak", "idzie|chowa się|mieszka|szczypie:-"), ("rozgwiazda", "leży|mieszka"),
    ("ryba łosoś pstrąg karp szczupak okoń sum węgorz", "pływa|mieszka|je:-|skacze:-"),
    ("hipopotam", "pływa|śpi|je:-|ziewa|kąpie się|leży|mieszka|nurkuje"),
    ("krokodyl aligator", "pływa|śpi|leży|czeka:*|poluje|mieszka|je:-"),
    # --- egzotyczne ---
    ("lew lwica", "ryczy|śpi|poluje|je:-|leży|biega|ziewa|mieszka|odpoczywa:-"),
    ("tygrys tygrysek tygrysica", "ryczy|poluje|biega|śpi|pływa|skacze|mieszka|leży"),
    ("słoń", "trąbi:*|idzie|je|pije|kąpie się|śpi|stoi|mieszka"),
    ("żyrafa", "je|stoi|idzie|biega|pije|śpi|mieszka"),
    ("zebra", "biega|je|pije|stoi|ucieka|pasie się|mieszka"),
    ("nosorożec", "biega|je|śpi|stoi|kąpie się|mieszka"),
    ("antylopa", "biega|skacze|ucieka|je|pasie się|mieszka"), ("gepard", "biega|poluje|śpi|mieszka|leży"),
    ("lampart pantera jaguar", "poluje|śpi|skacze:*|biega|ryczy|mieszka|leży"),
    ("małpa małpka małpeczka", "skacze:*|je|bawi się:*|huśta się|krzyczy|śpi|mieszka|siedzi"),
    ("goryl szympans orangutan", "je|śpi|siedzi|bawi się:*|mieszka|ryczy"),
    ("lemur koala leniwiec", "śpi|je|siedzi|mieszka"), ("leniwiec", "wisi|ziewa"),
    ("panda", "je|śpi|siedzi|bawi się:*|mieszka"), ("kangur", "skacze|je|biega|śpi|mieszka"),
    ("wielbłąd", "idzie|pije|je|stoi|śpi|mieszka|odpoczywa:-"),
    ("wąż", "syczy|pełznie|śpi|poluje|chowa się|mieszka|leży"),
    ("jaszczurka", "biega|śpi|ucieka|chowa się|leży|mieszka"), ("kameleon", "siedzi|śpi|poluje|mieszka|idzie"),
    # --- zabawki i rzeczy ---
    ("misiek misiaczek pluszak lalka laleczka", "leży|siedzi|śpi"),
    ("piłka piłeczka", "leży|leci:-|skacze:-|pływa"),
    ("balon balonik", "leci|pęka|wisi"), ("latawiec", "leci|fruwa|wisi"),
    ("samochodzik autko", "jedzie:-|stoi|leży"), ("bączek", "kręci się|leży"), ("jojo kostka kredka grzechotka", "leży"),
    ("rower rowerek hulajnoga deskorolka", "stoi|leży|jedzie:-"),
    ("huśtawka zjeżdżalnia piaskownica trampolina", "stoi"), ("karuzela", "kręci się|stoi|gra:-"),
    ("łyżka łyżeczka widelec nóż", "leży"),
    ("talerz talerzyk miska miseczka kubek kubeczek szklanka filiżanka dzbanek", "stoi|leży"),
    ("garnek patelnia czajnik", "stoi"), ("czajnik", "gwiżdże:GAR"),
    ("stół stolik krzesło fotel łóżko łóżeczko kanapa szafa", "stoi:*"), ("dom domek", "stoi:*"),
    # --- jedzenie ---
    ("chleb bułka bułeczka rogal rogalik chała pączek drożdżówka precel ciasto ciastko tort sernik szarlotka piernik pizza",
     "leży|pachnie"),
    ("chleb ciasto pizza sernik szarlotka piernik", "piecze się"), ("ciasto", "rośnie:-"),
    ("chleb bułka pączek pizza ciasto", "stygnie"),
    ("@owoce", "leży|rośnie:WZROST_OWOCE|dojrzewa|pachnie:-"),
    ("jabłko gruszka śliwka jabłuszko czereśnia wiśnia brzoskwinia morela", "wisi|spada"),
    ("ser masło szynka kiełbasa parówka jogurt serek jajko jajeczko pisanka", "leży"), ("kiełbasa", "piecze się"),
    ("zupa rosół barszcz kasza makaron ryż gulasz bigos owsianka kisiel budyń", "gotuje się|stygnie|pachnie:-"),
    ("kanapka naleśnik kotlet hamburger", "leży"), ("kotlet naleśnik", "smaży się"),
    ("cukierek lizak czekolada batonik ciasteczko", "leży"),
    ("mleko sok woda kakao herbata kawa kompot lemoniada oranżada", "stoi"),
    ("mleko kakao herbata kawa kompot", "stygnie"), ("woda mleko", "gotuje się"), ("mleko", "kipi"),
    ("@warzywa", "rośnie:WZROST_WARZYWA|leży"),
    # --- ubrania, szkoła, dom ---
    ("czapka czapeczka szalik kurtka sweter sweterek bluza bluzka koszula koszulka sukienka spódnica spódniczka płaszcz "
     "piżama szlafrok kombinezon", "wisi|leży|schnie"),
    ("but bucik skarpetka rękawiczka", "leży|schnie"), ("kapelusz", "leży|wisi"),
    ("parasol parasolka", "stoi|leży|wisi|schnie"),
    ("książka książeczka zeszyt ołówek długopis gumka linijka klej kartka kolorowanka pędzel plastelina temperówka "
     "piórnik", "leży"),
    ("plecak", "stoi|leży|wisi"), ("tablica", "wisi"), ("globus", "stoi"), ("mapa", "wisi|leży"),
    ("lampa lampka", "świeci|stoi"), ("lampa", "wisi"),
    ("zegar", "tyka|wisi|stoi|bije:-"), ("zegarek", "tyka|leży"), ("obraz obrazek lustro", "wisi"), ("lusterko", "leży"),
    ("telefon", "dzwoni|leży"), ("klucz kluczyk", "leży|wisi"), ("ręcznik", "wisi|schnie|leży"),
    ("mydło szampon szczoteczka pasta grzebień szczotka", "leży"), ("poduszka koc kocyk kołdra", "leży"),
    ("kwiat kwiatek róża tulipan stokrotka mak słonecznik fiołek bratek konwalia niezapominajka mlecz dmuchawiec",
     "rośnie:WZROST_KWIATY|kwitnie:WZROST_KWIATY|pachnie"),
    ("kwiat kwiatek róża tulipan", "stoi"),
    ("świeczka świeca", "świeci|pali się|płonie|stoi"),
    ("prezent paczka", "leży|czeka:*"), ("choinka", "stoi|świeci|pachnie|rośnie"),
    ("bombka", "wisi|błyszczy"), ("list pocztówka", "leży"), ("moneta pieniążek grosik", "leży|błyszczy"),
    ("skarb", "leży|błyszczy|czeka:*"), ("korona", "leży|błyszczy"), ("miotła", "stoi|leży"),
    ("wiadro wiaderko", "stoi|leży"), ("łopatka foremka", "leży"),
    # --- przyroda ---
    ("słońce", "świeci|grzeje|wschodzi|zachodzi|chowa się"), ("księżyc", "świeci|wschodzi|chowa się"),
    ("gwiazda gwiazdka", "świeci|błyszczy|spada|mruga:-"), ("chmura chmurka", "płynie|wisi"),
    ("tęcza", "błyszczy"), ("śnieg", "pada|leży|topnieje|skrzypi:-"), ("mgła", "wisi:*|opada:-"),
    ("deszcz", "pada|kapie:-|szumi:-"), ("wiatr", "wieje|szumi|gwiżdże:-"), ("rzeka", "płynie:*|szumi"),
    ("@drzewa", "rośnie|stoi|szumi"), ("jabłoń grusza lipa", "kwitnie"),
    ("grzyb grzybek", "rośnie"), ("liść listek", "leci:-|spada|leży|wisi|płynie"),
    ("kasztan żołądź szyszka orzech", "leży|spada|wisi"), ("kamień kamyk muszla muszelka", "leży"),
    ("sopel", "wisi|topnieje|spada"), ("ogień", "pali się|płonie|grzeje"), ("ognisko", "pali się|płonie|grzeje|dymi:-"),
    # --- pojazdy ---
    ("auto samochód", "jedzie|stoi|trąbi|pędzi"), ("autobus tramwaj taksówka", "jedzie|stoi|czeka:*"),
    ("tramwaj", "dzwoni:ULICA"), ("autobus", "trąbi"),
    ("karetka radiowóz", "jedzie|pędzi|stoi|wyje:ULICA"), ("motor motocykl skuter", "jedzie|stoi|warczy:ULICA|pędzi"),
    ("ciężarówka wywrotka", "jedzie|stoi|trąbi"), ("koparka", "kopie:*|pracuje:ROBOTY|stoi|jedzie:-"),
    ("dźwig betoniarka walec spychacz", "pracuje:ROBOTY|stoi|jedzie:-"),
    ("traktor ciągnik kombajn", "jedzie|pracuje:ROBOTY|stoi|warczy:ROBOTY"),
    ("pociąg lokomotywa wagon kolejka", "jedzie|stoi|pędzi"), ("pociąg lokomotywa", "gwiżdże|sapie"),
    ("łódka łódź jacht żaglówka kajak ponton tratwa statek okręt", "płynie|stoi:PORT|kołysze się"),
    ("statek okręt", "trąbi:-"),
    ("samolot helikopter śmigłowiec odrzutowiec szybowiec sterowiec", "leci|ląduje|startuje|stoi"),
    ("rakieta", "leci|startuje:-|ląduje"),
]

# ---------------------------------------------------------------------------------------------
# PRZYMIOTNIKI pasujące do podmiotów: (podmioty, przymiotniki w formie męskiej)
# ---------------------------------------------------------------------------------------------
PA = [
    ("@dorośli", "miły dobry kochany wesoły zmęczony głodny wysoki mądry zdrowy smutny śpiący silny"),
    ("@dzieci", "mały wesoły grzeczny głodny śpiący zmęczony smutny miły kochany mądry zdrowy ciekawy duży silny odważny"),
    ("@niemowlęta", "mały malutki wesoły głodny śpiący kochany zdrowy grzeczny"),
    ("@zawody", "miły dobry wesoły mądry zmęczony młody silny"),
    ("strażak policjant policjantka pilot kosmonauta astronauta alpinista kowboj marynarz", "odważny"),
    ("piłkarz bramkarz narciarz kolarz rowerzysta tancerz tancerka", "szybki"),
    ("pirat", "groźny stary odważny zły wesoły"), ("rycerz książę królewicz", "odważny młody silny dobry mądry"),
    ("król królowa", "dobry mądry stary wesoły smutny"),
    ("królewna księżniczka", "piękny młody dobry smutny wesoły mądry śpiący"),
    ("czarownica wiedźma", "zły stary groźny mądry"), ("czarodziej czarodziejka magik iluzjonista", "mądry stary dobry"),
    ("wróżka", "dobry piękny mały miły"), ("krasnal krasnoludek skrzat elf", "mały wesoły pracowity stary miły malutki"),
    ("olbrzym wielkolud", "wielki groźny silny głodny śpiący dobry"), ("klaun pajac", "wesoły smutny kolorowy"),
    ("syrenka", "piękny mały smutny wesoły"),
    ("smok", "wielki groźny zły zielony stary głodny śpiący"), ("duch", "biały stary cichy smutny mały"),
    ("robot", "mały duży nowy stary mądry silny"), ("kosmita", "zielony mały mądry miły"),
    ("jednorożec", "biały piękny różowy mały"), ("dinozaur tyranozaur", "wielki groźny zielony głodny stary"),
    ("potwór straszydło troll goblin", "groźny zły wielki zielony głodny"), ("mumia", "stary"),
    ("bałwan bałwanek", "biały wielki mały zimny wesoły gruby"),
    # zwierzęta
    ("@koty @psy @domowe @farma @leśne @ptaki @wodne @egzotyczne", "mały duży głodny śpiący młody stary zdrowy"),
    ("@owady", "mały malutki głodny"),
    ("@koty @psy królik króliczek chomik papuga papużka konik kucyk osiołek owieczka baranek prosiaczek kurczaczek "
     "kaczuszka delfin foka małpka", "wesoły miły kochany"),
    ("@koty królik króliczek chomik owca owieczka baranek lis lisek wiewiórka miś niedźwiadek panda koala kurczak "
     "kurczaczek kaczątko piesek szczeniak zając zajączek", "puszysty"),
    ("koń konik zając gepard pies jaskółka sokół struś antylopa lew tygrys delfin rekin jeleń sarna lis mysz jaszczurka "
     "zebra kangur orzeł wilk", "szybki"),
    ("ślimak żółw leniwiec", "wolny"),
    ("lew lwica tygrys tygrysica wilk niedźwiedź rekin krokodyl aligator wąż pantera lampart jaguar dzik byk goryl",
     "groźny dziki silny"),
    ("lis zając sarna jeleń koń", "dziki"),
    ("kot kotek kotka pies piesek królik króliczek koń konik owca owieczka baranek gęś gąska łabędź niedźwiedź kura mysz "
     "myszka koza kózka gołąb gołąbek bocian miś mewa", "biały"),
    ("kot kotek kocur kotka pies piesek koń kruk wrona pantera kret owca byk żuk pająk kura", "czarny"),
    ("kot kotek kotka mysz myszka wilk słoń osioł osiołek zając zajączek gołąb wróbel wróbelek foka królik gęś hipopotam "
     "nosorożec delfin", "szary"),
    ("kot kotek kocur kotka lis lisek wiewiórka pies", "rudy"),
    ("niedźwiedź niedźwiadek miś koń konik pies krowa bóbr jeleń sarna wielbłąd małpa kangur", "brązowy"),
    ("żaba żabka krokodyl aligator jaszczurka kameleon pasikonik gąsienica papuga papużka wąż żółw", "zielony"),
    ("motyl motylek papuga papużka paw kameleon tukan rybka", "kolorowy"),
    ("biedronka rak krab", "czerwony"), ("świnia prosiak prosiaczek flaming", "różowy"),
    ("kurczak kurczaczek kaczątko kaczuszka pszczoła pszczółka", "żółty"), ("rybka", "złoty"),
    ("kot kocur leniwiec", "leniwy"), ("słoń wieloryb kaszalot żyrafa hipopotam nosorożec niedźwiedź goryl", "wielki"),
    ("mrówka myszka biedronka komar kurczaczek", "malutki"), ("mysz myszka ryba rybka", "cichy"),
    ("kogut papuga osioł", "głośny"), ("żyrafa", "wysoki"), ("sowa delfin słoń pies", "mądry"),
    ("pszczoła pszczółka mrówka bóbr", "pracowity"), ("wąż dżdżownica", "długi"), ("hipopotam świnia kocur niedźwiedź", "gruby"),
    # zabawki
    ("miś misiek misiaczek pluszak", "mały duży miękki puszysty kochany stary nowy brązowy"),
    ("lalka laleczka", "mały ładny nowy stary piękny"),
    ("piłka piłeczka", "mały duży nowy kolorowy czerwony niebieski żółty okrągły lekki"),
    ("balon balonik", "czerwony niebieski żółty zielony kolorowy duży mały okrągły lekki różowy"),
    ("latawiec", "kolorowy duży nowy czerwony lekki"), ("samochodzik autko", "mały nowy czerwony niebieski szybki"),
    ("bączek jojo kostka kredka grzechotka", "mały kolorowy nowy"), ("kredka", "czerwony niebieski zielony żółty"),
    ("rower rowerek hulajnoga deskorolka", "nowy stary mały szybki czerwony niebieski"),
    ("huśtawka zjeżdżalnia piaskownica trampolina karuzela", "nowy duży mały kolorowy stary"),
    # kuchnia i meble
    ("łyżka łyżeczka widelec nóż", "mały duży czysty brudny nowy"), ("nóż", "ostry"),
    ("talerz talerzyk miska miseczka kubek kubeczek szklanka filiżanka dzbanek garnek patelnia czajnik",
     "mały duży czysty brudny pusty pełny nowy"),
    ("kubek kubeczek talerz talerzyk miska miseczka filiżanka dzbanek", "biały niebieski czerwony żółty zielony kolorowy"),
    ("garnek patelnia czajnik", "gorący ciężki"),
    ("stół stolik krzesło fotel łóżko łóżeczko kanapa szafa", "nowy stary mały duży ładny biały"),
    ("fotel łóżko łóżeczko kanapa", "miękki"), ("stół szafa", "ciężki wielki"),
    ("dom domek", "mały duży nowy stary ładny biały piękny"),
    # jedzenie
    ("chleb bułka bułeczka rogal rogalik chała precel", "świeży ciepły chrupiący smaczny pyszny"),
    ("pączek drożdżówka ciasto ciastko tort sernik szarlotka piernik ciasteczko", "słodki smaczny pyszny świeży"),
    ("tort", "wielki"), ("pizza", "gorący pyszny smaczny duży okrągły"),
    ("@owoce", "słodki soczysty smaczny dojrzały świeży pyszny"),
    ("jabłko jabłuszko truskawka malina wiśnia czereśnia porzeczka", "czerwony"),
    ("jabłko gruszka kiwi arbuz winogrono", "zielony"), ("banan cytryna gruszka melon", "żółty"),
    ("cytryna jabłko wiśnia porzeczka kiwi", "kwaśny"), ("śliwka winogrono jagoda borówka", "fioletowy"),
    ("arbuz melon ananas", "duży wielki"), ("jagoda poziomka borówka malina porzeczka", "mały"),
    ("ser masło szynka kiełbasa parówka jogurt serek", "świeży smaczny pyszny"), ("ser masło", "żółty"),
    ("jogurt serek", "biały zimny"), ("jajko jajeczko", "świeży biały mały"), ("pisanka", "kolorowy ładny"),
    ("zupa rosół barszcz kasza makaron ryż gulasz bigos owsianka", "gorący smaczny pyszny ciepły"),
    ("barszcz", "czerwony"), ("ryż", "biały"), ("kisiel budyń", "słodki smaczny pyszny"),
    ("kanapka naleśnik kotlet hamburger", "smaczny pyszny duży świeży"), ("kotlet", "gorący"), ("naleśnik", "słodki"),
    ("cukierek lizak czekolada batonik ciasteczko", "słodki smaczny pyszny mały"), ("lizak", "kolorowy czerwony"),
    ("czekolada", "biały"), ("miód dżem marmolada", "słodki smaczny pyszny"), ("miód", "złoty"),
    ("keczup", "czerwony"), ("majonez", "biały"), ("musztarda", "żółty"),
    ("mleko", "biały ciepły zimny świeży smaczny"), ("sok kompot lemoniada oranżada", "słodki zimny smaczny pyszny"),
    ("sok", "pomarańczowy"), ("woda", "zimny ciepły czysty gorący"), ("kakao herbata kawa", "gorący ciepły smaczny słodki"),
    ("kawa", "czarny"),
    ("@warzywa", "świeży smaczny zdrowy"), ("marchewka marchew dynia", "pomarańczowy"),
    ("ogórek sałata kapusta groszek papryka", "zielony"), ("pomidor papryka burak rzodkiewka", "czerwony"),
    ("kukurydza papryka", "żółty"), ("cebula czosnek", "biały"), ("marchewka ogórek rzodkiewka sałata", "chrupiący"),
    ("pomidor", "soczysty dojrzały"), ("dynia kapusta", "duży wielki"), ("groszek rzodkiewka", "mały"),
    ("marchewka", "słodki"), ("ogórek", "kwaśny"),
    # ubrania
    ("czapka czapeczka szalik kurtka sweter sweterek bluza bluzka koszula koszulka sukienka spódnica spódniczka płaszcz "
     "piżama szlafrok kombinezon", "nowy stary ładny czysty brudny kolorowy czerwony niebieski zielony żółty biały różowy"),
    ("czapka czapeczka szalik kurtka sweter sweterek bluza płaszcz piżama szlafrok kombinezon", "ciepły"),
    ("szalik sukienka spódnica płaszcz szlafrok", "długi"), ("kurtka czapka", "mokry"),
    ("but bucik", "nowy stary brudny czysty mokry mały"), ("skarpetka rękawiczka", "ciepły czysty brudny mokry kolorowy mały"),
    ("kapelusz", "nowy stary duży czarny"), ("parasol parasolka", "mokry kolorowy czerwony czarny duży nowy"),
    # szkoła
    ("książka książeczka", "ciekawy nowy stary gruby kolorowy"), ("zeszyt", "nowy czysty niebieski gruby"),
    ("ołówek", "nowy ostry długi"), ("długopis", "nowy niebieski czerwony"), ("gumka linijka klej temperówka", "nowy mały"),
    ("kartka", "biały czysty kolorowy"), ("kolorowanka", "nowy kolorowy"), ("pędzel", "mały nowy mokry"),
    ("plastelina", "kolorowy miękki"), ("plecak piórnik", "nowy kolorowy czerwony niebieski ciężki pusty"),
    ("tablica", "czarny zielony czysty duży"), ("globus mapa", "duży stary kolorowy nowy"),
    # dom
    ("lampa lampka", "nowy stary mały jasny ładny"), ("zegar zegarek", "stary nowy mały duży złoty"),
    ("obraz obrazek", "ładny piękny stary kolorowy duży mały"), ("lustro lusterko", "czysty duży mały stary"),
    ("telefon", "nowy stary mały czarny"), ("klucz kluczyk", "mały stary złoty"),
    ("ręcznik", "czysty mokry miękki suchy biały"), ("mydło szampon", "pachnący"),
    ("szczoteczka grzebień szczotka", "nowy mały"), ("pasta", "biały"),
    ("poduszka koc kocyk kołdra", "miękki ciepły czysty nowy kolorowy puszysty"),
    ("kwiat kwiatek", "piękny ładny kolorowy pachnący mały czerwony żółty biały"),
    ("róża", "czerwony biały żółty różowy piękny pachnący"), ("tulipan", "czerwony żółty piękny"),
    ("stokrotka konwalia dmuchawiec", "biały mały"), ("mak", "czerwony"), ("słonecznik mlecz", "żółty"),
    ("słonecznik", "wysoki duży"), ("fiołek bratek", "fioletowy mały"), ("niezapominajka", "niebieski mały"),
    ("konwalia", "pachnący"),
    ("świeczka świeca", "mały jasny"), ("prezent paczka", "duży mały ładny kolorowy ciężki"),
    ("choinka", "zielony wysoki piękny pachnący duży"), ("bombka", "złoty czerwony srebrny kolorowy okrągły"),
    ("list", "długi"), ("pocztówka", "ładny kolorowy"), ("moneta pieniążek grosik", "złoty mały okrągły"),
    ("skarb", "wielki złoty stary"), ("korona", "złoty piękny ciężki"), ("miotła", "stary nowy"),
    ("wiadro wiaderko", "pełny pusty ciężki czerwony niebieski"), ("łopatka foremka", "mały kolorowy czerwony żółty"),
    # przyroda
    ("słońce", "jasny ciepły gorący żółty złoty wielki"), ("księżyc", "jasny okrągły złoty wielki"),
    ("gwiazda gwiazdka", "jasny mały złoty"), ("chmura chmurka", "biały szary ciemny czarny mały duży"),
    ("tęcza", "kolorowy piękny wielki"), ("śnieg", "biały zimny mokry czysty miękki puszysty"),
    ("mgła", "gęsty biały szary"), ("deszcz", "ciepły zimny"), ("wiatr", "silny zimny ciepły"),
    ("rzeka", "długi głęboki czysty zimny"),
    ("@drzewa", "wysoki stary zielony młody duży mały piękny"), ("grzyb grzybek", "mały duży brązowy czerwony"),
    ("liść listek", "zielony żółty czerwony suchy mały złoty kolorowy"), ("kasztan żołądź szyszka", "brązowy mały twardy"),
    ("orzech", "twardy mały smaczny"), ("kamień kamyk", "twardy ciężki szary mały zimny"), ("kamień", "wielki duży"),
    ("muszla muszelka", "biały ładny mały"), ("sopel", "zimny długi ostry"), ("kałuża", "mały duży głęboki wielki"),
    ("ogień", "gorący"), ("ognisko", "gorący ciepły wielki duży"),
    # pojazdy
    ("auto samochód autobus tramwaj taksówka",
     "nowy stary szybki mały duży czysty brudny czerwony niebieski żółty zielony biały czarny"),
    ("karetka", "biały szybki"), ("radiowóz", "niebieski szybki"),
    ("motor motocykl skuter", "szybki nowy stary głośny czerwony czarny"),
    ("ciężarówka wywrotka koparka dźwig betoniarka walec spychacz", "wielki duży ciężki żółty głośny stary nowy"),
    ("traktor ciągnik kombajn", "duży stary nowy czerwony zielony głośny"),
    ("pociąg lokomotywa", "długi szybki stary głośny"), ("lokomotywa", "ciężki czarny wielki"),
    ("wagon kolejka", "długi mały stary"),
    ("łódka łódź jacht żaglówka kajak ponton tratwa", "mały biały nowy stary szybki"),
    ("statek okręt", "wielki duży stary biały"),
    ("samolot helikopter śmigłowiec odrzutowiec szybowiec sterowiec", "szybki duży mały biały głośny"),
    ("rakieta", "szybki wielki biały"),
]

# ---------------------------------------------------------------------------------------------
# „mama je zupę w kuchni”: dla tych grup czynności dokładamy miejsce (jeśli podmiot też je ma)
# ---------------------------------------------------------------------------------------------
GDZIE = {
    "je": "w kuchni|w domu|przy stole|w ogrodzie|na tarasie|na balkonie|u babci|u cioci|w przedszkolu|w szkole|w restauracji",
    "pije": "w kuchni|w domu|przy stole|w ogrodzie|na tarasie|na balkonie|u babci|u cioci|w kawiarni|w restauracji",
    "czyta": "w łóżku|na kanapie|na fotelu|w pokoju|w domu|w ogrodzie|w bibliotece|w szkole|u babci|przy biurku|na ławce|w parku",
    "rysuje": "przy stole|przy biurku|w pokoju|w domu|w przedszkolu|w szkole|u babci|na dywanie|na podłodze",
    "kuchnia": "w kuchni|w domu|u babci",
}

# ---------------------------------------------------------------------------------------------
# PARY do „… i …”: w obrębie tych kategorii łączymy podmioty ze sobą (bez zdrobnień tego samego słowa),
# plus pary dopisane ręcznie.
# ---------------------------------------------------------------------------------------------
PARY_W_KATEGORIACH = ("dorośli koty psy domowe farma leśne owady ptaki wodne egzotyczne pluszaki naczynia "
                      "pieczywo owoce nabiał dania napoje warzywa ubrania szkolne meble kwiaty drzewa auta "
                      "łodzie samoloty").split()
# Słów zbyt ogólnych nie łączymy automatycznie („ptak i wrona”, „mama i pan”).
BEZ_PAR_AUTO = set("pan pani ptak ptaszek ptaszyna ryba drzewo drzewko krzak krzew kwiat kwiatek kwiaty sztućce "
                   "pluszak dom domek".split())
# W zdaniach „… i … + miejsce” pomijamy miejsca dla jednej osoby („mama i tata na krześle”).
PARY_BEZ_MIEJSC = _m(na="krześle fotelu rowerze koniu kucyku hulajnodze deskorolce", w="wózku łóżeczku foteliku kołysce")
PARY_DODATKOWE = ("mama-tata pani-pan kot-pies kot-mysz kot-myszka pies-kotek mama-dziecko mama-córeczka mama-synek "
                  "tata-synek tata-córeczka babcia-dziadek ciocia-wujek brat-siostra król-królowa książę-księżniczka "
                  "królewicz-królewna lalka-miś chleb-masło chleb-ser bułka-masło bułka-ser mleko-miód kawa-ciasto "
                  "herbata-ciastko słońce-księżyc słońce-chmura księżyc-gwiazda słońce-tęcza deszcz-wiatr "
                  "śnieg-wiatr rycerz-smok królewna-smok czarownica-kot wilk-zając lis-kura lis-zając kot-ptak "
                  "stół-krzesło łóżko-szafa talerz-łyżka kubek-talerz nóż-widelec łyżka-widelec "
                  "czapka-szalik kurtka-czapka auto-rower piłka-lalka miś-lalka babcia-kot dziadek-pies "
                  "dziecko-pies dziecko-kot chłopiec-pies dziewczynka-kot pirat-papuga zeszyt-ołówek "
                  "książka-zeszyt ołówek-gumka mydło-ręcznik poduszka-kołdra drzewo-krzak grzyb-liść "
                  "sąsiad-sąsiadka braciszek-siostrzyczka chłopiec-dziewczynka synek-córeczka uczeń-uczennica "
                  "mydło-szampon szczoteczka-pasta grzebień-szczotka poduszka-koc lampa-zegar obraz-lustro "
                  "koc-kołdra telefon-klucz krzak-drzewo ptak-ryba kwiat-drzewo dom-drzewo dom-ogień "
                  "miś-pluszak kot-ryba").split()

# ---------------------------------------------------------------------------------------------
# „na stole jest kubek”: miejsca-czynności, z którymi takie odwrócone zdanie brzmi źle
# ---------------------------------------------------------------------------------------------
BEZ_ODWRACANIA = _m(
    na="spacerze wycieczce wakacjach rowerze koniu sankach nartach łyżwach rolkach deskorolce hulajnodze kucyku "
       "urodzinach balu weselu koncercie lekcji meczu wyścigu smyczy miotle traktorze kempingu biwaku słońcu",
    w="kąpieli deszczu skafandrze zbroi koronie kapeluszu bajce filmie praniu", u=_U + " lekarza dentysty fryzjera weterynarza",
    przy="pożarze")

# ---------------------------------------------------------------------------------------------
# ZDANIA ŚMIESZNE – z czego wolno je układać
# ---------------------------------------------------------------------------------------------
# Miejsca do śmiesznych zdań: zabawne i bezpieczne (bez piekarnika, pralki, ulicy itp.).
SMIESZNE_MIEJSCA = _m(
    na="księżycu szafie choince tęczy dachu karuzeli miotle torcie tronie drzewie huśtawce zjeżdżalni trampolinie "
       "rowerze hulajnodze deskorolce nartach łyżwach sankach rolkach koniu kucyku traktorze statku wyspie pustyni "
       "lodowisku basenie plaży balu weselu koncercie urodzinach lekcji wakacjach wycieczce spacerze komodzie "
       "parapecie lampie suficie kominie płocie słupie maszcie bałwanie lianie pajęczynie gałęzi",
    w="kapeluszu kieszeni plecaku walizce koszyku pudełku szufladzie wannie akwarium rakiecie kosmosie samolocie "
      "helikopterze taksówce tramwaju autobusie pociągu kinie teatrze cyrku szkole przedszkolu bibliotece muzeum "
      "restauracji kawiarni sklepie banku hotelu zamku pałacu koronie zbroi skafandrze namiocie ulu gnieździe "
      "budzie norce dziupli mrowisku kurniku chmurach dżungli zoo lunaparku orkiestrze kałuży błocie piaskownicy "
      "wózku łóżeczku kołysce filiżance kubku czajniku dzbanku butelce słoiku wazonie doniczce zegarze skarbonce "
      "portfelu torebce kopercie piórniku",
    pod="łóżkiem stołem kołdrą parasolem prysznicem grzybem choinką poduszką wycieraczką",
    u="fryzjera dentysty lekarza weterynarza", za="piecem kominem szafą", przy="tablicy")
# Przymiotniki do śmiesznych zdań: dla ludzi tylko pierwsza lista, dla zwierząt i rzeczy obie.
SMIESZNE_PRZYM_LUDZIE = "zielony niebieski różowy fioletowy pomarańczowy srebrny złoty kolorowy malutki wielki puszysty".split()
SMIESZNE_PRZYM_RESZTA = "okrągły pachnący słodki miękki szybki".split()
# Czasowniki do śmiesznych zdań: „zwierzęce” dla wszystkich żywych, „ludzkie” tylko dla zwierząt i stworów.
SMIESZNE_V_ZWIERZECE = ("miauczy mruczy szczeka warczy muczy ryczy rży beczy meczy chrumka kwiczy gdacze pieje kwacze "
                        "gęga gulgocze wyje huka kumka rechocze bzyczy ćwierka kracze skrzeczy grucha kuka klekocze "
                        "syczy trąbi piszczy cyka fruwa kica galopuje pełznie raczkuje nurkuje tyka dzwoni gwiżdże "
                        "topnieje kwitnie").split() + ["pasie się"]
SMIESZNE_V_LUDZKIE = ("tańczy śpiewa czyta rysuje maluje gotuje piecze sprząta chrapie gra pisze liczy czaruje "
                      "pracuje").split() + ["czesze się", "ubiera się", "huśta się", "ślizga się"]
# Wyrażeń zawierających te słowa nie wkładamy do śmiesznych zdań.
SMIESZNE_BEZ_SLOW = set("dziecko dzieci dzieciom brodę wąsy pożarze złodzieja katar zastrzyk lekarstwo daje kradnie "
                        "porywa rękę garb rogi poroże smycz obrożę piegi".split())
# Par z tych list nie łączymy spójnikiem „i” (to samo innymi słowami).
NIE_PARY = set("auto-samochód helikopter-śmigłowiec traktor-ciągnik pies-psiak piesek-psiak szczeniak-psiak "
               "gęś-gąska gęś-gąsior uczeń-pierwszak uczennica-pierwszak".split())
