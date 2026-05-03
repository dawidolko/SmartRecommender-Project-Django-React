# Lista tematów do wyboru — Dawid Olko (praca magisterska, rozszerzenie SmartRecommender)

---

## Punkt wyjścia: drugi seeder badawczy `seed_research`

Aplikacja zostaje bez zmian. Schemat bazy zostaje. Obecny `seed.py` (sklep komputerowy demo) zostaje. **Dodajemy** drugą komendę `python manage.py seed_research`, która zapełnia te same tabele (`Product`, `Order`, `OrderProduct`, `Opinion`, `UserInteraction`, `Complaint`), ale z parametryzowaną logiką pod każdy temat — żeby dane miały **strukturę**, którą metoda może wykryć i którą można obronić jako hipotezę.

Praktyczne reguły dla każdego tematu:

- nie kasujemy obecnego seedera ani migracji
- każdy temat dorzuca **swój** podrozdział do `seed_research` (jeden plik, kilka funkcji `_seed_for_topic_X()`)
- parametry seedera (siła sygnału, odsetek szumu, rozkłady) są **jawne i kontrolowane**, czyli mogę robić **eksperymenty na samych parametrach** ("co się dzieje z metodą gdy szum rośnie z 10% do 50%")
- na obronie odpowiedź na pytanie _"czy nie testujesz swojego seedera"_ brzmi: **świadomie kontroluję sygnał i szum, mierzę degradację metody w funkcji szumu, dodatkowo walidacja krzyżowa na publicznym datasecie z analogicznej domeny** — i to robię tylko tam, gdzie ma to sens.

---

## Temat D1 — Hybrydowe łączenie metod rekomendacji (CF + Apriori + sentyment) vs metody pojedyncze

**Krótki opis**
8 systemów: B0 popularność, S1 CF, S2 Apriori, S3 sentyment, F12, F13, F23, F123 (fuzje RRF). Pomiar NDCG@10, Precision@10, Recall@10. Test Friedmana po userach.

**Realizacja**

- `seed_research` generuje 200 userów z 5 personami (gamer, biuro, twórca, prezent, entuzjasta). Każda persona ma listę kategorii preferowanych. Reguła: 80% zakupów z preferowanych kategorii, 20% szumu (eksploracja).
- Cutoff temporal split: ostatnie 20% osi czasu = test.
- Implementacja w `home/experiments/fusion.py` (RRF, Borda, Weighted) + `runner.py` (uruchamia 8 systemów, zapisuje do tabeli `ExperimentRun`).
- Powtarzam eksperyment dla 3 poziomów szumu seedera (10% / 30% / 50% zakupów spoza persony) — pokazuje czy fuzja jest **odporna** na szum (a nie tylko że "działa, gdy dane są idealne").

**Cel badawczy**
Sprawdzić, czy fuzja CF+Apriori+sentyment poprawia ranking względem pojedynczych metod **i jak ta przewaga maleje wraz z szumem w danych** — bo realny sklep ma noise.

**Sens i wartość praktyczna**
Sklep dostaje konkretną odpowiedź: "wdrożyć F123" albo "F12 wystarcza, sentyment nie dokłada". Plus krzywa "ile %% szumu jeszcze toleruje fuzja" → użyteczne przy decyzji "czy potrzebujemy lepszego trackingu danych".

---

## Temat D2 — Wpływ hiperparametrów CF, Apriori, sentymentu na jakość i koszt

**Krótki opis**
Siatka parametrów: CF (próg podobieństwa), Apriori (`min_support`, `min_confidence`), sentyment (waga recency, próg neutralności). ~42 konfiguracje × 3 kanały. Front Pareto NDCG vs czas vs rozmiar tabeli.

**Realizacja**

- Używam tego samego `seed_research` co D1 (5 person, 200 userów).
- Dodatkowo seeder skaluje się parametrem (`--clients 50/100/200/400`) — żeby pokazać, że sweet spot zależy od rozmiaru bazy.
- Każdy run zapisuje do `ExperimentRun`: parametry + NDCG + czas regeneracji + liczba wierszy w `ProductSimilarity` / `ProductAssociation`.
- Optuna do strojenia + ręczna siatka dla wykresów Pareto.

**Cel badawczy**
Wyznaczyć **rekomendowane** wartości hiperparametrów dla sklepu naszej skali oraz pokazać, jak sweet spot przesuwa się gdy baza rośnie.

**Sens i wartość praktyczna**
Konkretna instrukcja eksploatacyjna ("dla 200 userów ustaw `min_support=0.02`, dla 1000+ ustaw `0.005`"). Reguła do `RecommendationSettings` w panelu admina — admin nie musi zgadywać.

---

## Temat D3 — Bielik 11B (lokalny LLM) jako re-ranker listy kandydatów

**Krótki opis**
Bielik dostaje 40 kandydatów z fuzji CF+Apriori i ma ich uporządkować. Pomiar NDCG@10 (G0 bez LLM vs G1 z LLM), conformance rate, hallucination rate, latency p95. Modele: Bielik 7B vs 11B vs Mistral Small.

**Realizacja**

- `seed_research` daje historie zakupów dla 200 userów (jak w D1) + opisy produktów z istniejącej bazy (sklep komputerowy ma już opisane produkty: "Mysz Razer Basilisk V3", "Karta GeForce RTX 4070 12GB").
- LLM dostaje historię zakupów + listę 40 kandydatów (id, nazwa, cena, kategoria) → zwraca JSON z permutacją.
- Pydantic v2 waliduje, fallback do G0 przy błędzie.
- Powtarzam dla 3 wielkości listy (20/40/80 kandydatów) — żeby pokazać, jak długość kontekstu wpływa na halucynacje.

**Cel badawczy**
Sprawdzić, czy Bielik 11B (polski LLM) realnie poprawia ranking nad samym sortowaniem po score — i ile to kosztuje (latency, hallucinations, GPU vs CPU).

**Sens i wartość praktyczna**

- Decyzja "czy wdrożyć GPU dla LLM rerankera" z liczbami w ręku (jeśli zysk NDCG <2 punkty a latency rośnie 50× to nie wdrażam)
- Pierwsza ewaluacja Bielika v3 w rec-sys (model wydany 2025) — wkład do polskiej społeczności NLP
- Szablon "jak wdrożyć LLM jako re-rank w sklepie Django+DRF" przenośny do innych projektów

---

## Temat D4 — Profile rekomendacyjne z danych jawnych (opinie) vs ukrytych (interakcje + dwell time)

**Krótki opis**
System J (ranking z `Opinion` + sentyment + ratingi) vs system U (ranking z `UserInteraction` + dwell time) na tym samym ground truth. Stratyfikacja po liczbie opinii / interakcji / personie.

**Realizacja**

- `seed_research` generuje **dwa równoległe strumienie**: dla każdego usera tworzy `Opinion` (jawne) **i** `UserInteraction` (ukryte) skorelowane z personą.
- Dodaję migrację `UserInteraction.duration_ms` (dwell time) + frontend `ProductPage.jsx` loguje czas spędzony na karcie.
- Seeder ma parametr `--review_propensity_per_persona` (gamer 0.6, biuro 0.2, twórca 0.8) → różne userów ma różną liczbę opinii → naturalna stratyfikacja.
- Trzy wariańcie szumu: `noise_implicit` (20% przypadkowych kliknięć), `noise_explicit` (15% trolli piszących nieadekwatne opinie). Pokazuje który strumień jest bardziej odporny.

**Cel badawczy**
Czy jawne opinie wystarczają, czy implicit (interakcje + dwell) jest lepszy — i kiedy?

**Sens i wartość praktyczna**

- Sklep dowiaduje się "czy warto inwestować w zachęcanie do opinii (rabaty za review) czy w tracking dwell time"
- Praca **wspólna z Piotrem** (on robi część implicit) → wspólny seed, wspólny test, dwa rozdziały eksperymentalne z identyczną metodyką

---

## Temat D5 — Skalowalność CF i Apriori w Django + PostgreSQL

**Krótki opis**
Pomiar czasu regeneracji CF i Apriori, rozmiaru tabel, czasu pojedynczego zapytania w funkcji rozmiaru bazy. EXPLAIN ANALYZE. Optymalizacje (indeksy, cache).

**Realizacja**

- `seed_research --clients N` dla N ∈ {50, 100, 200, 400, 800, 1600}.
- Każdy rozmiar: pełna regeneracja CF, pełna regeneracja Apriori → pomiar czasu i rozmiaru.
- Stały zbiór testowy referencyjny (50 userów wybranych raz na zawsze) → NDCG@10 mierzony na każdym rozmiarze, pokazuje że **jakość jest stała** a tylko koszt rośnie.
- 3 optymalizacje: (1) indeks złożony na `Order(user_id, date_order)`, (2) cache rankingów w Redis, (3) batch update zamiast pojedynczych INSERT-ów. Pomiar przed/po.

**Cel badawczy**
Wyznaczyć empirycznie złożoność czasową CF i Apriori w mojej implementacji + zwalidować 3 optymalizacje.

**Sens i wartość praktyczna**

- Konkretna odpowiedź "do ilu userów wystarcza obecna architektura" — istotne dla każdego sklepu Django
- Wnioski przenoszą się 1:1 na inne projekty Django + PostgreSQL z item-based CF i Apriori (dziesiątki podobnych projektów na GitHubie)
- Bezpieczny temat: zawsze coś wyjdzie (jakaś krzywa, jakaś poprawa)

---

## Temat D9 — Rekomendacja na podstawie opisów produktów (wektoryzacja + szukanie podobnych)

**Krótki opis**
Trzy systemy: R0 popularność, R1 wyszukiwanie po wektorach opisów (bez LLM), R2 to samo + LLM przestawia kolejność. Porównanie modelu wielojęzycznego vs angielskiego do wektoryzacji. Pgvector w PostgreSQL.

**Realizacja**

- Sklep komputerowy ma już **realne opisy produktów** w `Product.description` (z seedera podstawowego — laptop "Lenovo ThinkPad X1 Carbon, 14 cali, i7, 16GB RAM, lekki do biura"). To jest realna treść, nie wymaga zmian.
- `seed_research` dorzuca tylko historie zakupów per persona (jak w D1) — żeby był ground truth do ewaluacji.
- Tekst zapytania budowany z historii ("Użytkownik kupił: laptop Lenovo, mysz Logitech, klawiatura mechaniczna") → embedding → kNN po pgvector.
- Dwa modele: `paraphrase-multilingual-mpnet-base-v2` (polski) vs `all-MiniLM-L6-v2` (EN) — porównanie czy warto polski.
- Eksperyment cold-start produktu: chowam 20% produktów z historii (udaję że są nowe, bez zakupów) i sprawdzam czy R1 je znajduje (CF nie znajdzie, bo nie ma historii — opisów jeszcze ma).

**Cel badawczy**
Czy rekomendacja "po treści opisu" działa w sklepie komputerowym (dużo wąskich kategorii, podobne nazwy) i czy LLM dokłada coś nad samym wyszukiwaniem wektorowym.

**Sens i wartość praktyczna**

- Nowy produkt w sklepie (CF go nie zna) — R1 **od razu** go rekomenduje na podstawie opisu. Fundamentalny zysk dla sklepu z rotującym asortymentem
- Sklep dowiaduje się "warto inwestować w długie sensowne opisy" (jeśli R1 > R0)
- Argument za pgvector w naszym stacku — bez nowych usług (Qdrant nie potrzebny)

---

## Temat D10 (REKOMENDOWANY) — Połączenie D1 + D3 + D9 w jeden trzyetapowy pipeline

**Krótki opis**
Jeden duży system: 4 źródła kandydatów (CF + Apriori + sentyment + opisy) → fuzja RRF → Bielik LLM przestawia kolejność. 7 wariantów do ablacji (V1 sama klasyka, V2 same opisy, V3 opisy+LLM, V4 klasyka+LLM, V5 wszystko, V6 dwustopniowy: opisy → klasyka → LLM, B0 popularność).

**Realizacja**

- Łączy seedery z D1 (persony, zakupy), D9 (opisy z bazy + cold-start) — jedno wywołanie `seed_research --topic d10`.
- Ablacja: każdy z 7 wariantów to ten sam kod ze zmienioną maską aktywnych komponentów (`{cf, apriori, sent, rag, llm}`).
- 5 powtórzeń × 7 wariantów × 2 testy (wszyscy userzy + cold-start) = 70 runów do `ExperimentRun`.
- Front Pareto: jakość NDCG@10 na osi Y, czas pojedynczego zapytania na osi X — szukam wariantu nie zdominowanego (V6 oczekiwany).

**Cel badawczy**
Zaprojektować i wskazać **architekturę produkcyjną** rec-sys hybrydowego: który komponent ile dokłada do jakości, który podzbiór wystarcza, który ma najlepszy stosunek jakości do kosztu.

**Sens i wartość praktyczna**

- Gotowy szablon architektury dla polskiego sklepu e-commerce (Django + PostgreSQL + pgvector + Ollama + Bielik)
- Liczby pod każdą decyzję: "klasyka sama → 0.62 NDCG, koszt 50ms; klasyka+LLM → 0.71 NDCG, koszt 4s; wszystko → 0.74 NDCG, koszt 5s — wybierz V4"
- Łączy trzy gorące tematy 2024–2026 (klasyczne hybrydy, LLM4Rec, RAG) w jednym spójnym deployu — argument za publikacją (PP-RAI, FedCSIS)
- Plan B: jeśli LLM nie zadziała → V1+V2 wciąż dają pełną pracę (D1+D9 jako fallback)

---

# Tematy nie-rekomendacyjne (korzystające z aplikacji, ale nie z metod CF/Apriori/sentymentu)

---

## Temat N1 — Automatyczna kategoryzacja i routing reklamacji klientów

**Krótki opis**
W bazie jest `Complaint` z polem tekstowym `description`. Klient pisze co go boli ("paczka uszkodzona", "płatność nie przeszła", "nie działa po tygodniu"). Klasyfikator przypisuje: kategorię problemu, priorytet, sugerowane rozwiązanie. Trzy podejścia: TF-IDF+SVM vs HerBERT (polski transformer) vs Bielik zero-shot.

**Realizacja**

- `seed_research` generuje 2000 syntetycznych reklamacji z **kontrolowaną** strukturą: 6 kategorii (logistyka / jakość / opis / płatność / brak elementu / zmiana zdania) × 3 poziomy priorytetu × 4 sugerowane rozwiązania. Każda reklamacja ma **prawdziwą etykietę** (ground truth).
- Treść generowana z szablonów + parafrazy z Bielika (żeby nie były 1:1 te same zdania) + 15% szumu (literówki, nietypowe sformułowania).
- Walidacja krzyżowa: dodatkowo biorę 200 prawdziwych reklamacji z **publicznego US Consumer Complaint Database** (przetłumaczone DeepL na polski) → sprawdzam czy klasyfikator trenowany na seederze działa też na realnym tekście. Jeśli tak → seeder oddaje wystarczającą strukturę.
- Endpoint `POST /api/complaint/{id}/classify/` zwraca 3 predykcje + confidence.

**Cel badawczy**
Czy mały model specjalistyczny (HerBERT) + trochę danych bije zero-shot LLM (Bielik) bez treningu — i jaki jest break-even point liczby oznaczonych reklamacji.

**Sens i wartość praktyczna**

- Realne narzędzie dla sklepu: panel admina pokazuje pre-wypełnione kategorie reklamacji → admin szybciej obsługuje zgłoszenia
- Decyzja biznesowa: "od ilu reklamacji warto trenować własny model" (jeśli mam <500 oznaczonych → LLM, jeśli >500 → trening)
- Wynik przenosi się na inne polskie e-commerce (Allegro, OLX) — wszyscy mają reklamacje w polskim, mało prac NLP na tym

---

## Temat N2 — Wykrywanie podejrzanych zachowań i nietypowych zamówień

**Krótki opis**
System scoruje każde zamówienie pod kątem ryzyka (bot / fraud / nadużycie zwrotów). Trzy podejścia: reguły ręczne (baseline) vs Isolation Forest vs Autoencoder na sekwencjach `UserInteraction`.

**Realizacja**

- `seed_research` generuje 95% normalnych userów (jak w D1: persony, naturalne ścieżki) + **wstrzykuje 5% anomalii** z trzema profilami:
  - **bot**: konto < 1h, sesja < 30s, 1 view → kup → wyloguj
  - **fraud**: drogie zamówienie >5× średniej tego usera, świeże konto, nietypowa godzina
  - **abuse**: 10+ zwrotów w miesiącu na koncie założonym 6mc temu
- **Wszystkie 5% jest oznaczone** (`is_anomaly_ground_truth=True`) → pełen ground truth do ewaluacji recall/precision/F1.
- Walidacja krzyżowa: trenuję na anomaliach z seedera, testuję na **publicznym IEEE-CIS Fraud Detection** (Kaggle) — jeśli model trenowany na moich syntetycznych anomaliach łapie też realne fraudy → znaczy że profile anomalii w seederze są realistyczne (a nie "moje wymysły").
- Nowy model `OrderRiskScore` + endpoint `GET /api/admin/risk-alerts/` + zakładka w panelu admina.

**Cel badawczy**
Który z trzech detektorów ma najlepszy stosunek wykrywalności (recall) do liczby fałszywych alarmów (FPR) — przy ograniczeniu, że admin akceptuje max 5 alertów dziennie.

**Sens i wartość praktyczna**

- Realna oszczędność dla sklepu: każdy wyłapany fraud = 200-2000 zł oszczędności. 5% anomalii × 1000 zamówień miesięcznie = 50 prób → kilka tysięcy zł rocznie
- Decyzja biznesowa: "wystarczają reguły, czy warto inwestować w ML"
- Walidacja na IEEE-CIS daje wartość naukową — replikowalne na innych e-commerce

---

## Temat N3 — Inteligentne wyszukiwanie produktów odporne na literówki, synonimy i intencje

**Krótki opis**
Trzy silniki wyszukiwania: klasyczny (TF-IDF + obecna `FuzzySearchAPIView`) vs wektorowy (embedding zapytania + pgvector) vs LLM-asysta (Bielik filtruje 50 wyników wektorowych). Plus autocomplete.

**Realizacja**

- Sklep komputerowy ma już **prawdziwe nazwy produktów** w `Product.name` ("Mysz Razer Basilisk V3", "Karta GeForce RTX 4070 12GB"). Bazujemy na tym.
- `seed_research` dorzuca **dataset zapytań testowych** (200 zapytań × 3 typy):
  - **literówki**: "razr basilsk", "rtx 4070" → cel: znaleźć Razer Basilisk, GeForce RTX 4070
  - **synonimy**: "słuchawki" vs "headset" vs "nauszniki" → cel: ten sam produkt
  - **intencje**: "monitor do gier", "laptop do biura", "mysz dla lewaka" → cel: przefiltrować po atrybutach
- Każde zapytanie ma **ręcznie oznaczony** "idealny wynik" (top-3 produkty) → ground truth do mierzenia trafności (Precision@1, Precision@3, MRR).
- Walidacja krzyżowa: dodatkowo testuję na **MS MARCO** (publiczny zbiór zapytań wyszukiwania) — jeśli ranking moich silników jest spójny na zapytaniach komputerowych i na MS MARCO, to wnioski są ogólne.
- Frontend: nowy komponent `SmartSearchBar` z autocomplete + przełącznikiem silnika.

**Cel badawczy**
Który silnik (lub hybryda) daje najwyższą trafność wyszukiwania — i czy LLM dokłada coś nad samym wektorem przy wąskim katalogu (sklep komputerowy ma 500 produktów, mało).

**Sens i wartość praktyczna**

- **Demo na obronie**: wpisuję "monitor do gier" na żywo, pokazuję trzy silniki obok siebie → wizualny dowód
- Realny zysk dla sklepu: lepsza wyszukiwarka = niższy bounce rate = wyższa konwersja (każdy 1% konwersji = realne pieniądze)
- Decyzja biznesowa: "czy LLM w wyszukiwarce się opłaca przy 500 produktach" (prawdopodobnie nie — wektor wystarcza, LLM rezerwujemy dla katalogów 10k+)

## Wybór tematu — szybka mapa

| Wariant                        | Trzon pracy           | Dodatki                 |
| ------------------------------ | --------------------- | ----------------------- |
| **A (rec-sys, rekomendowany)** | **D10**               | D2, D5                  |
| **B (rec-sys węższy)**         | D1 + D9               | D3 jako rozszerzenie    |
| **C (rec-sys minimalny)**      | D1 + D2               | bez LLM/RAG, bezpieczne |
| **D (LLM-centric)**            | D3 + D9               | D1 jako baseline        |
| **E (NLP/aplikacyjny)**        | **N1** (reklamacje)   | N3 jako uzupełnienie    |
| **F (security)**               | **N2** (anomalie)     | N1 jako uzupełnienie    |
| **G (UX)**                     | **N3** (wyszukiwarka) | D9 jako baza techniczna |
