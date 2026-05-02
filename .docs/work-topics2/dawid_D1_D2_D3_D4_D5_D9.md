# Dawid Olko — szczegółowy opis wybranych tematów magisterskich (D1, D2, D3, D4, D5, D9)

Dokument uzupełnia `final_proposals.tex`: **jak by to działało**, **czego by używało (biblioteki)**, **czy wchodzi kNN / k-means**, **co mierzysz**, **jaki jest sens badawczy**. Spójny z istniejącym repozytorium *SmartRecommender* (Django, Twoje metody: CF, Apriori, sentyment).

---

## Wspólne elementy dla wszystkich tych tematów

| Element | Opis |
|--------|------|
| **Dane** | Zalecany `seed_research` (persony, spójne zamówienia, opinie po zakupie) zamiast samego `seed.py` demo. |
| **Ewaluacja offline** | Jeden ustalony **podział czasowy** (np. ostatnie 20% czasu = zbiór testowy): dla każdego użytkownika z testu budujesz rekomendację **tylko z przeszłości** (train) i sprawdzasz, czy produkty z **przyszłych** zakupów w bazie trafiają do top-K. |
| **Metryki rankingowe** | Precision@K, Recall@K, NDCG@K (K np. 5 lub 10), MAP, często też *coverage* (jaki % katalogu kiedykolwiek pojawia się w rekomendacjach) i opcjonalnie *diversity*. |
| **Kod w projekcie** | Nowy pakiet np. `backend/home/experiments/` (`metrics.py`, `runner.py`, ewentualnie `fusion.py`, `llm_recommender.py`) + rejestracja `ExperimentRun` w adminie — **bez** kasowania istniejących widoków sklepu. |
| **k-means / K-means** | W **Twoich** tematach D1–D5, D3 **nie musi** wystąpić. **k-means** jest typowy u **Piotra** (segmentacja — P2). U Ciebie może pojawić się **tylko jako opcjonalny** dodatek (np. grupowanie użytkowników po cechach jawnych w D4) — patrz przy D4. |
| **kNN** | W **D9 (RAG)** najczęściej używasz **kNN w przestrzeni embeddingów** (sąsiedzi po cosinusie) do pobrania kandydatów tekstowych. W D1/D3 **możesz** (nie musisz) użyć kNN na wektorach jako **generatora kandydatów** przed LLM — to osobna decyzja projektowa. |

---

## D1 — Łączenie metod rekomendacji versus metody pojedyncze

### Aspekt badawczy
- Pytanie praktyczno-naukowe: **czy ensemble (łączenie rankingów) poprawia jakość** względem najlepszej pojedynczej metody i względem naiwnego baseline (popularność)?
- W literaturze hybrydy są klasą samą w sobie; Ty masz **konkretny zestaw trzech kanałów** już zaimplementowanych w inżynierce — więc praca jest **empiryczna i odtwarzalna**, nie „abstrakcyjna”.

### Na czym polega technicznie
1. Dla użytkownika `u` i ustalonego K każdy kanał zwraca listę `(product_id, score_lub_ranga)`:
   - **CF** — z `ProductSimilarity` (collaborative) i historii zakupów z `Order` / `OrderProduct`.
   - **Apriori** — z `ProductAssociation` (np. reguły koszykowe; scoring z confidence/lift).
   - **Sentyment** — ranking produktów z Twojej logiki `CustomSentimentAnalysis` + opinie (`Opinion`), ustal **jedną** sztywną regułę agregacji (żeby było do obrony).
2. **Fuzja** — osobny moduł, np.:
   - **RRF (Reciprocal Rank Fusion)** — bez kalibracji score; łatwe do obrony.
   - **Borda** — suma miejsc na listach.
   - **Ważona średnia** — po znormalizowaniu score do [0,1] per metoda.
   - Opcjonalnie **switching**: np. jeśli użytkownik ma <3 zamówienia, wyłącz CF z fuzji (to już rozszerzenie — można jako podrozdział).

### k-means / kNN
- **Rdzeń D1: ani k-means, ani kNN nie są wymagane.** To łączenie list z gotowych metod.
- **Opcjonalnie:** generator kandydatów przed fuzją może użyć **kNN** w przestrzeni embeddingów produktów (jak zapowiedź D9) — wtedy fuzja działa na zwężonym zestawie; to **wariant rozszerzony**, nie definicja D1.

### Biblioteki (orientacyjnie)
- **numpy** — wektory score, normalizacja.
- **pandas** — wygodne tabele wyników eksperymentów (opcjonalnie).
- **Django ORM** — dane.
- **scipy.stats** — jeśli robisz testy statystyczne porównań (np. Friedman + post-hoc) — opcjonalnie.
- Sam algorytm RRF/Bordy to kilkanaście–kilkadziesiąt linii Pythona, bez osobnej „ciężkiej” biblioteki.

### Co mierzysz
- NDCG@K, Precision@K, Recall@K, MAP, coverage (i czas jednej rekomendacji / czas batcha).
- Porównujesz: każda metoda osobno vs. każda wersja fuzji vs. popularność.

### Co wnosi praca
- Twarde **porównanie hybryd vs. singleton** na jednym protokole, na Twoim sklepie i Twoich trzech silnikach — gotowy materiał na rozdział „eksperyment”.

### Propozycja rozdziałów
1. Teoria krótko: hybrydy, RRF/Borda.  
2. Implementacja: adaptery na CF / Apriori / sentyment + `fusion.py`.  
3. Protokół i metryki.  
4. Wyniki i wnioski.

---

## D2 — Wpływ hiperparametrów na jakość i czas (CF, Apriori, sentyment)

### Aspekt badawczy
- Nie „nowy algorytm”, tylko **systematyczna analiza czułości**: które pokrętła realnie zmieniają ranking, a które tylko kosztują czas lub puchną baza reguł.
- Naturalny produkt: **krzywe Pareto** (jakość vs. czas vs. rozmiar modelu w DB).

### Na czym polega technicznie
- **Apriori:** parametry już w kodzie — `min_support`, `min_confidence` (`CustomAssociationRules`, endpoint `update-association-rules`). Uruchamiasz pętlę: np. siatka wartości lub **Optuna** szuka sensownych kombinacji przy karnym czasie przeliczenia.
- **CF:** m.in. **próg podobieństwa** przy zapisie par do `ProductSimilarity` (w `recommendation_views` jest logika z progiem) — zmieniasz, regenerujesz podobieństwa, mierzysz jakość i czas.
- **Sentyment:** np. sposób mapowania tekstu opinii na score produktu dla użytkownika (średnia, waga recency, próg neutralny) — **musisz zamrozić jedną rodzinę reguł**, żeby nie rozlać się na 100 wariantów heurystyk naraz.

### k-means / kNN
- **Nie są potrzebne** w rdzeniu D2.

### Biblioteki
- **optuna** lub klasyczna siatka (pętle w `manage.py` / skrypt).
- **time** / **logging** — pomiar czasu regeneracji.
- **Django ORM**, ewentualnie **django-extensions** runscript — organizacja.

### Co mierzysz
- Te same metryki co w D1 + **czas** przeliczenia (Apriori, CF) + **liczba rekordów** w `ProductAssociation` / `ProductSimilarity`.

### Co wnosi praca
- Odpowiedź typu: „w naszym sklepie **min_support=…** to sweet spot; niżej — szum i czas, wyżej — utrata pokrycia”.

### Propozycja rozdziałów
1. Hiperparametry i literatura (krótko).  
2. Metodologia strojenia (siatka vs. bayesowski).  
3. Wyniki: tabele + Pareto.  
4. Wnioski inżynierskie dla utrzymania systemu.

---

## D3 — Duży model językowy jako główny kanał (re-ranking kandydatów)

### Aspekt badawczy
- Jak **LLM jako re-ranker** (na zwężonej liście) radzi sobie na polskim e-commerce z Twoimi danymi; **halucynacje** (ID spoza listy) i **stabilność** formatu vs. jakość rankingowa.
- Porównanie z inżynierką **opcjonalne** — minimum sensowne: ta sama lista kandydatów **bez** LLM (sort po score generatora) vs. **z** LLM.

### Na czym polega technicznie
1. **Generator kandydatów** (tanio): popularność w kategorii użytkownika, top-N z CF, top-N z Apriori, los z ograniczeniem kategorii — **jeden wariant zamrożony** w pracy, żeby nie rozmyć tematu.
2. Z ORM składasz **prompt**: historia zakupów (skrót), lista kandydatów (id, nazwa, krótki opis).
3. **Ollama** + model otwarty (np. Bielik) → odpowiedź w **JSON** (np. lista `{product_id, rank}`).
4. **Pydantic** waliduje ID ∈ kandydaci; retry / skrót kontekstu przy błędzie.
5. Ten sam **runner metryk** co dla pozostałych metod.

### k-means / kNN
- **k-means:** niepotrzebny.  
- **kNN:** nie jest wymagany; **możesz** wygenerować kandydatów przez kNN w embeddingach (jak w D9) — wtedy D3 i D9 się ładnie łączą w jednym kodzie, ale to decyzja zakresu pracy.

### Biblioteki
- **ollama** (klient) lub **httpx** do `localhost:11434`
- **pydantic** v2
- **Django**
- Opcjonalnie **jinja2** / pliki `.txt` na szablony promptów

### Co mierzysz
- NDCG@K, Precision@K; **udział nieważnych ID / błędów JSON**; **latency** na jednego użytkownika; zużycie RAM na M3 Pro.

### Co wnosi praca
- Empiryczny materiał „**LLM4Rec na własnym stacku + polski model**”, z jasnym ograniczeniem (kandydaci z katalogu).

### Propozycja rozdziałów
1. LLM w rekomendacjach (literatura skrót).  
2. Architektura: kandydaci → prompt → walidacja.  
3. Eksperymenty (modele, prompty).  
4. Bezpieczeństwo i błędy (nawiązanie do D11 jeśli robisz).

---

## D4 — Jakość przy profilu z **danych jawnych** (opinie, oceny)

### Aspekt badawczy
- Czy rekomendacja zbudowana **tylko z jawnych sygnałów** (tekst/ocena) jest konkurencyjna względem profilu z **ukrytych interakcji** (część zwykle u Piotra) — **przy tym samym zadaniu predykcji** (np. następny zakup w teście czasowej).
- Wkład: **porównanie strumieni danych**, nie tylko jeden algorytm.

### Na czym polega technicznie
1. **Ty:** z `Opinion` + `CustomSentimentAnalysis` budujesz ranking produktów dla użytkownika (np. produkty „w stylu” pozytywnych opinii użytkownika, lub podobieństwo tekstowe do jego historii — **jedna ustalona formuła**).
2. **Piotr (zespół):** profile z `UserInteraction` (+ ewentualnie dwell).
3. Wspólny **ground truth**: przyszłe `OrderProduct` w teście.
4. Wspólne metryki i ten sam split.

### k-means / kNN
- **k-means (opcjonalnie):** możesz pogrupować użytkowników według **wektora jawnych cech** (np. liczba opinii, średnia gwiazdka, entropia kategorii komentowanych) i raportować metryki **per klaster** — to **nie jest obowiązek**, ale daje ładny podrozdział „analiza podgrup”.
- **kNN:** możesz powiedzieć „użytkownicy podobni pod kątem historii opinii → polecanie produktów, które podobni lubią” — to jest **user-user po stronie jawnej treści**; biblioteka: **numpy** / **scikit-learn** `NearestNeighbors` na rzadkich wektorach (ostrożnie ze skalą). Rdzeń pracy może zostać przy prostszej agregacji bez kNN.

### Biblioteki
- Django ORM, numpy; opcjonalnie **scikit-learn** (`NearestNeighbors`, `KMeans`) jeśli wybierzesz te rozszerzenia.

### Co mierzysz
- Rankingowe: NDCG@K, Precision@K; opcjonalnie błąd predykcji oceny jeśli zdefiniujesz regresję.

### Co wnosi praca
- Odpowiedź „**czy opinie wystarczą**” w waszym sklepie — ważne biznesowo (zbieranie recenzji vs. telemetria).

---

## D5 — Skalowalność collaborative filtering i reguł asocjacyjnych

### Aspekt badawczy
- Gdzie **pęka czas i pamięć** przy rosnącym N użytkowników / produktów / transakcji; jak rośnie rozmiar `ProductSimilarity` i `ProductAssociation`; które zapytania PostgreSQL dominują koszt.

### Na czym polega technicznie
- Seria seedów (lub parametrów `--clients`) 50 → 100 → 200 → … przy **zamrożonym** teście referencyjnym (np. stała proporcja czasu albo stały zbiór userów testowych wyciągnięty wcześniej).
- Pomiar: czas **regeneracji** podobieństw CF, czas **Apriori**, czas pojedynczego zapytania rekomendacji, rozmiar tabel.
- **EXPLAIN ANALYZE** na 2–3 najcięższych zapytaniach.
- Propozycje optymalizacji: indeksy, batch, cache (u Was już jest cache w debug CF), ewentualnie materialized view — **bez** konieczności przepisywania na Sparka.

### k-means / kNN
- **Nie dotyczy** (chyba że robisz przybliżone CF oparte na klastrach użytkowników — to już inny research track, raczej nie D5).

### Biblioteki
- **psycopg** + surowe SQL do EXPLAIN; **time**, **memory_profiler** / **tracemalloc** (opcjonalnie); Django.

### Co mierzysz
- Czas, RAM, liczby wierszy w tabelach, metryki jakości **na jednym** ustalonym teście (żeby skala nie zmieniła definicji jakości między runami bez kontroli).

### Co wnosi praca
- Rozdział typu „**jak daleko zajedzie ten stack**” — przydatny przy obronie i w pracy inżynierskiej.

---

## D9 — LLM i RAG wyłącznie nad **treścią katalogu**

### Aspekt badawczy
- Czy **retrieval + generacja** na opisach produktów (i opcjonalnie fragmentach opinii) daje zysk nad **samym retrieval bez LLM** i nad popularnością — przy kontrolowanym katalogu (Twój sklep).
- To jest najbliższy „klasycznemu” **RAG**: źródło prawdy = Twoja baza produktów.

### Na czym polega technicznie
1. **Indeks:** dla każdego produktu budujesz tekst (nazwa + opis + kategoria + opcjonalnie skrót opinii); liczysz **embedding** (model wielojęzyczny).
2. **Baza wektorowa lub pgvector:** przechowujesz wektory; dla zapytania użytkownika (zbudowanego z historii zakupów jako tekst) liczysz embedding zapytania.
3. **Retrieval:** **k najbliższych sąsiadów** w sensie cosinusa (**to jest kNN w przestrzeni embeddingów** — centralny element D9).
4. **Opcjonalnie MMR** (maksymalna marginalna relewancja) żeby ograniczyć pięć podobnych myszek w jednej liście — implementacja w numpy lub **langchain** CommunityRetriever (opcjonalnie).
5. **LLM:** dostaje tylko **retrieve’owane** opisy i ma zwrócić ranking lub uszeregować listę; walidacja `product_id`.
6. **Baseline porównawcze:** (A) ten sam retrieval + prosty scoring bez LLM (np. średnia ocena wśród retrieved), (B) popularność globalna.

### k-means / kNN
- **kNN:** **tak, w rdzeniu** — wyszukiwanie sąsiadów w przestrzeni embeddingów (implementacja: **FAISS**, **qdrant-client**, **chromadb**, lub **pgvector** z operatorem `<=>`).
- **k-means:** **opcjonalnie** — np. **kwantyzacja** klastrów przy dużym katalogu (IVF w FAISS) lub grupowanie produktów do analizy — **nie jest wymagane** na obronę; możesz wspomnieć jako „przyszła optymalizacja”.

### Biblioteki
- **sentence-transformers** + **torch**
- **qdrant-client** / **chromadb** / **pgvector** (wybór jednej ścieżki)
- **ollama** + **pydantic** (jak D3)
- Opcjonalnie **langchain** / **llama-index** (wygoda, nie obowiązek)

### Co mierzysz
- NDCG@K, Precision@K; czas budowy indeksu i czas zapytania end-to-end; opcjonalnie **Recall@k retrieval** względem „idealnego’’ zbioru produktów z przyszłego koszyka (wymaga precyzyjnej definicji).

### Co wnosi praca
- Jasny eksperyment **RAG vs. retrieval-only** na jednym katalogu — mocna narracja „semantyka treści sklepu”.

### Propozycja rozdziałów
1. RAG — skrót literaturowy.  
2. Embeddingi i indeks (kNN).  
3. Prompt i LLM.  
4. Baseline i wyniki.

---

## Szybkie zestawienie: kNN / k-means w Twoich tematach

| Temat | kNN | k-means |
|-------|-----|--------|
| **D1** Fuzja | Nie w rdzeniu. Opcjonalnie do generowania kandydatów. | Nie |
| **D2** Tuning | Nie | Nie |
| **D3** LLM re-rank | Opcjonalnie (kandydaci z embeddingów) | Nie |
| **D4** Jawne vs ukryte | Opcjonalnie (podobni użytkownicy po profilu opinii) | Opcjonalnie (grupy użytkowników po cechach jawnych) |
| **D5** Skalowalność | Nie | Nie |
| **D9** RAG | **Tak** (sąsiedzi w przestrzeni embeddingów) | Opcjonalnie (optymalizacja / analiza), nie rdzeń |

---

## Gdzie to siada w Twoim repozytorium (przypomnienie)

- **CF:** `backend/home/recommendation_views.py`, `ProductSimilarity` (collaborative).  
- **Apriori:** `backend/home/custom_recommendation_engine.py` (`CustomAssociationRules`), `association_views.py`, `ProductAssociation`.  
- **Sentyment:** `custom_recommendation_engine.py` (`CustomSentimentAnalysis`), `sentiment_views.py`.  
- **Nowe:** `backend/home/experiments/*`, `seed_research`, modele `ExperimentRun` itd. wg `final_proposals.tex`.

---

*Plik pomocniczy do obrony i planowania rozdziałów — możesz wkleić fragmenty do pracy po uzgodnieniu z promotorem.*
