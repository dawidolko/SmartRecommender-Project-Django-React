Opis metod stosowanych w projekcie:

1. Collaborative Filtering (CF)

   - Analizuje podobieństwa między użytkownikami (lub między produktami) na podstawie historii zakupów i ocen.
   - W projekcie posłuży do sugerowania produktów, które kupili inni, podobni klienci (User-Based CF) lub produktów powiązanych ze sobą w historii zakupów (Item-Based CF).

2. Content-Based Filtering (CBF)

   - Skupia się na cechach produktu (np. kategoria, słowa kluczowe, opis).
   - W projekcie będzie proponować produkty podobne do tych, które użytkownik już polubił/kupił, bazując na analizie ich atrybutów (np. TF-IDF w opisach).

3. Modele Probabilistyczne (Naive Bayes)

   - Wykorzystują dane o użytkownikach i produktach do szacowania prawdopodobieństwa zainteresowania konkretną ofertą.
   - W projekcie pomogą określać, z jakim prawdopodobieństwem użytkownik kupi dany produkt, co pozwoli lepiej priorytetyzować rekomendacje.

4. Fuzzy Decision Systems (Logika Rozmyta)

   - Wprowadza pojęcia „stopnia przynależności” (np. produkt może być „trochę drogi” albo „umiarkowanie tani”), co pozwala lepiej oddać subiektywne cechy.
   - W projekcie umożliwi bardziej elastyczne reguły rekomendacyjne, np. łączenie atrybutów takich jak „niska cena” i „wysoka jakość” w celu wybrania najlepszych ofert.

5. Sentiment-Based Recommendations

   - Analizuje opinie i recenzje użytkowników, aby określić ich wydźwięk (pozytywny/negatywny).
   - W projekcie pozwoli proponować produkty, które zbierają głównie pozytywne komentarze, jednocześnie filtrując te z negatywnymi opiniami.

6. Reguły Asocjacyjne
   - Wykrywają zależności między produktami na podstawie analizy transakcji, co umożliwia identyfikację produktów często kupowanych razem.
   - W projekcie pozwalają na identyfikację powiązanych produktów, które mogą być rekomendowane klientom.
