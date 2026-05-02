# Dawid Olko — opis tematów D1, D2, D3, D4, D5, D9 (wersja rozszerzona)

Dokument odpowiada na pytania: **co dokładnie jest badane**, **z czym porównujesz**, **co liczysz (metryki)**, **jak wygląda fuzja w D1 (w tym wyłączanie metod)**. Spójny z repozytorium *SmartRecommender*.

---

## Wspólny protokół (wszystkie tematy z ewaluacją rankingową)

| Element | Konkret |
|--------|--------|
| **Zbiór danych** | `seed_research` (lub równoważny): persony, sensowne zamówienia, opinie powiązane z zakupem. **Ta sama wersja** bazy dla wszystkich metod w porównaniu. |
| **Zadanie predykcji** | Dla użytkownika z **zbioru testowego**: zbuduj ranking top-K produktów **używając wyłącznie informacji dostępnych przed końcem okna treningowego**; sprawdź, czy **produkty faktycznie kupione przez tego użytkownika w oknie testowym** pojawiają się wysoko na liście. |
| **Podział** | **Temporal split** — np. ostatnie 20% **osi czasu** zamówień = test (ustal raz w pracy: np. 15% / 20% / 25% i uzasadnij). |
| **Parametry raportowane** | Ustal **K** (np. **K=10**) i **ew. K=5** dla czułości; wszystkie metody ten sam K. |
| **Metryki (zawsze raportowane przy porównaniu rankerów)** | **Precision@K**, **Recall@K**, **NDCG@K**, **MAP** (lub wyłącznie Precision+NDCG jeśli promotor woli prostotę); dodatkowo **coverage** (% produktów z katalogu kiedykolwiek w rekomendacjach) i opcjonalnie **diversity**. |
| **Baseline obowiązkowy** | **Popularność** (np. top-K najczęściej kupowanych w train) — żebyś nie porównywał tylko „swój algorytm z drugim swoim”. Opcjonalnie **losowy** ranker w obrębie kategorii użytkownika (słabszy baseline). |

---

## D1 — Łączenie metod (CF + Apriori + sentyment) vs metody pojedyncze

### Odpowiedź na Twoje pytanie (jak to ma działać)

**Tak:** w eksperymencie **porównujesz nie tylko „trzy osobno'' z ''trzy razem''**. Sensowny zestaw to:

1. **Trzy metody pojedyncze:** wyłącznie CF, wyłącznie Apriori, wyłącznie kanał sentymentowy (jedna ustalona reguła rankingu z opinii).
2. **Trzy fuzje dwuskładnikowe** (pare): CF+Apriori, CF+Sentyment, Apriori+Sentyment — **to już jest fuzja z wyłączonym trzecim kanałem**.
3. **Jedna fuzja trójkanałowa:** CF+Apriori+Sentyment.
4. **Baseline:** popularność (+ opcjonalnie los).

**Fuzja nie musi zawsze używać wszystkich trzech metod.** W kodzie robisz np. `FusionRRF(active={"cf", "apriori"})` albo maskę bitową — **ablacja** (wyłączenie kanału) to normalna część pracy: pokazujesz, **który kanał jest zbędny albo szkodliły** w danej strategii łączenia.

Dodatkowo możesz porównać **dwie strategie łączenia** na tej samej rodzinie składowych (np. RRF vs Borda vs ważona średnia score) — to drugi wymiar eksperymentu; jeśli robi Ci się za dużo runów, **zacznij od RRF + jedna para + trójka**, potem rozszerz.

---

### Zadania badawcze (2–3 konkretne)

1. **Zadanie B1 (główne):** Czy **najlepsza** konfiguracja fuzji (spośród wybranych: pary + trójka) daje **istotnie wyższy** NDCG@K i Precision@K niż **najlepsza pojedyncza** metoda spośród {CF, Apriori, Sentyment} na **tym samym** splitcie czasowym?
2. **Zadanie B2 (ablacja):** Dla ustalonej metody fuzji (np. RRF): **który podzbiór kanałów** minimalizuje stratę jakości względem pełnej trójki? (np. czy Apriori+CF ≈ pełna trójka → sentyment w praktyce nie dokłada?)
3. **Zadanie B3 (vs. naiwnie):** Czy **każda** sensowna fuzja pokonuje baseline **popularności**? (Jeśli nie — masz ważny wniosek o sile heurystyk na waszych danych.)

---

### Co porównujesz (macierz wykonawcza)

| ID | Konfiguracja | Opis |
|----|----------------|------|
| B0 | Popularność | Ranking z liczby zakupów w train |
| S1 | CF-only | Tylko collaborative filtering (Twoja logika + `ProductSimilarity`) |
| S2 | Apriori-only | Tylko reguły koszykowe (`ProductAssociation`, ustalony sposób score) |
| S3 | Sentyment-only | Jedna zamrożona reguła: np. ranking produktów wg opinii/sentymentu pod użytkownika |
| F12 | CF + Apriori | Fuzja; **bez** sentymentu |
| F13 | CF + Sentyment | Fuzja; **bez** Apriori |
| F23 | Apriori + Sentyment | Fuzja; **bez** CF |
| F123 | Pełna trójka | Wszystkie kanały |

Opcjonalnie: **F123-RRF** vs **F123-Borda** (drugi wymiar).

**Liczba runów:** minimum sensowne to ok. **8 systemów** (B0,S1,S2,S3,F12,F13,F23,F123) × ta sama ewaluacja.

---

### Co jest mierzone

- **Jakość rankingu:** Precision@K, Recall@K, NDCG@K, MAP (co najmniej **NDCG@K + Precision@K** muszą być w pracy).
- **Koszt obliczeniowy (minimum podstawowe):** średni lub sumaryczny **czas** wygenerowania rekomendacji dla zbioru testowego (per konfiguracja), żeby obronić, że fuzja nie jest „darmowa”.
- **Opcjonalnie (mocniejsza praca):** test Friedman + post-hoc na **użytkownikach testowych** (czy różnice między systemami są statystycznie spójne).

---

### Protokół (jedno zdanie na obronę)

„**Jeden split czasowy, jeden K, ten sam kod `metrics.py`, osiem nazwanych konfiguracji rankera; w fuzji kanały mogę włączać i wyłączać — to jest ablacja, nie osobna magia.**”

### Biblioteki

numpy, Django ORM; scipy.stats (opcjonalnie). RRF/Borda — implementacja własna (krótki moduł).

### kNN / k-means

Rdzeń D1: **nie**. (Opcjonalny dodatek: kNN do kandydatów przed fuzją — poza minimalnym zakresem D1.)

---

## D2 — Wpływ hiperparametrów (CF, Apriori, sentyment) na jakość **i** czas

### Zadania badawcze

1. **Zadanie B1:** Dla **Apriori**: jak **min_support** i **min_confidence** wpływają na NDCG@K i na **czas przeliczenia** oraz na **liczbę reguł** w `ProductAssociation`? Gdzie jest „kolano” krzywej (Pareto: jakość vs czas)?
2. **Zadanie B2:** Dla **CF**: jak **próg podobieństwa** (zapis podobnych par) wpływa na jakość i na **rozmiar** `ProductSimilarity` oraz czas regeneracji?
3. **Zadanie B3 (sentyment):** Dla **jednej rodziny** reguł (np. sposób agregacji opinii → score produktu): jak 1–2 parametry (np. minimalna liczba opinii, waga recency) zmieniają ranking i metryki?

---

### Co porównujesz

- **Nie porównujesz „metod różnych rodzajów''** jak w D1 — porównujesz **warianty tej samej metody** z różnymi parametrami + punkt **referencyjny = domyślne ustawienia z inżynierki** (baseline wewnętrzny).
- Wyjście: **tabele** (parametr → metryki → czas → rozmiar DB) + **wykresy Pareto**.

---

### Co jest mierzone

- Metryki jak w D1 (te same K i split) — **dla każdego zestawu hiperparametrów**.
- **Czas:** pełna regeneracja Apriori / CF (sekundy lub minuty).
- **Rozmiar modelu:** liczba wierszy w `ProductAssociation`, liczba par w `ProductSimilarity` (CF).

---

### Biblioteki

**optuna** lub siatka ręczna; `time`, logging; Django.

### kNN / k-means

**Nie.**

---

## D3 — LLM jako główny kanał (re-ranking na liście kandydatów)

### Cel pracy i zakres badawczy

**Cel:** sprawdzić, czy **model językowy użyty wyłącznie do przestawienia kolejności** już wybranych produktów poprawia **jakość rankingu** (w sensie metryk z wspólnego protokołu) względem **tej samej listy kandydatów bez LLM** — oraz jaki jest **koszt operacyjny** (czas odpowiedzi, błędy formatu, halucynacje ID).

**Co jest *w* zakresie:** jeden spójny **temporal split**, ustalone **K**, dla każdego użytkownika testowego: (1) zbudowanie listy kandydatów **C** (zamrożony generator — patrz niżej), (2) wariant **G0** = ranking z C bez LLM, (3) wariant **G1** = **te same elementy** zbioru kandydatów **C**, tylko **inna kolejność** po LLM + walidacja, (4) porównanie metryk i logów błędów.

**Co jest *poza* zakresem (żeby nie rozlać tematu):** LLM nie wybiera produktów spoza C; nie badasz „pełnego chatbota’’; nie musisz wdrażać produkcyjnego UI — wystarczy skrypt ewaluacyjny + ewentualnie jeden endpoint diagnostyczny. Porównanie z **RAG (D9)** jest osobne: tam **zmienia się sposób znalezienia** kandydatów (embedding + sąsiedzi), tu **kandydaci są dane z góry**.

### D3 vs D9 — jedna linijka na pamięć

| | **D3** | **D9** |
|--|--------|--------|
| Skąd kandydaci? | Z **istniejących** rankerów / reguł / CF (generator **bez** embeddingów jako rdzenia). | Z **retrievalu** po embeddingach opisów produktów (**kNN** w przestrzeni wektorów). |
| Rola LLM | **Tylko** permutacja (re-rank) **pewnej** listy ID. | **Retrieval może być bez LLM (R1);** z LLM (R2) model **interpretuje** już pobrane opisy i zwraca podzbiór / kolejność **spośród pobranych**. |

---

### Mapowanie na aplikację SmartRecommender

**Dziś:** np. `RecommendedProductsAPIView` zwraca produkty posortowane po `score` z `UserProductRecommendation` (lub fallback). **D3 w wdrożeniu** to ten sam kontrakt API (lista produktów w JSON), z opcjonalnym krokiem *po* wyliczeniu kandydatów: wywołanie Ollamy, walidacja permutacji ID, **fallback** do kolejności G0 przy błędzie.

---

### Przepływ krok po kroku (ewaluacja offline — rdzeń pracy)

1. **Przygotowanie (raz na eksperyment)**  
   - Zamroź `seed_research`, temporal split, listę użytkowników testowych.  
   - Ustal **generator kandydatów G0**: np. top **N=40** produktów z Twojego CF+agregacja score (lub najlepsza para z D1 — ale **jedna** definicja na cały eksperyment D3).  
   - Dla każdego usera **u** w teście, w momencie „predykcji” (tylko dane z train): policz listę **`C(u) = [id_1, …, id_N]`** + opcjonalnie krótkie cechy (nazwa, kategoria) do promptu.

2. **Ścieżka G0 (baseline bez LLM)**  
   - Posortuj `C(u)` według istniejącego score z generatora (lub oryginalnej kolejności — **opisz w pracy, którą wersję uznajesz za G0**).  
   - Weź **top-K** (np. K=10). To jest ranking **R_G0(u)**.

3. **Ścieżka G1 (z LLM)**  
   - Zbuduj **prompt**: identyfikacja użytkownika (skrót historii z train), lista **tylch samych** `id` co w `C(u)` + minimalne metadane; instrukcja: zwróć **JSON** z permutacją **wyłącznie** tych ID (np. `ordered_ids`).  
   - Wywołaj model (Ollama).  
   - **Parse + Pydantic:** jeśli struktura zła → **retry** (ustal limit, np. 2) → przy porażce **fallback: R_G0(u)**.  
   - **Walidacja zbioru:** każdy ID w odpowiedzi ∈ `C(u)`, brak duplikatów, liczba zgodna — jeśli nie: naprawa (ucięcie / odrzucenie obcych ID) albo fallback do G0 — **musisz to opisać w metodyce**.  
   - Utwórz **R_G1(u)** = pierwsze K pozycji po walidacji.

4. **Ground truth**  
   - Z zamówień w **oknie testowym** weź zbiór produktów **relevantnych** dla **u** (np. wszystkie kupione w teście — jak w wspólnym protokole). To samo dla każdego systemu.

5. **Liczenie metryk**  
   - Dla każdego **u**: Precision@K, Recall@K, NDCG@K względem ground truth (jak w bloku wspólnym).  
   - Uśrednij po użytkownikach testowych → **tabela G0 vs G1** (+ ewentualnie G2 z innym modelem).

6. **Pomiary „jakości usługi’’** (osobna tabela)  
   - **Conformance rate:** % wywołań, w których pierwszy parse OK bez fallbacku.  
   - **Hallucination rate:** % wywołań, gdzie model zwrócił ID ∉ `C(u)` (przed naprawą).  
   - **Latency:** czas od wysłania promptu do gotowego `R_G1(u)` (średnia, mediana, **p95**) na ustalonym sprzęcie (np. MacBook M3 Pro).

---

### Przepływ krok po kroku (opcjonalnie: w produkcji)

1. Request HTTP (zalogowany user).  
2. Backend buduje `C(u)` jak w inżynierce.  
3. Jeśli flaga `use_llm_rerank=false` → zwróć G0 jak dziś.  
4. Jeśli `true` → wywołaj LLM; sukces → `ProductSerializer` w kolejności R_G1; błąd → ta sama odpowiedź co G0 + opcjonalnie `X-LLM-Fallback: 1` dla logów.

---

### Co dokładnie „zwraca’’ system

- **W pracy (offline):** nie „endpoint’’ jest wynikiem, tylko **macierz wyników** — metryki rankingowe + logi błędów + czasy — dla wariantów G0, G1, (G2).  
- **W API (jeśli zaimplementujesz):** ta sama **lista obiektów produktu** co teraz (`ProductSerializer`), **inna kolejność**; opcjonalnie pola diagnostyczne: `llm_used`, `rerank_ms` (tylko dla admina / dev).

**Czego D3 *nie* zwraca:** nowych produktów spoza katalogu; „wyjaśnień’’ dla usera — chyba że dodasz to poza minimalnym zakresem (wtedy opisz jako rozszerzenie).

---

### Zadania badawcze

1. **Zadanie B1:** Czy **średni** NDCG@K (i Precision@K) dla **G1** jest wyższy niż dla **G0** przy **identycznym** `C(u)` i identycznym splitcie?
2. **Zadanie B2:** Jak zmienia się jakość i **stabilność formatu** przy: różnych **modelach** (np. Bielik 7B vs 11B), **zero-shot vs few-shot**, różnej **długości kontekstu**?
3. **Zadanie B3 (jakość usługi):** Jaki jest **udział** odpowiedzi **nieważnych** (ID spoza kandydatów / zły JSON) i jak **fallback** na G0 zmienia **effective** latency i metryki „w produkcji symulowanej’’?

---

### Co porównujesz

| System | Opis |
|--------|------|
| G0 | Generator kandydatów **bez** LLM (baseline „przed LLM'') |
| G1 | G0 + **LLM re-rank** (ten sam seed promptu + walidacja Pydantic) |
| Opcjonalnie G2 | Inny model / inny prompt — ta sama procedura |

**Porównanie z inżynierką:** **opcjonalne** — jeśli promotor chce, dodajesz **G-extra:** najlepszy singleton z D1 na tym samym proteole.

---

### Co jest mierzone (skrót checklist)

- Jakość: **NDCG@K, Precision@K, Recall@K, MAP** (minimum jak w protokole).  
- **Conformance / halucynacje / retry** — liczone per wywołanie LLM.  
- **Latency:** G0 (bazowo krótki) vs G1 (dominuje LLM).  
- Opcjonalnie: **coverage / diversity** — jeśli permutacja zmienia eksplorację w obrębie C.

---

### Biblioteki

ollama / httpx, pydantic, Django.

### kNN / k-means

**Nie w rdzeniu.** Generator może być ten sam kanał co w D9 (np. kandydaci z retrievalu) — wtedy kNN jest **w generatorze**, a nie w „rdzeniu’’ samego D3; sens D3 i tak zostaje: **LLM tylko przestawia już znalezione ID**.

---

## D4 — Rekomendacja z **danych jawnych** (opinie/oceny) vs **ukryte** (Piotr)

### Zadania badawcze

1. **Zadanie B1:** Przy **identycznym** ground truth (przyszłe zakupy w teście): czy ranker **„tylko jawne''** (Opinion + Twoja logika sentymentu/agregacji) ma **wyższą / równą / niższą** NDCG@K niż ranker **„tylko ukryte''** (interakcje od Piotra)?
2. **Zadanie B2:** Dla **podgrup** (np. użytkownicy z małą vs dużą liczbą opinii): kto wygrywa — jawne czy ukryte?
3. **Zadanie B3 (opcjonalnie):** Czy **kombinacja** (prosta fuzja jawny + ukryty score) pokonuje oba źródła osobno? (wtedy D4 styka się z ideą D1, ale **porównanie strumieni danych** zostaje głównym wątkiem)

---

### Co porównujesz

- **System J:** ranking zbudowany **wyłącznie** z `Opinion`/ocen/sentymentu (Ty zamrażasz **jedną** formułę).
- **System U:** ranking zbudowany **wyłącznie** z `UserInteraction` (+ ewentualnie dwell) — implementacja Piotra.
- **Ten sam** temporal split, **ten sam** K, **ta sama** lista użytkowników testowych.
- Opcjonalnie **JU:** prosta fuzja dwóch list (np. RRF) — jako trzeci punkt.

---

### Co jest mierzone

- Metryki rankingowe standardowe.
- **Stratyfikacja:** metryki liczone **osobno** dla bucketów „liczba opinii użytkownika: 0–2 / 3–10 / 10+” (przykład — dostosuj do rozkładu w `seed_research`).

---

### Biblioteki

Django ORM, numpy; opcjonalnie scikit-learn jeśli robisz rozszerzenie kNN/k-means na profilu jawnych cech.

### kNN / k-means

**Opcjonalnie:** kNN na wektorze „kto podobnie oceniał”; k-means na cechach jawnych użytkownika — **nieobowiązkowe**.

---

## D5 — Skalowalność CF i Apriori

### Zadania badawcze

1. **Zadanie B1:** Jak **rosną** (względem liczby syntetycznych klientów / zamówień): **czas regeneracji** macierzy CF, **czas miningu** Apriori, **rozmiar** tabel `ProductSimilarity` i `ProductAssociation`?
2. **Zadanie B2:** Które **zapytania SQL** dominują czas przy największej skali — potwierdzenie `EXPLAIN ANALYZE`.
3. **Zadanie B3:** Czy **jakość rankingowa** (na **ustalonym** małym zbiorze testowym „referencyjnym'') **spada** przy większej skali z powodu rzadszych sygnałów per użytkownik — czy efekt jest pomijalny?

---

### Co porównujesz

- **Nie porównujesz algorytmów między sobą** jak w D1 — porównujesz **ten sam kod** uruchomiony na **serii baz** różnej skali (np. 50 / 100 / 200 / 400 klientów z seedera) przy **zamrożonym** protokole testowym (np. ten sam plik listy userów testowych lub ten sam procent czasu).

---

### Co jest mierzone

- **Czas** (sekundy): pełny pipeline przeliczenia CF i Apriori.
- **Pamięć / rozmiar:** liczba wierszy w tabelach, opcjonalnie RAM.
- **Jakość:** NDCG@K na **tym samym** (lub proporcjonalnie losowanym, ale opisanym) teście referencyjnym.

---

### Biblioteki

Django, psycopg (EXPLAIN), time, opcjonalnie memory_profiler.

### kNN / k-means

**Nie.**

---

## D9 — RAG na treści katalogu (embedding + retrieval + LLM)

### Cel pracy i zakres badawczy

**Cel:** sprawdzić, czy **rekomendacja oparta na treści katalogu** (opisy produktów → wektory → sąsiedzi) daje sensowny ranking w Twoim **temporal split**, oraz czy **dodanie LLM** do obróbki **już pobranych** fragmentów/opisów (klasyczny schemat RAG: retrieve-then-read) poprawia wynik względem **tylko retrievalu** (bez LLM) i względem **baseline popularności**.

**Co jest *w* zakresie:** (1) **indeks semantyczny** produktów z bazy (np. `name` + `description` + kategorie), (2) **zapytanie użytkownika** zbudowane **wyłącznie z informacji dostępnych w train** (historia zakupów / krótki profil tekstowy generowany deterministycznie z train — **opisz dokładnie** w pracy), (3) **kNN** po embeddingach → lista **k** kandydatów, (4) finalny ranking **top-K** dla metryk (to samo **K** co w D1/D3), (5) porównanie **R0 vs R1 vs R2** na tym samym ground truth.

**Co jest *poza* zakresem (typowo):** pełna produkcyjna wyszukiwarka Elasticsearch; fine-tuning modeli embeddingowych; wieloźródłowe indeksy (PDF, HTML spoza Twojego `Product`). Możesz to wymienić jako **pracę przyszłą**.

### D9 vs D3 — co robić w głowie

- **D9:** „**Skąd** wziąć sensownych kandydatów, jeśli chcę oprzeć się na **tekście katalogu**?” → embedding + **kNN**. LLM (R2) jest **po** pobraniu sąsiadów.  
- **D3:** „**Mam już** kandydatów (CF/reguły) — czy LLM **przestawiając** ich kolejność coś poprawia?” → **ten sam zbiór ID**, inna permutacja.

Możesz **złożyć** oba w jednym systemie (kandydaci z D9 → re-rank D3), ale **minimalne** prace magisterskie trzymają **D3 i D9 jako osobne eksperymenty**, żeby wnioski były czytelne.

---

### Przepływ krok po kroku — faza indeksu (raz / po zmianie katalogu)

1. Dla każdego produktu w katalogu (tym, który wchodzi w eksperyment): złóż **tekst źródłowy** (np. nazwa + opis + kategorie — stały szablon).  
2. **Embedding:** model `E` (np. sentence-transformers) → wektor **d**-wymiarowy.  
3. Zapisz wektor w **FAISS / pgvector / Qdrant** (jasny wybór w rozdziale implementacji).  
4. Zmierz **czas budowy indeksu** i **RAM / rozmiar** — to jest część D9 (koszt wdrożeniowy).

---

### Przepływ krok po kroku — inference **R1 (retrieval-only, bez LLM)**

1. Dla użytkownika testowego **u** (tylko dane train): zbuduj **tekst zapytania** **Q(u)** — przykłady: „Użytkownik kupił: [lista tytułów z train]”; lub krótki skonsolidowany opis wygenerowany regułami (ważne: **reprodukowalność**).  
2. **Embed:** `q = E(Q(u))`.  
3. **kNN:** pobierz **k** najbliższych produktów (k osiągalny hiperparametr, np. 20, 50).  
4. **Ranking bez LLM:** przypisz score = **podobieństwo cosinusowe** (lub odległość → monotoniczna transformacja) i weź **top-K** jako ranking **R_R1(u)**.  
5. Na tym samym ground truth co w protokole: licz metryki.

**Co „zwraca’’ R1 w aplikacji:** lista produktów (JSON jak dziś), kolejność wg podobieństwa do **Q(u)** — **bez** wywołania chat modelu. To już jest „mądry’’ rekomender tekstowy, tylko że **scoring = wektory**, nie LM.

---

### Przepływ krok po kroku — inference **R2 (RAG = R1 + LLM)**

1. Kroki 1–3 **identyczne jak R1** → masz **k** kandydatów + ich opisy (tylko te pobrane, nie cały katalog).  
2. Zbuduj **prompt**: **Q(u)** + **lista kandydatów** z krótkimi opisami + instrukcja: wybierz / uporządkuj **wyłącznie** podane `product_id` → JSON (np. `ordered_ids` lub `selected_ids` + ranks).  
3. Ollama / inny serwer LLM → parse **Pydantic**, walidacja ⊆ zbiór pobranych ID (jak w D3).  
4. **Fallback:** przy błędzie ustaw **R_R2(u) := R_R1(u)** (uczciwe porównanie — RAG „nie psuje’’ relative do retrieval-only).  
5. **Top-K** do ewaluacji — te same metryki co R1.

**Intuicja:** LLM czyta **tylko** to, co retrieval przyniósł („R” w RAG) i próbuje lepiej dopasować językowe niuanse; **nie** przeszukuje całej bazy.

---

### Przepływ krok po kroku — **R0 (baseline)**

- Ranking = top-K **najpopularniejszych** produktów w train (jak B0 w dokumencie).  
- **Po co:** żebyś nie „wygrał’’ tylko z najprostszą heurystyką przez przypadek małej próby.

---

### Co dokładnie jest mierzone (z interpretacją)

| Miara | Co znaczy w D9 |
|--------|----------------|
| **NDCG@K, Precision@K, Recall@K, MAP** | Ta sama semantika co w całym dokumencie: jak wysoko w **top-K** lądują produkty faktycznie kupione w oknie testowym. |
| **Czas indeksu** | Jednorazowy koszt po dodaniu/zmianie produktów. |
| **Czas zapytania R1** | Embed(u) + kNN + sort (bazowy latency retrievalu). |
| **Czas zapytania R2** | R1 + round-trip LLM (zazwyczaj dominuje). |
| **Recall@k (retrieval)** *(opcjonalnie)* | Frakcja pozycji z ground truth (test), która pojawia się w **zbiorze k** sąsiadów **zanim** LLM cokolwiek zrobi. Wymaga formalnej definicji: ground truth = pojedynczy następny produkt vs cały koszyk testowy — **wybierz jedną i trzymaj w całej pracy**. |

---

### Zadania badawcze

1. **Zadanie B1:** Czy **R2** (RAG) ma wyższy **NDCG@K** niż **R1** (retrieval-only) przy **tym samym** **k**, tym samym **E** i tym samym `Q(u)`?
2. **Zadanie B2:** Jak **model embeddingów** i **k** wpływają na (opcjonalny) **Recall@k** oraz na końcowy **NDCG@K**?
3. **Zadanie B3:** Czy **R1** i/lub **R2** biją **R0** (popularność)? Jeśli nie — opiszesz **cold start** i ograniczenia treści w katalogu.

---

### Co porównujesz

| System | Opis |
|--------|------|
| R0 | Popularność (jak B0) |
| R1 | **Retrieval-only:** embedding zapytania użytkownika → **kNN** po produktach → ranking bez LLM |
| R2 | **RAG:** R1 + **LLM** na pobranych opisach (walidacja ID, fallback → R1) |

Opcjonalnie R1 z **MMR** vs bez — jeśli retrieval zwraca zestaw zbyt podobnych wizualnie/semantycznie produktów i chcesz pokazać trade-off **diversity vs metryki**.

---

### Co „zwraca’’ system w API (intuicja)

- **R0 / R1 / R2:** nadal **`ProductSerializer`** (lista produktów).  
- **R2** może dodatkowo zwracać pole diagnostyczne „źródło: rag’’ lub embedding_id wersji indeksu — dla rozdziału o reproducibility.

**„Co to da’’ w sensie praktycznym:** jeśli R1/R2 > R0 na Twoich danych, masz argument za **szyciem rekomendacji do treści produktów** (SEO, długie opisy, atrybuty). Jeśli R2 ≈ R1, **LLM nie dokłada** przy Twoim **k** i promptach — też wartościowy wniosek (oszczędność GPU).

---

### Biblioteki

sentence-transformers + torch; FAISS / qdrant / chroma / **pgvector**; ollama + pydantic.

### kNN / k-means

- **kNN:** **tak, rdzeń D9** (sąsiedzi w przestrzeni embeddingów).
- **k-means:** opcjonalnie (IVF / analiza klastrów), nie wymagane.

---

## Tabela: skrót „co badam / z czym / co mierzę”

| Temat | Co badasz (sedno) | Z czym porównujesz | Co mierzysz (minimum) |
|-------|-------------------|--------------------|------------------------|
| **D1** | Czy fuzja wygrywa z pojedynczymi i z popularnością | S1,S2,S3, pary F12,F13,F23, F123, B0 | NDCG@K, Precision@K, MAP, coverage; czas |
| **D2** | Czułość na hiperparametry | Warianty parametrów vs default inżynierki | Metryki + czas + rozmiar DB |
| **D3** | Czy LLM poprawia ranking na tych samych kandydatach | G0 vs G1 (+ opc. modele) | Metryki + błędy JSON + latency |
| **D4** | Jawne vs ukryte przy tym samym teście | J vs U (+ opc. JU) | Metryki + stratyfikacja po liczbie opinii |
| **D5** | Jak skaluje się czas i rozmiar vs N użytkowników | Ta sama metoda na serii rozmiarów danych | Czas, wiersze w DB, metryki na ref. teście |
| **D9** | Czy RAG dokłada ponad retrieval | R0, R1, R2 | Metryki + czas indeksu/zapytania |

---

## Repozytorium (skrót)

- CF: `recommendation_views.py`, `ProductSimilarity` (collaborative).
- Apriori: `custom_recommendation_engine.py` (`CustomAssociationRules`), `association_views.py`, `ProductAssociation`.
- Sentyment: `CustomSentimentAnalysis`, `sentiment_views.py`, `Opinion`.

---

*Plik: szczegóły pod rozdział metodyki i eksperyment — dopasuj liczbę runów do czasu na magisterce; minimum to jeden spójny split i jedno K z uzasadnieniem.*
