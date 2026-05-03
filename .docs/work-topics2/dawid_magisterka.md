# Lista tematów do wyboru — Dawid Olko (praca magisterska, rozszerzenie SmartRecommender)

---

## Temat D1 — Hybrydowe łączenie metod rekomendacji (CF + Apriori + sentyment) vs metody pojedyncze

**Krótki opis**
Porównanie ośmiu konfiguracji rankera: trzy pojedyncze kanały (CF, Apriori, sentyment), trzy fuzje dwukanałowe (CF+Apriori, CF+sentyment, Apriori+sentyment), pełna fuzja trójkanałowa, baseline popularności. Fuzja implementowana jako RRF (Reciprocal Rank Fusion), opcjonalnie Borda i weighted average.

**Gdzie to siedzi w kodzie**
- CF: `recommendation_views.py` + tabela `ProductSimilarity`
- Apriori: `custom_recommendation_engine.py::CustomAssociationRules` + tabela `ProductAssociation`
- Sentyment: `custom_recommendation_engine.py::CustomSentimentAnalysis` + tabela `Opinion`
- Nowy moduł: `home/experiments/fusion.py` (RRF, Borda, Weighted)

**Cel badawczy**
Sprawdzić, czy fuzja kanałów istotnie statystycznie poprawia NDCG@10 i Precision@10 względem najlepszego pojedynczego kanału i baseline'u popularności, oraz który podzbiór kanałów jest redundantny.

**Hipotezy**
- H1: najlepsza fuzja trójkanałowa poprawia NDCG@10 o ≥10% nad najlepszym singletonem
- H2: któraś fuzja dwukanałowa = trójkanałowej (jeden kanał redundantny)
- H3: dla cold-start (<3 zamówień) sentyment+Apriori biją CF
- H4: RRF jest robustniejszy niż weighted average (nie wymaga kalibracji score'ów)

**Innowacyjność**
Ablacja kanałów jako pierwszorzędny wynik (nie dodatek), stratyfikacja po cold-start, reprodukowalny seeder z personami.

**Co wnosi**
Twardą inżynierską odpowiedź "którą fuzję wdrożyć i czy w ogóle". Nadaje się jako trzon pracy lub jej połowa.

---

## Temat D2 — Wpływ hiperparametrów na jakość i koszt obliczeniowy CF, Apriori, sentymentu

**Krótki opis**
Studium czułości hiperparametrów: próg podobieństwa par CF, `min_support` i `min_confidence` Apriori, parametry agregacji sentymentu (waga recency, próg neutralności, min liczba opinii). Siatka lub Optuna, krzywe Pareto jakość vs czas vs rozmiar tabeli.

**Gdzie to siedzi w kodzie**
- Apriori: parametry `CustomAssociationRules` w `custom_recommendation_engine.py`, endpoint `update-association-rules`
- CF: logika progu w `recommendation_views.py`
- Sentyment: formuły w `CustomSentimentAnalysis`

**Cel badawczy**
Wyznaczyć krzywe czułości NDCG@10 vs koszt regeneracji (czas + rozmiar tabeli) dla każdego z trzech kanałów, znaleźć punkty Pareto-optymalne, sprawdzić czy domyślne wartości z inżynierki są blisko optimum.

**Hipotezy**
- H1: krzywa NDCG@10(`min_support`) ma kolano w 0.02–0.05
- H2: próg podobieństwa CF wpływa głównie na rozmiar tabeli, nie na NDCG
- H3: waga recency sentymentu istotna tylko dla userów z >5 opiniami
- H4: domyślne wartości inżynierki leżą poza frontem Pareto co najmniej dla jednego kanału

**Innowacyjność**
Trójwymiarowy Pareto (NDCG × czas × rozmiar tabeli), niezależne strojenie kanałów + check joint tuning na próbie kontrolnej.

**Co wnosi**
Praktyczną instrukcję eksploatacyjną. Dobry **podrozdział** D1 albo D10. Sam jako trzon pracy mag. — za wąsko.

---

## Temat D3 — Bielik 11B (lokalny LLM) jako re-ranker listy kandydatów rekomendacji

**Krótki opis**
LLM dostaje zamrożoną listę 40 kandydatów z generatora klasycznego (np. fuzji CF+Apriori) i ma ją tylko **uporządkować**. Walidacja JSON przez Pydantic, fallback do score'u generatora przy błędzie. Porównanie modeli (Bielik 7B/11B, Mistral Small, Qwen 2.5), strategii promptu (zero-shot vs few-shot), pomiar latency p95, hallucination rate, conformance rate.

**Gdzie to siedzi w kodzie**
- Generator kandydatów: `RecommendedProductsAPIView` + fuzja z D1
- Nowy moduł: `home/experiments/llm_recommender.py`
- Stack: Ollama (lokalnie) + httpx + pydantic v2 + tabela `ExperimentRun` na wyniki

**Cel badawczy**
Sprawdzić, czy lokalny polski LLM jako warstwa re-ranku poprawia NDCG@10 nad samym sortowaniem po score generatora — przy jednoczesnym pomiarze kosztu operacyjnego (latency, hallucinations).

**Hipotezy**
- H1: G1 (z LLM) > G0 (bez LLM, ten sam zbiór kandydatów) w NDCG@10, Wilcoxon p<0.05
- H2: Bielik 11B > Bielik 7B w NDCG@10 o ≥5%, ale 7B ma wyższy conformance rate
- H3: few-shot podnosi conformance o ≥20pp przy podobnym NDCG
- H4: hallucination rate >0% nawet po walidacji, rośnie z długością listy
- H5: latency p95 Bielik 11B na CPU M3 Pro >5s/user → wdrożenie wymaga GPU

**Innowacyjność**
Pierwsze (lub jedne z pierwszych) testy Bielika v3 w zadaniu rec-sys, hallucination rate jako nowa metryka jakości usługi, twarda separacja "LLM tylko do permutacji".

**Co wnosi**
Empiryczną odpowiedź "czy polski LLM dokłada coś nad sortowaniem po score". Nadaje się jako trzon pracy lub składnik D10.

---

## Temat D4 — Profile rekomendacyjne z danych jawnych (opinie) vs ukrytych (interakcje + dwell time)

**Krótki opis**
Porównanie dwóch strumieni danych przy identycznym ground truth (przyszłe zakupy w teście): system J (ranking z `Opinion` + sentyment + ratingi) vs system U (ranking z `UserInteraction` + opcjonalnie `duration_ms`). Plus prosta fuzja JU (RRF). Stratyfikacja po liczbie opinii, liczbie interakcji, personie.

**Gdzie to siedzi w kodzie**
- Jawne (moja strona): `Opinion`, `CustomSentimentAnalysis`
- Ukryte (część Piotra): `UserInteraction`, opcjonalnie nowe pole `duration_ms` (migracja + tracking we frontendzie `ProductPage.jsx`)

**Cel badawczy**
Określić, który strumień daje wyższy NDCG@10 globalnie i w stratyfikacji, oraz czy ich fuzja bije oba pojedyncze.

**Hipotezy**
- H1: globalna różnica J vs U <5%, kierunek zależy od stratyfikacji
- H2: dla 0–2 opinii U > J; dla 10+ opinii J ≥ U
- H3: fuzja JU bije oba o <3% (nie warto)
- H4: dodanie dwell time do U poprawia NDCG@10 o ≥5%

**Innowacyjność**
Kontrolowane porównanie (ten sam ground truth, ten sam K, te same testy statystyczne — rzadkie w literaturze), stratyfikacja persona-driven.

**Co wnosi**
Biznesową odpowiedź "inwestować w opinie czy w tracking". Naturalna synergia z pracą Piotra (wspólny seed). Lepiej jako **rozdział wspólny / uzupełniający** niż trzon pracy.

---

## Temat D5 — Skalowalność implementacji CF i Apriori w Django + PostgreSQL

**Krótki opis**
Seria rozmiarów bazy (50 → 100 → 200 → 400 → 800 klientów) przy zamrożonym teście referencyjnym. Pomiar: czas regeneracji CF, czas Apriori, czas pojedynczego zapytania (p50, p95), rozmiar tabel `ProductSimilarity` i `ProductAssociation`. `EXPLAIN ANALYZE` na 2–3 najcięższych zapytaniach, propozycje optymalizacji (indeksy, cache, batch) + pomiar przed/po.

**Gdzie to siedzi w kodzie**
- CF/Apriori: jak wyżej
- Cache: sprawdzić istniejący w `recommendation_views.py`
- Pomiary: `time.perf_counter`, `tracemalloc`, `psycopg` z surowym SQL

**Cel badawczy**
Wyznaczyć empiryczne krzywe `czas(N)` i `rozmiar_tabeli(N)`, zidentyfikować dominujące zapytania SQL, zaproponować i zmierzyć ≥2 optymalizacje.

**Hipotezy**
- H1: czas CF rośnie kwadratowo z |produkty| (item-based: O(|I|²·|U|))
- H2: czas Apriori rośnie silniej z |zamówienia| niż z |produkty|
- H3: NDCG@10 na referencyjnym teście NIE spada ze skalą (problemem jest koszt, nie jakość)
- H4: indeks złożony na `Order(user_id, date_order)` skraca czas CF o ≥30% przy N=400
- H5: cache rankingów per-user (TTL 1h) skraca p95 o ≥80%

**Innowacyjność**
Empiryczna krzywa skalowania konkretnego stacku, identyfikacja zapytań-zabójców z `EXPLAIN ANALYZE`, walidacja optymalizacji przed/po (większość prac proponuje, nie mierzy).

**Co wnosi**
Solidny rozdział inżynierski. Nadaje się jako **podrozdział** w pracy z trzonem D1 lub D10. Sam jako trzon — możliwy, ale mało innowacyjny.

---

## Temat D9 — Rekomendacja na podstawie opisów produktów (zamiana opisów na liczby + wyszukiwanie podobnych)

**Krótki opis (po ludzku)**
Klasyczne CF i Apriori patrzą tylko na to, **co kto kupował**. Ignorują **opisy produktów** (nazwa, opis, kategoria), które są w bazie. Tutaj robimy odwrotnie — patrzymy **wyłącznie na treść**:

1. Każdy opis produktu zamieniamy na **wektor liczb** (np. 768 cyfr) — taki "odcisk palca" tekstu. Robi to gotowy model językowy z biblioteki sentence-transformers (jak Google Translate, ale zamiast tłumaczyć — zwija tekst do liczb tak, że podobne znaczeniowo opisy mają **podobne wektory**). Po polsku to się nazywa "wektoryzacja tekstu" albo "embedding" (zostawiam słowo bo i tak jest standardem w branży).
2. Wektory wszystkich produktów wrzucamy do bazy danych (rozszerzenie `pgvector` do PostgreSQL — i tak go używam, więc bez nowych usług).
3. Dla użytkownika budujemy "tekst zapytania" z jego historii zakupów (np. "Kupił: laptop gamingowy, mysz Razer, słuchawki HyperX") i też zamieniamy go na wektor.
4. Szukamy w bazie produktów, których wektory są **najbliższe** wektorowi użytkownika (mierzone kątem między wektorami — to jest "podobieństwo cosinusowe", proste mnożenie i dodawanie).
5. Wyświetlamy top 10 najbliższych — to są rekomendacje **po znaczeniu opisu**.

**Trzy badane warianty:**
- **R0** — baseline popularności (najczęściej kupowane)
- **R1** — czysty retrieval (kroki 1–5 powyżej, bez żadnego LLM)
- **R2** — to samo co R1, ale na końcu **lokalny model językowy (Bielik)** czyta opisy 50 najbliższych produktów i przestawia ich kolejność (jakby "doczytał" co tam piszą i wybrał 10 najlepszych)

**Po co dwa modele do wektoryzacji**
Porównujemy model **wielojęzyczny** (rozumie polski) vs **angielski** (formalnie nie rozumie polskiego, ale często działa) — na polskich opisach. Pytanie czy warto brać większy/wolniejszy model wielojęzyczny.

**Gdzie to siedzi w kodzie**
- Tekst produktu: pola `Product.name`, `Product.description`, `Product.category` z `models.py`
- Nowy moduł: `home/experiments/embedding_index.py` (zamiana tekstu na wektory + zapis do pgvector)
- LLM (tylko dla R2): `home/experiments/llm_recommender.py` (Ollama + Bielik)

**Cel badawczy**
Sprawdzić czy rekomendacja po opisach (R1) bije popularność (R0), czy dodanie LLM (R2) coś dokłada nad samym R1, oraz czy radzi sobie z **nowymi produktami** (które nie mają jeszcze zakupów — CF ich nie widzi, ale opis już mają).

**Hipotezy**
- H1: R1 (retrieval) > R0 (popularność) o ≥10% w NDCG@10
- H2: R2 (z LLM) > R1 (bez LLM) tylko gdy LLM dostaje dużo kandydatów (50). Przy 10 — różnicy nie ma
- H3: model wielojęzyczny lepiej rozumie polskie opisy niż angielski (różnica ≥15 punktów procentowych w Recall)
- H4: czas odpowiedzi R2 jest zdominowany przez LLM (90%+ czasu) — sam retrieval jest błyskawiczny (<100 ms)
- H5: dla nowych produktów (mniej niż 5 zakupów) R1 bije CF o ≥20% — bo R1 patrzy na opis, a CF nie ma na czym pracować

**Innowacyjność**
Polski e-commerce + porównanie modeli wektoryzacji + osobny eksperyment "co z nowymi produktami" + jeden czytelny pipeline (PostgreSQL + pgvector + Ollama, bez egzotycznych usług).

**Co wnosi**
Praktyczna odpowiedź "czy warto inwestować w długie sensowne opisy produktów" (bo to przekłada się na rekomendacje) i "czy LLM dokłada coś nad sam wyszukiwaniem po wektorach". Nadaje się jako trzon pracy lub składnik D10.

---

## Temat D10 (REKOMENDOWANY) — Połączenie wszystkich trzech podejść w jeden pipeline (klasyczne metody + opisy produktów + LLM)

**Krótki opis (po ludzku)**
Spaja D1, D3 i D9 w jeden duży system, który działa **trzyetapowo**:

1. **Etap 1 — szukamy kandydatów z czterech źródeł równocześnie:**
   - z CF (kto kupił to, kupił też tamto),
   - z reguł Apriori (kto kupił X, ten zwykle bierze też Y),
   - z sentymentu opinii (produkty pasujące do tego, co user dobrze ocenia),
   - z opisów produktów (z D9 — wektorowe podobieństwo opisów).

   Każde źródło zwraca swoją listę top-N kandydatów.

2. **Etap 2 — łączymy te cztery listy w jedną** (np. metodą RRF — kto jest wysoko na wielu listach, idzie wyżej w finalnej).

3. **Etap 3 — lokalny LLM (Bielik) na końcu** dostaje tę połączoną listę i przestawia kolejność (zostawiając te same produkty, tylko inaczej je ustawiając).

**Co porównujemy** — siedem wariantów, żeby zobaczyć **który komponent ile dokłada**:

| Wariant | Co robi | Co reprezentuje |
|---|---|---|
| **B0** | popularność | baseline obowiązkowy |
| **V1** | sama klasyka (CF + Apriori + sentyment, fuzja) | = D1 |
| **V2** | same opisy produktów (wektory + szukanie podobnych) | = D9 R1 |
| **V3** | opisy + LLM przestawia | = D9 R2 |
| **V4** | klasyka + LLM przestawia | = D3 |
| **V5 (główny)** | wszystko naraz: 4 źródła kandydatów → fuzja → LLM | nowość |
| **V6** | dwa etapy: opisy znajdują kandydatów → klasyka szereguje → LLM dopina | tańszy wariant produkcyjny |

**Po co tyle wariantów**
Żeby odpowiedzieć "co tu naprawdę pomaga". Jeżeli V5 jest nieznacznie lepszy od V4 (klasyka + LLM, bez opisów), to znaczy że dodawanie wektorowego kanału opisów było stratą czasu. Jeżeli V5 jest lepszy od V3 (czyste opisy + LLM), to znaczy że klasyka nadal się przydaje. To jest tzw. **ablacja** — wyłączanie po jednym komponencie żeby zmierzyć ich indywidualny wkład.

**O co chodzi z "Pareto"**
Pareto-optymalny wariant to taki, którego **nie da się poprawić bez zepsucia czegoś innego**. Czyli: V5 ma najlepszą jakość ale jest najwolniejszy; V1 jest najszybszy ale ma niską jakość; V6 może być pośrodku — gorszy w jakości od V5 o 1%, ale 30% szybszy. Wtedy V6 jest na "froncie Pareto" — żaden inny wariant nie jest jednocześnie szybszy i lepszy. To pokazujemy na wykresie (oś X = czas, oś Y = jakość, każdy wariant jako kropka) i wskazujemy "do produkcji proponuję V6" zamiast tylko V5.

**Gdzie to siedzi w kodzie**
Składa wszystko z D1 + D3 + D9 w jeden moduł:
- Klasyka (CF, Apriori, sentyment) — pliki z D1
- Wektory opisów + pgvector — z D9
- LLM Bielik + Ollama + Pydantic — z D3
- Wspólny moduł oceny: `home/experiments/{base_recommender,metrics,splits,runner,fusion,llm_recommender,embedding_index}.py`
- Tabela wyników: `ExperimentRun`

**Cel badawczy**
Zbudować i porównać siedem wariantów hybrydowego pipeline'u na tym samym splicie czasowym `seed_research`. Wskazać wariant z najlepszym stosunkiem jakości do kosztu (i odporności na nowych użytkowników/nowe produkty) jako rekomendację do wdrożenia.

**Hipotezy**
- H1: V5 (wszystko razem) bije każdy pojedynczy wariant V1–V4 o ≥5% w NDCG@10
- H2: wyrzucenie kanału opisów (V5 → V4) psuje wynik o >3% — czyli opisy faktycznie coś dokładają
- H3: wyrzucenie LLM (V5 → sama fuzja czterech) psuje wynik o >3% — czyli LLM faktycznie coś dokłada
- H4: dla nowych produktów (mniej niż 5 zakupów) V5 i V3 wygrywają z V1 i V4 o ≥20% — bo oba używają opisów, a klasyka nowych produktów nie zna
- H5: dla nowych użytkowników (mniej niż 3 zamówienia) V5 wygrywa z V1
- H6: V6 (dwustopniowy) ma podobną jakość do V5, ale ≥30% szybszy — czyli to jest **ten** wariant do produkcji
- H7: V5 ma mniej "halucynacji" LLM (wymyślania ID produktów spoza listy) niż V3, bo dostaje krótszą i lepiej wyselekcjonowaną listę kandydatów

**Innowacyjność**
- Cztery źródła kandydatów w jednym module (klasyka + opisy razem) — większość prac używa albo opisów, albo klasyki, **rzadko obu naraz**
- Wariant V6 (najpierw opisy znajdują kandydatów, potem klasyka szereguje, potem LLM dopina) — odpowiedź na drogi LLM
- Pomiar "ile co dokłada" przez wyłączanie komponentów — twardy wynik, nie spekulacje
- Polski LLM (Bielik v3) w pełnej architekturze, nie tylko jako sam re-ranker
- Liczenie "halucynacji" LLM jako funkcji jakości listy kandydatów
- Osobne eksperymenty na nowych produktach i nowych użytkownikach (większość prac to ignoruje)
- Cały stos open-source (Django + PostgreSQL + pgvector + sentence-transformers + Ollama + Bielik) + udostępniony seed losowy → ktoś inny może to powtórzyć krok po kroku

**Co wnosi**
- Gotowy szablon architektury hybrydowego rec-sys dla polskiego e-commerce z konkretnymi liczbami "ile kosztuje który wariant"
- Trzy obszary literatury (klasyczne hybrydy, LLM w rekomendacjach, RAG) w jednej spójnej pracy
- Plan B: jeśli LLM nie zadziała, V1+V2 wciąż dają pełną pracę magisterską (D1 + D9 jako fallback)

**Tytuł roboczy**
> *Hybrydowy system rekomendacji produktów łączący klasyczne metody filtracji kolaboratywnej, reguły asocjacyjne, podobieństwo opisów produktów oraz lokalny model językowy — implementacja i ewaluacja dla polskiego e-commerce*

---

---

# Tematy nie-rekomendacyjne (korzystające z aplikacji, ale nie z metod CF/Apriori/sentymentu)

---

## Temat N1 — Automatyczna kategoryzacja i analiza reklamacji klientów (NLP + LLM)

**Krótki opis (po ludzku)**
W bazie jest model `Complaint` (reklamacje). Klient pisze tekstem co go boli ("paczka przyszła zniszczona", "produkt nie działa po tygodniu", "kurier nie zadzwonił", "źle opisany rozmiar"). W realnym sklepie takie reklamacje czyta człowiek i ręcznie przypisuje kategorię + priorytet + dział.

Tu robimy to **automatycznie**:
1. Generujemy syntetyczne reklamacje w seederze (różne typy: uszkodzenie, niezgodność z opisem, brak elementu, problem z dostawą, problem z płatnością, zmiana zdania).
2. Budujemy klasyfikator który czyta tekst i przypisuje:
   - **kategorię problemu** (logistyka / jakość produktu / opis / płatność / inne),
   - **priorytet** (niski / średni / wysoki — np. zniszczenie = wysoki, zmiana zdania = niski),
   - **proponowane rozwiązanie** (zwrot / wymiana / rabat / wyjaśnienie).
3. Porównujemy **trzy podejścia**:
   - **klasyczne ML** (TF-IDF + regresja logistyczna / SVM) — szybkie, mała pamięć, wymaga oznaczonych danych
   - **wektorowe** (zamiana tekstu reklamacji na wektor jak w D9, potem klasyfikator na wektorach) — średnia złożoność, średnia jakość
   - **LLM** (Bielik dostaje tekst reklamacji + listę dostępnych kategorii, zwraca wybór w JSON) — wolne, drogie, ale działa **bez oznaczonych danych**
4. Mierzymy: dokładność klasyfikacji (accuracy, F1 per kategoria), czas, czy dla wysokiego priorytetu jest mniej pomyłek niż dla niskiego.

**Gdzie to siedzi w kodzie**
- Model `Complaint` w `models.py` (rozszerzony o pola `predicted_category`, `predicted_priority`, `predicted_solution`)
- Nowy moduł: `home/complaints_nlp/` (klasyfikatory + ewaluacja)
- Frontend: panel admina pokazuje przewidywaną kategorię obok reklamacji (`AdminPanel/`)
- Endpoint: `POST /api/complaint/{id}/classify/` zwraca trzy przewidywania

**Cel badawczy**
Sprawdzić, które z trzech podejść (klasyczne ML / wektorowe / LLM) daje najlepszą dokładność klasyfikacji reklamacji i przypisywania priorytetu — przy uwzględnieniu kosztu (czas, zasoby) i tego, czy potrzebują oznaczonych danych treningowych.

**Hipotezy**
- H1: LLM (Bielik) bez treningu osiąga ≥80% dokładności klasyfikacji kategorii — czyli "działa od razu" bez oznaczonego zbioru
- H2: Klasyczne ML (TF-IDF + LogReg) potrzebuje minimum 200 oznaczonych reklamacji żeby dorównać LLM
- H3: Wektorowe podejście jest pośrodku — lepsze niż TF-IDF przy małej liczbie danych, ale gorsze niż LLM
- H4: Dla "wysokiego priorytetu" (uszkodzenia, oszustwa) wszystkie trzy metody są dokładniejsze niż dla "niskiego" — bo to bardziej oczywiste słowa kluczowe
- H5: LLM jest 50–100× wolniejszy niż TF-IDF — więc do produkcji nadaje się tylko jako pierwsza linia (a człowiek sprawdza tylko niepewne)

**Innowacyjność**
- Polski tekst reklamacji + Bielik (mało prac NLP na polskim e-commerce)
- Porównanie trzech podejść z różną krzywą "ile danych treningowych vs jakość" — odpowiedź dla startupów "od ilu reklamacji warto trenować własny model"
- Klasyfikacja **wielowymiarowa** (kategoria + priorytet + rozwiązanie naraz), nie pojedyncza
- Pomiar "**zaufania**" predykcji LLM (poprzez logprob lub kilkukrotne wywołanie) i routing niepewnych do człowieka

**Co wnosi**
Praktyczne narzędzie dla sklepu (panel admina szybciej obsługuje zgłoszenia) + pracę magisterską z gotowym dataset'em (syntetyczne reklamacje + ich klasyfikacje, można udostępnić). Nadaje się jako trzon pracy.

---

## Temat N2 — Wykrywanie podejrzanych zachowań i nietypowych zamówień (anomaly detection)

**Krótki opis (po ludzku)**
W każdym sklepie zdarzają się **dziwne** zamówienia: bot kupuje 50 sztuk jednego produktu, ktoś nadużywa zwrotów, ktoś używa skradzionej karty. W modelach `Order`, `OrderProduct`, `UserInteraction`, `Complaint` mamy całą historię działań użytkownika.

Tu budujemy system, który dla każdego zamówienia liczy **score podejrzliwości** od 0 do 1 i wyrzuca admina alerty gdy przekroczy próg. **Bez** uczenia nadzorowanego (bo nie mamy oznaczonych "to fraud, to nie") — używamy **uczenia nienadzorowanego** (anomaly detection):

Trzy podejścia:
1. **Reguły ręczne** (baseline): "więcej niż 10 zwrotów w miesiącu", "zamówienie powyżej 5× średniej tego użytkownika", "konto założone <1h przed zakupem o wysokiej wartości" — proste IF, ale działają.
2. **Statystyczne** (Isolation Forest, Local Outlier Factor): liczymy wektor cech zamówienia (kwota, liczba produktów, godzina, czas od rejestracji, liczba poprzednich zwrotów…) i model uczy się "co jest normalne" na pełnej bazie. Co odstaje — anomalia.
3. **Sekwencyjne** (LSTM / Autoencoder na sekwencji `UserInteraction`): patrzymy nie na pojedyncze zamówienie, ale na **całą ścieżkę** (np. "10 sekund na karcie produktu, od razu zakup, od razu wylogowanie" = bot, "30 minut przeglądania → zakup" = normalny człowiek).

W seederze dodajemy **kontrolnie wstrzykiwane anomalie** (np. 5% zamówień to "boty" z bardzo krótkimi sesjami, 3% to "fraud" z kontami świeżymi i wysokimi kwotami) — to są nasze **prawdziwe pozytywy** do oceny.

**Gdzie to siedzi w kodzie**
- Modele `Order`, `OrderProduct`, `UserInteraction`, `Complaint`, `User` z `models.py`
- Nowy moduł: `home/anomaly/` (detektor + cechy + ewaluacja)
- Nowy model: `OrderRiskScore` (zamówienie → score + powód)
- Panel admina: kolumna "ryzyko" przy zamówieniach, lista alertów
- Endpoint: `GET /api/admin/risk-alerts/`

**Cel badawczy**
Sprawdzić, które z trzech podejść do wykrywania anomalii (reguły / statystyczne / sekwencyjne) ma najlepszy stosunek wykrywalności (recall) do liczby fałszywych alarmów (false positive rate) — przy uwzględnieniu, że administrator **nie chce** się utopić w alertach.

**Hipotezy**
- H1: Reguły ręczne wykrywają ≥60% wstrzykniętych anomalii, ale generują ≥15% false positive (każda 7. uczciwa transakcja jest oznaczona)
- H2: Isolation Forest na cechach zamówienia ma lepszy AUC niż reguły o ≥0.1
- H3: Sekwencyjny model (LSTM) wykrywa **boty** (krótkie sesje) lepiej niż statystyczny, ale gorzej niż statystyczny wykrywa **fraud** (drogie zamówienia)
- H4: Ensemble (głosowanie 2 z 3) ma niższy false positive rate o ≥30% przy podobnym recall
- H5: Próg alertu można dostroić tak, żeby admin dostawał ≤5 alertów dziennie i wyłapywał ≥80% prawdziwych przypadków

**Innowacyjność**
- Praca z **trzema jakościowo różnymi** metodami (regułowa / statystyczna / głębokiego uczenia) na tych samych danych
- Wstrzykiwane anomalie z różnymi profilami (bot vs fraud vs nadużycie zwrotów) — można testować wykrywalność per typ
- Pomiar "kosztu uwagi admina" (alerts per day) jako pierwszorzędny wynik, nie tylko AUC
- Dataset wstrzykniętych anomalii do udostępnienia (rzadkie w polskim e-commerce)

**Co wnosi**
Praktyczne narzędzie security dla sklepu + pełnoprawna praca magisterska z trzema metodami i pomiarami. Łączy się z biznesem (oszczędność strat na fraudzie) i z nauką (porównanie metod). Nadaje się jako trzon pracy.

---

## Temat N3 — Inteligentne wyszukiwanie produktów odporne na literówki, synonimy i pytania w języku naturalnym

**Krótki opis (po ludzku)**
W aplikacji jest wyszukiwarka produktów (`FuzzySearchAPIView` z `sentiment_views.py`). Działa, ale prymitywnie. Klient wpisuje "myszka razer dla gracza" i nic nie dostaje, bo w bazie jest "Mysz Razer Basilisk V3, dla graczy". Albo wpisuje "monitor 4k do gier" i dostaje wszystkie monitory, bo wyszukiwarka nie rozumie "do gier".

Tu budujemy wyszukiwarkę **trzypoziomową** i porównujemy:

1. **Klasyczna** (TF-IDF + obecna fuzzy search) — szybka, działa na słowach, rozumie literówki ale nie znaczenie
2. **Wektorowa** (zapytanie zamieniamy na wektor jak w D9, szukamy produktów z najbliższymi wektorami opisów) — rozumie znaczenie, dłuższa
3. **Z LLM** (Bielik dostaje zapytanie + 50 najbliższych produktów wektorowo, "rozumie" intencję typu "do gier" i odfiltrowuje) — najlepsza, ale wolna

Plus dodatkowy poziom: **autocomplete w pasku wyszukiwania** (klient wpisuje "lapt..." i dostaje sugestie "laptop gamingowy", "laptop biurowy", "laptop dla studenta") — można zrobić z N-gram albo z LLM.

Mierzymy:
- **trafność** wyszukiwania (czy klient klika w pierwszy / pierwsze 3 wyniki),
- **czas odpowiedzi** (musi być ≤300 ms żeby klient nie czekał),
- **odporność na literówki** ("razr", "razerr" → znajdzie Razera),
- **odporność na synonimy** ("słuchawki" vs "headset" vs "nauszniki"),
- **rozumienie intencji** ("monitor do gier" vs "monitor do biura" — różne wyniki dla tej samej kategorii).

**Gdzie to siedzi w kodzie**
- Obecna wyszukiwarka: `FuzzySearchAPIView` w `sentiment_views.py`
- Nowy moduł: `home/search/` (trzy implementacje + ewaluacja)
- Indeks wektorowy: pgvector (jak w D9 — można współdzielić)
- Frontend: pasek wyszukiwania w nagłówku (`components/Header/` lub podobne) + autocomplete
- Endpoint: `GET /api/search/v2/?q=...&engine=tfidf|vector|llm`

**Cel badawczy**
Sprawdzić, który silnik wyszukiwania (klasyczny / wektorowy / LLM) daje najwyższą trafność dla **trzech typów zapytań**: literówkowych, synonimicznych, intencyjnych — przy zachowaniu akceptowalnego czasu odpowiedzi (<300 ms dla klasyki i wektora, <2 s dla LLM).

**Hipotezy**
- H1: Klasyczna wyszukiwarka (TF-IDF + fuzzy) wygrywa na literówkach (≥90% trafność), ale przegrywa na synonimach (<50%)
- H2: Wektorowa wygrywa na synonimach (≥85%), ale jest gorsza na literówkach niż klasyczna (bo "razr" ma inny wektor niż "razer")
- H3: LLM wygrywa na intencjach ("do gier", "do biura") — ≥80% dla intencji, klasyka i wektor <40%
- H4: Hybryda (klasyka dla krótkich zapytań ≤2 słowa, wektor dla 3–5 słów, LLM dla 6+ słów lub pytań) bije każdy pojedynczy silnik o ≥10% globalnie
- H5: Autocomplete oparty na N-gram + popularności wystarczy — LLM nie dokłada nad nim wartości (i jest 100× wolniejszy)

**Innowacyjność**
- Trzypoziomowe porównanie + hybryda + autocomplete w **jednej pracy**, na **jednych danych**
- Polski dataset zapytań wyszukiwania (literówki + synonimy + intencje) — można udostępnić
- Pomiar "rozumienia intencji" jako osobna metryka (nie tylko trafność)
- Routing zapytań do najlepszego silnika na podstawie długości / rodzaju (innowacja architektoniczna)

**Co wnosi**
Realnie lepszą wyszukiwarkę w aplikacji (widoczne demo na obronie — wpisujesz "monitor do gier" i widzisz różnicę) + pracę magisterską z gotowym datasetem zapytań i trzema implementacjami. Nadaje się jako trzon pracy.

---

---

# Tematy obliczeniowe (mało zależne od danych z seedera, oparte na zewnętrznych benchmarkach lub realnych obrazach/dokumentach)

> Wszystkie poniższe tematy mają wspólną cechę: **dane do badań nie pochodzą z seedera**. Zamiast tego korzystają z publicznych zbiorów danych (ImageNet, COCO, OWASP, OpenAI evals), benchmarków technicznych (czas odpowiedzi API, kompresja zdjęć), lub generują dane proceduralnie (testy obciążeniowe). Aplikacja SmartRecommender jest wtedy **platformą, na której to badamy**, a nie źródłem ocen jakości.

---

## Temat O1 — Prognozowanie sprzedaży z pełnym pipeline'em ML (EDA → preprocessing → modele klasyczne → modele głębokie → LLM jako prognosta)

**Krótki opis (po ludzku)**
Klasyczny problem data science: **mam historię sprzedaży i chcę przewidzieć, co się sprzeda za tydzień / miesiąc / kwartał**. W bazie mam już model `SalesForecast` i `ProductDemandForecast` — gotowy szkielet do wypełnienia.

Ale nie chcę zależeć od seedera (bo seeder generuje "fake" sprzedaż) — biorę **prawdziwe dane historyczne** z publicznych konkursów Kaggle:

- **Walmart Sales Forecasting** (45 sklepów × 99 produktów × 3 lata) — to jest klasyczny dataset prognozowania
- **Rossmann Store Sales** (1115 sklepów × 2.5 roku) — zwycięski model XGBoost znany z literatury
- **M5 Forecasting** (Walmart, 30k+ produktów) — najbardziej zaawansowany dataset, używany w benchmarkach
- **Online Retail II** (UK retailer, 2 lata transakcji) — dla porównania

Dane są **realne** (prawdziwa sprzedaż prawdziwego sklepu), **publiczne** (każdy może sprawdzić), **z benchmarkami** (wiadomo jak dobre były modele konkursowe). Wyniki nie zależą od seedera w żaden sposób.

**Pełny pipeline ML — to jest cel pracy, nie tylko "model"**:

1. **EDA (eksploracyjna analiza danych)** — wykresy sezonowości, autokorelacji, rozkładów, wykrywanie outlierów, identyfikacja świąt i promocji, analiza brakujących danych. To jest **pierwszy rozdział pracy** (ważny — pokazuje że rozumiem dane zanim je modeluję).

2. **Preprocessing** — imputacja braków (mean / median / KNN-imputer / MICE), kodowanie zmiennych kategorycznych (one-hot vs target encoding vs ordinal), skalowanie numeryczne (StandardScaler vs RobustScaler), tworzenie cech czasowych (dzień tygodnia, miesiąc, święto, dzień przed promocją, lag-1 / lag-7 / lag-28).

3. **Feature engineering** — to jest klucz do prognozowania:
   - cechy czasowe (Fourier dla sezonowości)
   - lagi sprzedaży (1, 7, 14, 28 dni temu)
   - statystyki ruchome (rolling mean / std / max z 7 i 28 dni)
   - cechy promocji (czy jest promocja + jaki rabat + ile dni do końca)
   - cechy zewnętrzne (pogoda jeśli dataset ma, święta z `holidays` Python lib)

4. **Modele — pięć klas porównujemy**:
   - **Naiwne**: średnia / ostatnia wartość / sezonowy naive
   - **Statystyczne**: ARIMA, SARIMA, Exponential Smoothing (Holt-Winters), Prophet (Facebook)
   - **Klasyczne ML**: Linear Regression, Random Forest, XGBoost, LightGBM, CatBoost
   - **Głębokie uczenie**: LSTM, GRU, Temporal Fusion Transformer (TFT), N-BEATS
   - **LLM jako prognosta**: GPT/Bielik dostaje historię sprzedaży w prompcie + kontekst ("to był weekend Black Friday") i ma zwrócić prognozę. Nowy nurt w literaturze — **time-series with LLMs** (TimeGPT, Chronos od Amazon).

5. **Ewaluacja** — RMSE, MAE, MAPE, sMAPE, **WMAPE** (weighted by sales) na zbiorze testowym (ostatnie 3 miesiące) + **time-based cross-validation** (rolling origin), nie standardowy K-fold.

6. **Wdrożenie** — najlepszy model wpina się w aplikację (`SalesForecast`, `ProductDemandForecast` zapełnia automatycznie), endpoint `GET /api/forecast/{product_id}` zwraca prognozę.

**Gdzie LLM się przydaje**
- **LLM jako prognosta** (główny eksperyment, nowinka): Chronos, TimeGPT, lub Bielik z dobrym promptem na szeregach czasowych
- **LLM do EDA**: model dostaje statystyki opisowe i pisze tekstowy raport "co widać w tych danych" — porównujemy z ręcznym opisem analityka (czy LLM łapie te same insighty)
- **LLM do feature engineering**: pytamy "jakie cechy zaproponowałbyś dla tego problemu" i porównujemy z literaturą + intuicją

**Gdzie to siedzi w kodzie**
- Modele `SalesForecast`, `ProductDemandForecast`, `Sale`, `Order`, `OrderProduct` z `models.py`
- Nowy moduł: `home/forecasting/` (pipeline ML w stylu scikit-learn — `Pipeline` + `ColumnTransformer`)
- Notebooks: `notebooks/01_eda.ipynb`, `02_preprocessing.ipynb`, `03_models.ipynb`, `04_llm_forecasting.ipynb`
- Endpoint: `GET /api/forecast/?product_id=X&horizon=7` — zwraca prognozę z confidence interval
- Panel admina: wykres prognozy obok każdego produktu

**Cel badawczy**
Zbudować pełny pipeline prognozowania sprzedaży na publicznych datasetach Kaggle i porównać pięć klas modeli (naiwne / statystyczne / klasyczne ML / głębokie / LLM) pod kątem dokładności (WMAPE), kosztu treningu, kosztu inferencji i interpretowalności — wskazać który model do której sytuacji.

**Hipotezy**
- H1: XGBoost / LightGBM po dobrym feature engineeringu bije LSTM o ≥3 punkty WMAPE — bo "ręczne" cechy lagów + sezonowości są lepsze niż to, co LSTM wyciąga sam
- H2: Prophet wygrywa **prostotą** (zero feature engineering, kilka linii kodu) i osiąga ≥85% wyniku XGBoost — czyli "wystarczy jeśli nie chcesz się męczyć"
- H3: LLM jako prognosta (Chronos lub Bielik z promptem) **bez fine-tuningu** osiąga ≥80% wyniku XGBoost — co jest zaskakująco dobre na zero-shot
- H4: Temporal Fusion Transformer (TFT) bije XGBoost o ≥1pp WMAPE, ale wymaga 50× więcej czasu treningu — opłacalny tylko dla krytycznych prognoz
- H5: LLM piszący raport EDA łapie ≥70% insightów które łapie analityk-człowiek (mierzymy na ręcznie oznaczonej liście insightów dla 3 datasetów)
- H6: Czasowy CV (rolling origin) daje istotnie inne wyniki niż standardowy K-fold — błąd K-fold jest **niedoszacowany** o 30%+ (wyciek z przyszłości)

**Innowacyjność**
- **Pełny pipeline w jednej pracy** — większość prac mag. robi tylko jedno (np. tylko XGBoost albo tylko LSTM); ja porównuję 5 klas
- **LLM jako prognosta szeregów czasowych** — gorący temat 2024/2025 (Chronos od Amazon, TimeGPT od Nixtla), praktycznie nieobecny w polskich pracach mag.
- **LLM do automatyzacji EDA** — bardzo świeży nurt (data analyst agents), pierwsza ewaluacja na polskim e-commerce
- **Time-based CV jako wymóg metodologiczny** — większość prac używa K-fold i podaje zaniżony błąd
- Reprodukowalny pipeline (skrypty + notebooki + zapisane modele) na publicznych datasetach

**Co wnosi**
Pełny pipeline ML na realnych, publicznych danych — od EDA przez preprocessing, feature engineering, modele klasyczne, głębokie, aż po najnowsze LLM. Bez seedera (dane Kaggle są obiektywne i z benchmarkami). Aplikacja jest tu **platformą wdrożenia** najlepszego modelu (`SalesForecast` + endpoint + panel admina), a sama praca naukowa toczy się na danych zewnętrznych. Trzon pełnoprawnej pracy magisterskiej.

---

## Temat O2 — Przewidywanie odejścia klientów (customer churn prediction) z pełnym pipeline'em ML i wyjaśnialnością (XAI + LLM)

**Krótki opis (po ludzku)**
Klasyczny problem w e-commerce i bankowości: **który klient zaraz przestanie kupować i jak go zatrzymać**. W bazie mam już model `RiskAssessment` z gotowym typem `customer_churn` — szkielet do wypełnienia.

Dane (publiczne, nie z seedera):
- **Telco Customer Churn** (IBM, Kaggle) — 7000 klientów, 21 cech, klasyczny benchmark
- **Bank Customer Churn** (Kaggle) — 10 000 klientów, etykiety odejść
- **E-commerce Customer Churn** (Kaggle / UCI) — najbardziej pasuje do naszego sklepu
- **Online Retail II** — można sztucznie zdefiniować churn (klient nie kupił przez 90 dni = odszedł)

Pełny pipeline (to jest tym razem **klasyfikacja binarna**, nie regresja jak w O1):

1. **EDA** — rozkład cech między churnowymi i nie-churnowymi klientami, korelacje, wykresy violin/box, identyfikacja cech najbardziej różnicujących, analiza balansu klas (churn to typowo 10–25%, czyli niezbalansowane)

2. **Preprocessing + radzenie sobie z niezbalansowaniem klas**:
   - **SMOTE** (Synthetic Minority Over-sampling), ADASYN, klasyczny oversampling/undersampling
   - **Class weights** w modelach
   - Porównanie który schemat lepszy — to jest osobny eksperyment

3. **Feature engineering** — RFM (Recency, Frequency, Monetary), entropia kategorii zakupów, trend zakupów (rosną / spadają), liczba opinii, średni sentyment, dni od ostatniej interakcji

4. **Modele — pięć klas porównujemy**:
   - **Klasyczne**: Logistic Regression, Decision Tree, Random Forest, XGBoost, LightGBM, CatBoost
   - **Głębokie**: MLP, TabNet, FT-Transformer (transformery dla danych tabelarycznych)
   - **AutoML**: H2O AutoML, AutoGluon — które same dobierają model i hiperparametry
   - **LLM jako klasyfikator**: Bielik dostaje profil klienta opisany słowami ("klient kupił 5 razy, ostatnio 60 dni temu, średnia wartość 200 zł, 2 reklamacje") i decyduje czy odejdzie + uzasadnia dlaczego
   - **Hybryda**: XGBoost + LLM dla niepewnych przypadków (gdy XGBoost zwraca prawdopodobieństwo 0.4–0.6, pyta LLM)

5. **Wyjaśnialność (XAI) — drugi rdzeń pracy obok dokładności**:
   - **SHAP** values — które cechy wpłynęły na decyzję per-klient (lokalne) i globalnie
   - **LIME** — lokalne wyjaśnienia
   - **Permutation importance** — globalne ważności cech
   - **LLM jako "tłumacz"**: SHAP zwraca liczby, LLM przerabia je na zdanie ("ten klient prawdopodobnie odejdzie głównie z powodu spadku częstotliwości zakupów w ostatnich 30 dniach i 2 reklamacji bez odpowiedzi")
   - Pytanie badawcze: **czy LLM-tłumaczenia są zgodne z SHAP** i czy są **zrozumiałe dla nie-technicznego managera**

6. **Ewaluacja** — Accuracy (mało użyteczne dla niezbalansowanych), **AUC-ROC**, AUC-PR, F1, **Recall na klasie pozytywnej** (najważniejsze — chcemy wyłapać churnowych), **Cost-sensitive metrics** (ile kosztuje pomyłka FP vs FN)

7. **Wdrożenie** — endpoint `GET /api/customer/{id}/churn-risk` zwraca prawdopodobieństwo + 3 najważniejsze przyczyny + sugestię akcji ("wyślij rabat 10%"). Panel admina pokazuje listę klientów wysokiego ryzyka.

**Gdzie LLM się przydaje**
- **LLM jako klasyfikator** (zero-shot) — porównanie z trenowanymi modelami
- **LLM tłumaczy SHAP** na zdania zrozumiałe dla biznesu — eksperyment XAI
- **LLM proponuje akcję retencyjną** ("jaki rabat zaproponować temu klientowi") — może być element pracy

**Gdzie to siedzi w kodzie**
- Model `RiskAssessment` z typem `customer_churn` z `models.py`
- Modele `User`, `Order`, `OrderProduct`, `Opinion`, `Complaint`, `UserPurchasePattern` jako źródła cech (tylko do **wdrożenia** najlepszego modelu, nie do badań — tam Kaggle)
- Nowy moduł: `home/churn/` (preprocessing + modele + XAI + LLM)
- Notebooks: `01_eda_churn.ipynb`, `02_preprocessing_imbalance.ipynb`, `03_models.ipynb`, `04_xai_shap.ipynb`, `05_llm_explanations.ipynb`
- Endpoint: `GET /api/customer/{id}/churn-risk` zwraca JSON z prawdopodobieństwem + przyczynami + akcją
- Panel admina: zakładka "Klienci wysokiego ryzyka"

**Cel badawczy**
Zbudować pełny pipeline predykcji churn na publicznych datasetach Kaggle z naciskiem na **wyjaśnialność**, porównać pięć klas modeli + cztery techniki radzenia sobie z niezbalansowaniem, ocenić czy LLM jako klasyfikator i jako tłumacz SHAP może realnie zastąpić data analyst'a w tej dziedzinie.

**Hipotezy**
- H1: XGBoost / LightGBM bije Logistic Regression o ≥5pp AUC-ROC, ale LogReg jest **bardziej interpretowalny** (współczynniki + odds ratio) — kompromis interpretowalność vs jakość
- H2: SMOTE pomaga modelom liniowym (LogReg) ale nie pomaga modelom drzewiastym (XGBoost) — bo te ostatnie radzą sobie z niezbalansowaniem przez `class_weight`
- H3: LLM (Bielik 11B) jako zero-shot klasyfikator osiąga ≥80% AUC trenowanego XGBoost — to jest "darmowa" jakość bez treningu (przy koszcie inferencji)
- H4: Hybryda XGBoost + LLM dla niepewnych przypadków poprawia recall klasy pozytywnej o ≥3pp przy podobnym precision — czyli LLM dobrze rozróżnia trudne przypadki
- H5: LLM-tłumaczenia SHAP są zgodne z liczbami SHAP w ≥85% przypadków (mierzymy ręcznie na 100 losowo wybranych klientach), ale są **zrozumialsze dla nie-technicznego managera** (mierzymy ankietą na 5 osobach)
- H6: TabNet / FT-Transformer **NIE bije** XGBoost na danych tabelarycznych — replikacja typowego wniosku z literatury (Borisov et al. 2022) na nowym datasecie

**Innowacyjność**
- **Pełny pipeline z naciskiem na XAI** — większość prac mag. robi tylko klasyfikację, bez wyjaśnialności
- **LLM jako tłumacz SHAP** na zdania biznesowe — bardzo świeży nurt 2024/2025 (interpretable AI + LLMs)
- **LLM jako klasyfikator zero-shot** vs trenowany model — replikuje aktualny spór w literaturze
- **Pomiar zrozumiałości wyjaśnień ankietą** — element ludzki, rzadki w pracach mag.
- **Replikacja Borisov 2022** ("XGBoost still wins on tabular") na nowych danych — element nauki replikacyjnej
- Reprodukowalny pipeline na publicznych datasetach + udostępnione notebooki

**Co wnosi**
Pełny pipeline ML z mocnym akcentem na **wyjaśnialność** + LLM w trzech rolach (klasyfikator / tłumacz / doradca akcji). Niezależny od seedera (Kaggle). Bardzo praktyczny dla biznesu (działa od razu na danych klienta + manager rozumie czemu). Nadaje się jako trzon pracy mag.

---

## Temat O3 — Wielowymiarowa analiza opinii produktowych z LLM (sentyment + aspekty + emocje + kontrowersyjność + automatyczne moderowanie)

**Krótki opis (po ludzku)**
W bazie jest model `Opinion` (treść + rating). Klasyczna analiza sentymentu z mojej inżynierki działa **prymitywnie** — mówi tylko czy opinia jest pozytywna / negatywna / neutralna, na podstawie słownika Liu (2012). Tu robimy **dużo więcej** i to jest klasyczna praca **NLP / data science / LLM** — dane są **publiczne** (Amazon Reviews, IMDB, Yelp), a aplikacja jest platformą wdrożenia.

Pięć zadań NLP na **tej samej** treści opinii (pełen pipeline analizy tekstu):

1. **Sentyment fine-grained** (5 klas: bardzo negatywne / negatywne / neutralne / pozytywne / bardzo pozytywne) zamiast 3 klas
2. **Aspect-Based Sentiment Analysis (ABSA)** — wykryć **o jakim aspekcie** klient pisze: "Bateria świetna, ale ekran kiepski" → `bateria: pozytywny, ekran: negatywny`. Aspekty wyciągamy automatycznie z tekstu
3. **Detekcja emocji** (radość / złość / smutek / strach / zaskoczenie / wstręt — Ekman 1992): "Jestem wkurzony że paczka nie przyszła" → `złość`. Inny sygnał niż sentyment (negatywny może być ze złości lub smutku)
4. **Detekcja kontrowersyjności / fake review** — opinia ekstremalnie pozytywna od użytkownika z 1 zakupem; opinia kopiuje treść innej; opinia ma znaki astroturfingu (zbyt formalna, bez błędów, nieludzko spójna). Klasyfikator binarny "podejrzana / autentyczna"
5. **Automatyczne moderowanie** — opinie zawierające wulgaryzmy, obraźliwy język, dane osobowe (numer telefonu, email), spam (link do innego sklepu) → flagowane do moderacji

Porównanie metod (każde zadanie testowane w 4 podejściach):

- **Słownikowe** (jak moja inżynierska — Liu 2012, polskie słowniki sentymentu z CLARIN-PL) — szybkie, deterministyczne, słabe w niuansach
- **Klasyczne ML** (TF-IDF + LogReg / SVM, fastText, LSTM z glove embeddings) — wymagają oznaczonych danych
- **Modele transformerowe pre-trained** (HerBERT, polish-roberta-base, XLM-RoBERTa) — fine-tuning na zadaniu, dobre wyniki
- **LLM** (Bielik 11B zero-shot i few-shot) — bez treningu, jeden prompt na wszystko

**Dane do badań — niezależne od seedera**

- **Amazon Reviews 2023** — 30M opinii (en) z aspektami i ratingami, klasyczny benchmark NLP
- **PolEmo 2.0** — 8000 polskich opinii z 4-klasowym sentymentem, **publiczny polski dataset z CLARIN-PL**
- **Allegro Reviews** (Allegro/HerBERT) — polskie opinie produktowe z ratingami
- **SemEval-2014 ABSA** — benchmark dla aspect-based sentiment, używany w setkach prac
- **Yelp Reviews Polarity** — duży angielski dataset

To są **realne, oznaczone, publiczne** dane — wynik pracy nie zależy od seedera. Aplikacja używa najlepszego modelu na opiniach z `Opinion`, ale ewaluacja jakości toczy się na zewnętrznych benchmarkach.

**Gdzie LLM się przydaje (w wielu rolach)**
- **LLM zero-shot na 5 zadaniach** (sentyment 5-klasowy, ABSA, emocje, kontrowersyjność, moderacja) — porównanie z trenowanymi modelami
- **LLM jako data augmenter** — generuje syntetyczne opinie negatywne (jest ich mało) żeby zbalansować klasy
- **LLM do auto-oznaczania danych** — bierzemy nieoznaczone opinie z `Opinion`, LLM je etykietuje, na tym trenujemy lekki model (knowledge distillation)
- **LLM jako orchestrator** — jeden prompt zwraca JSON ze **wszystkimi 5** zadaniami naraz, porównanie z 5 osobnymi modelami

**Gdzie to siedzi w kodzie**
- Model `Opinion` z `models.py`, `SentimentAnalysis`, `ProductSentimentSummary`
- Stara analiza w `custom_recommendation_engine.py::CustomSentimentAnalysis` (baseline słownikowy)
- Nowy moduł: `home/nlp/` (5 zadań × 4 metody)
- Notebooks: `01_eda_reviews.ipynb`, `02_preprocessing_polish.ipynb`, `03_models.ipynb`, `04_llm_zeroshot.ipynb`, `05_distillation.ipynb`
- Endpoint: `POST /api/opinion/{id}/analyze-full/` zwraca JSON z 5 wynikami
- Panel admina: zakładka "Opinie do moderacji" + dashboard sentymentu per produkt + per aspekt

**Cel badawczy**
Zbudować i porównać pełny pipeline NLP do wielowymiarowej analizy opinii produktowych (sentyment + aspekty + emocje + autentyczność + moderacja) na **polskich i angielskich** publicznych benchmarkach, ocenić czy LLM zero-shot może zastąpić wyspecjalizowane modele transformerowe i czy auto-oznaczanie LLM pozwala wytrenować mały tani model konkurencyjny do dużego LLM.

**Hipotezy**
- H1: HerBERT (polski transformer) po fine-tuningu bije Bielik zero-shot na PolEmo 2.0 o ≥5pp F1 — czyli mały specjalistyczny model > duży generalistyczny **gdy są dane treningowe**
- H2: Bielik zero-shot bije słownik Liu 2012 o ≥15pp F1 na PolEmo — "darmowy" zysk w niuansach językowych
- H3: ABSA jest **dużo trudniejszy** niż sentyment ogólny — najlepszy model osiąga F1 ≤0.65 (vs 0.85 dla sentymentu)
- H4: Auto-oznaczanie 10 000 opinii Bielikiem + trening HerBERT (knowledge distillation) daje wynik na poziomie ręcznego oznaczania 1000 opinii — czyli **10× redukcja kosztu oznaczania**
- H5: LLM jako orchestrator (jeden prompt → 5 wyników) jest 3× szybszy niż 5 osobnych modeli, ale traci 2–5pp F1 na każdym zadaniu osobno — kompromis prędkość vs jakość
- H6: Detekcja fake review na danych syntetycznych (LLM generuje fake opinie, klasyfikator je rozpoznaje) osiąga F1 ≥0.9 — czyli da się wykrywać astroturfing automatycznie
- H7: Polski model (HerBERT) > model wielojęzyczny (XLM-RoBERTa) na polskich opiniach o ≥3pp F1 — replikacja typowego wyniku z literatury

**Innowacyjność**
- **Pięć zadań NLP w jednym pipeline'ie** na tych samych opiniach — większość prac robi jedno
- **LLM w czterech rolach** (klasyfikator / data augmenter / nauczyciel do distillation / orchestrator)
- **Knowledge distillation z LLM do małego modelu** — gorący temat 2024/2025, mało prac na polskich danych
- **Detekcja fake review z syntetycznymi danymi z LLM** — eleganckie rozwiązanie problemu braku oznaczonych danych
- **Polskie + angielskie benchmarki w jednej pracy** — pokazuje, że pipeline jest językowo agnostyczny
- Reprodukowalne notebooks + udostępnione modele po fine-tuningu

**Co wnosi**
Pełny pipeline NLP od EDA przez preprocessing, fine-tuning transformerów, po LLM w wielu rolach. Niezależny od seedera (publiczne benchmarki). LLM jest **głównym bohaterem** w wielu rolach, nie tylko jednej. Praktyczne wdrożenie w aplikacji (panel admin: moderacja + dashboard ABSA) + naukowa praca o **distillation** i **synthetic data**. Trzon pełnoprawnej pracy mag. — bardzo dużo treści na 80+ stron.

---

## Wybór tematu — szybka mapa

| Wariant | Trzon pracy | Podrozdziały / dodatki |
|---|---|---|
| **Wariant A (rekomendowany dla rec-sys)** | **D10** (klasyka + opisy + LLM) | D2 (tuning), D5 (skalowalność), D4 (jako wspólny z Piotrem) |
| **Wariant B (węższy rec-sys)** | D1 + D9 | D3 jako rozszerzenie, D2 jako tuning |
| **Wariant C (minimalny rec-sys)** | D1 + D2 | bez LLM i RAG — bezpieczne, ale mało innowacyjne |
| **Wariant D (LLM-centric rec-sys)** | D3 + D9 | D1 jako baseline, D5 dla LLM latency |
| **Wariant E (NLP-aplikacyjny)** | **N1 (reklamacje)** | N3 (wyszukiwarka) jako rozdział uzupełniający |
| **Wariant F (anomaly + NLP)** | **N2 (anomalie)** | N1 (reklamacje) jako uzupełnienie tematycznie blisko |
| **Wariant G (UX/wyszukiwarka)** | **N3 (wyszukiwarka)** | D9 jako baza techniczna (wektory współdzielone) |
| **Wariant H (data science / forecasting)** | **O1 (prognozowanie sprzedaży)** | O2 (churn) jako rozdział uzupełniający — obie predykcyjne, dwa różne taski |
| **Wariant I (data science / churn + XAI)** | **O2 (churn + XAI + LLM)** | O3 (NLP opinii) jako rozdział uzupełniający — XAI w obu |
| **Wariant J (NLP / LLM-heavy)** | **O3 (analiza opinii — 5 zadań NLP)** | O2 (churn) jako rozdział uzupełniający — wspólny temat XAI z LLM |
| **Wariant K (rekomendowany ogólnie — dwa filary)** | **O1 (forecasting) + O3 (NLP opinii)** | jeden ML tabelaryczny, jeden NLP z LLM — pełny przekrój data science |
| **Wariant L (najbezpieczniejszy)** | **O1 (forecasting) + O2 (churn)** | dwa klasyczne ML pipeline'y na publicznych Kaggle — minimalne ryzyko niewyjścia |
