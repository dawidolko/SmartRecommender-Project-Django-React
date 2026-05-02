# Magisterka na SmartRecommender — poprawki w projekcie + tematy

Założenie: nie budujecie sklepu od zera. Zostaje Django + React + PostgreSQL i to, co już jest; dokładacie **warstwę badawczą** (dane, eksperymenty, ewentualnie jeden-dwa endpointy). Poniżej: **co trzeba poprawić na starcie**, potem **lista tematów** — dla Ciebie i osobno dla kolegi (po kilka opcji do wyboru, nie jedna).

---

## 1. Co jest nie tak teraz i co gdzie sensownie poprawić

| Problem | Gdzie to widać | Co zrobić |
|--------|----------------|-----------|
| Mało użytkowników, zamówienia i opinie w dużej mierze losowe | `backend/home/management/commands/seed.py` | Osobna komenda albo rozszerzenie: **więcej klientów** (parametr z CLI), **persony** (np. ktoś kupuje głównie gaming, ktoś office), **sensowne koszyki** z kilku spójnych kategorii, **oś czasu** zamówień (żeby dało się robić split czasowy). Stały `seed` liczbowy → powtarzalność wyników w pracy. |
| Słabo pod porównanie „jawne vs ukryte” | `UserInteraction` często słaby lub losowy bez związku z zakupem | W seedzie generować **view/click przed zakupem** skorelowane z personą. Jeśli badacie czas na karcie: migracja + pole (np. `duration_ms`) + frontend `ProductPage.jsx` wysyłający czas przy wyjściu ze strony + rozszerzenie `log-interaction` w backendzie. |
| Po zwykłym seedzie często brak sensownego CF w bazie | `generate_product_similarities()` na końcu seeda robi głównie CBF; CF jest z `recommendation_views` / panelu | Jedna komenda typu `prepare_research_db`: po seedzie **zawsze** to samo przeliczenie (CF, CBF, reguły asocjacyjne), żeby każdy eksperyment zaczynał od **identycznego** stanu tabel. |
| Brak jednego miejsca na wyniki eksperymentów | — | Migracja: np. `ExperimentRun` + wiersze wyników albo zapis CSV z `manage.py` — żeby nie szukać metryk po logach konsoli. |
| Promotor chce metryki rekomendacji | — | Wspólny moduł (np. `home/experiments/metrics.py`): **ten sam** split (np. ostatnie X% czasu = test), **Precision@K / nDCG@K** (ustalacie K raz na zawsze). |

Nie trzeba przerabiać całego frontu — tylko to, co faktycznie wchodzi w badanie (log czasu, ewentualnie prosty panel „uruchom eksperyment” albo i bez tego, same komendy z terminala).

---

## 2. Lista od promotora — jak to się łączy z powyższym

- **Kombinacja vs pojedyncze metody** — potrzebujecie rankingów z każdej metody z inżynierki + wspólnej ewaluacji; fuzja (np. RRF albo uśrednienie po rankingu) vs każda metoda osobno.
- **Hyperparameter tuning** — fragment większej pracy: te same metryki, różne parametry (próg podobieństwa, min_support Apriori, ustawienia TF-IDF, fuzzy…); tabela jakość vs czas.
- **LLM vs metody z inżynierki** — ten sam protokół oceny; LLM dostaje historię + opisy/krótki kontekst opinii + często **listę kandydatów** (żeby nie szukał po całym katalogu); porównanie liczb z tym samym ground truth.
- **Sieć łącząca 9 metod + kontekst + dominacja** — wejście: wektor score’ów z 9 źródeł + cechy użytkownika; trening; **SHAP / podobne** — która metoda „waży” w jakiej sytuacji.
- **Segmentacja (K-Means / DBSCAN) + optymalna kombinacja per segment** — cechy użytkownika z bazy → klastry → osobno tuning wag / strategii na segmencie vs globalnie.
- **Jawne vs ukryte** — dwa sposoby budowy profilu (same opinie/oceny vs interakcje + ewentualnie dwell); ta sama metoda rankingu na wierzchu albo ta sama ewaluacja.
- **Skalowalność** — powiększanie syntetycznie |U| / |I| / transakcji, pomiar czasu i ewentualnie `EXPLAIN` na PostgreSQL; wskazanie wąskich gardeł.
- **Wnioskowanie przedziałowe (IT2)** — np. **pyIT2FLS** jako osobna ścieżka vs obecna logika rozmyta z inżynierki; dane z niepewnością (np. mało opinii → szerszy przedział).

---

## 3. Tematy magisterskie — **Ty** (ok. 5–10 propozycji)

Założenie z pracy inż.: CF, sentyment, reguły asocjacyjne — naturalnie trzymasz się **tej** części systemu jako „swoich” metod + **wspólnej** ewaluacji/danych.

1. **Łączenie metod rekomendacji a metody pojedyncze** — zaimplementować 2–3 proste fuzje (np. RRF, Borda, ważona średnia rankingu) nad rankingami z CF, asocjacyjnych i kanału opartego o opinie/sentyment; porównanie z każdą metodą osobno i z popularnością; protokół + metryki + test na seedzie badawczym.

2. **Wpływ hiperparametrów na jakość i czas — CF, Apriori, sentyment** — siatka lub Optuna na wybranych „pokrętłach” (próg podobieństwa CF, min_support/min_confidence, sposób agregacji sentymentu do score); te same dane, wykresy Pareto.

3. **LLM a pipeline z inżynierki (Twoja strona treści)** — przygotowanie promptu: historia zakupów + skrót opinii / agregaty sentymentu + lista kandydatów (np. z CBF); hipoteza: czy pre-trenowany LLM podbija metryki vs najlepszy singleton z inżynierki; kolega może trzymać integrację API — u Was w pracy jasny podział kto co kodzi.

4. **Jakość rekomendacji z danych jawnych (opinie, oceny)** — modele / rankery oparte tylko na `Opinion`, sentymencie i ewentualnie ratingu; porównanie z **drugą gałęzią** (u kolegi: implicit) na **tym samym** zbiorze i **tym samym** ground truth (np. przewidywanie następnego zakupu w części testowej).

5. **Skalowalność CF i reguł asocjacyjnych** — przy rosnącym N (generator): czas przeliczenia macierzy / reguł, liczba wierszy w `ProductSimilarity` / `ProductAssociation`, najcięższe zapytania; propozycje optymalizacji (cache, indeksy, batch).

6. **Reguły asocjacyjne + CF w jednym ensemble vs osobno** — wąski temat: czy celowane łączenie **tylko** tych dwóch rodzajów sygnałów (bez pełnej dziewiątki) daje stabilny zysk; dobra praca jeśli promotor chce węższy zakres.

7. **Sentyment i jakość rankingu tekstowego wyszukiwania vs czysty sygnał transakcyjny** — porównanie ścieżki „rekomendacja z opinii/sentymentu” z CF na jednym protokole ewaluacji (wymaga domknięcia: jak z sentymentu zrobić ranking produktów dla użytkownika — jedna ustalona reguła w całej pracy).

8. **Kontrolowany zbiór danych pod rekomendacje** — mocny **rozdział metodyczny**: projekt person, manifest, powtarzalność; implementacja `seed_research` + dokumentacja; łączy się z dowolnym z powyższych punktów jako „baza pod eksperyment”.

9. **„Cold start” produktów lub użytkowników** — eksperymentalnie: obcinanie historii w seedzie / symulacja nowych kont; kiedy CF się wywraca, a kiedy sentyment lub reguły trzymają jakość.

10. **Ewaluacja offline jako narzędzie** — jeden spójny pipeline (split, metryki, raport CSV) opisany metodycznie i zintegrowany z repozytorium; reszta pracy to 2–3 porównania hipotez na tym pipeline (jeśli promotor woli pracę bardziej „inżyniersko-metodyczną”).

---

## 4. Tematy magisterskie — **kolega (Piotr)** (ok. 5–10 propozycji)

Założenie z inżynierki: CBF, logika rozmyta, część probabilistyczna — analogicznie „jego” silnik + wspólna baza i metryki.

1. **Sieć neuronowa łącząca wszystkie 9 metod z kontekstem użytkownika** — wejście: znormalizowane score z każdej dostępnej metody + wektor cech (liczba interakcji, entropia kategorii, itd.); porównanie z fuzją bez uczenia (u Ciebie) i z najlepszym singletonem; **analiza dominacji** (SHAP lub inna metoda) — kiedy która metoda ma wpływ.

2. **Segmentacja użytkowników (K-Means i DBSCAN) i strategia rekomendacji per segment** — cechy z zamówień i interakcji; dla każdego klastra osobno np. wagi w ensemble lub wybór „dominującej” metody; porównanie z jednym globalnym ustawieniem.

3. **Hyperparameter tuning — CBF, fuzzy (`fuzzy_logic_engine`), parametry probabilistyczne** — ten sam styl co u Ciebie, ale na „jego” module; wspólna tabela porównawcza z pracy zespołowej może trafić do obu prac jako załącznik.

4. **LLM vs metody z inżynierki (strona integracji)** — serwis wywołań, limity tokenów, walidacja `product_id`, pomiar czasu i żądań; porównanie metryk z tym samym `evaluate` co reszta.

5. **Jakość przy danych ukrytych** — profil tylko z `UserInteraction` (z opcjonalnym decay czasu i dwell); to samo ground truth co u Ciebie przy „jawnym” — kto wygrywa na Waszym seedzie.

6. **Skalowalność CBF, fuzzy, zapytań probabilistycznych** — analogicznie jak u Ciebie, inne wąskie gardła (TF-IDF po wszystkich produktach, wiele reguł fuzzy).

7. **Wnioskowanie przedziałowe i niepewność (pyIT2FLS)** — wejścia jako przedziały np. z liczby opinii / rozrzutu ocen; porównanie z obecnym rozwiązaniem rozmytym z inżynierki przy tym samym protokole ewaluacji (albo osobna metryka typu coverage vs accuracy).

8. **Meta-learner prostszy od pełnej sieci** — np. **gradient boosting** na wektorze 9 score + kontekst; pytanie czy wystarcza zamiast MLP; nadal miejsce na „która metoda dominuje”.

9. **Stabilność klastrów i liczba segmentów** — sensownie przy większym N z seeda: silhouette, różne K, wrażliwość wyniku rekomendacji na dobór K.

10. **Kalibracja probabilistyczna** — jeśli w `analytics` / `PurchaseProbability` jest losowość, praca może być o **zastąpieniu** jej modelem uczonym z danych + porównanie jakości rankingu (to już łączy „probabilistykę” z inżynierki z realnym badaniem).

---

## 5. Krótko: podział obowiązków bez filozofii

| Razem | Ty przeważnie | Kolega przeważnie |
|-------|----------------|-------------------|
| Seed badawczy, manifest, `prepare_research_db`, wspólne metryki, ewentualnie migracja eksperymentów i log dwell | Fuzje klasyczne, CF/Apriori/sentyment, jawny kanał danych, opis danych/prompt pod LLM | Meta-model / segmentacja / IT2, implicit + frontend czasu, integracja LLM, tuning CBF/fuzzy/prob, skala „jego” części |

W pracy każdy ma **własny tytuł i własne rozdziały**; wstęp możecie uzgodnić jednym wspólnym akapitem o tym samym repozytorium i tym samym `seed_research`.

---

*Lista tematów ma być pulą do wyboru z promotorem — nie trzeba realizować wszystkich punktów z listy 10; zwykle 1–2 główne hipotezy + tuning albo skalowalność jako podrozdział wystarczą do obrony.*
