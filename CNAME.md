## 1. Usuń wpis o własnej domenie w GitHub Pages

1. Przejdź do **Settings** → **Pages** w Twoim repozytorium.
2. W sekcji **Custom domain** kliknij **Remove** (jeśli nadal jest ustawione „smartrecommender.dawidolko.pl”).
3. Zapisz zmiany.
4. (Opcjonalnie) Odznacz / wyłącz **Enforce HTTPS** (jeśli jest zaznaczone).

Po tym kroku GitHub Pages przestanie próbować używać Twojej domeny i wróci do domyślnego adresu.

---

## 2. Usuń/zmień plik `CNAME` w projekcie

1. Wejdź do folderu `frontend/public/` i **usuń** plik `CNAME` (lub zmień jego nazwę / wyczyść zawartość).
   - Plik `CNAME` odpowiada za konfigurację własnej domeny — jeśli go nie usuniesz, to przy każdym `npm run deploy` GitHub Pages będzie ponownie próbował przypisać tę customową domenę.
2. Zapisz i skomituj zmiany:
   ```bash
   git add public/CNAME
   git commit -m "Remove CNAME for custom domain"
   ```
   _(lub usuń plik zupełnie i też zacommituj)._

---

## 3. Zmień wartość `homepage` w `package.json` (lub usuń)

W pliku `frontend/package.json` masz prawdopodobnie wpis typu:

```json
"homepage": "https://project.dawidolko.pl",
```

Możesz go **usunąć** lub zastąpić domyślnym adresem GitHub Pages, np.:

```json
"homepage": "https://dawidolko.github.io/repo-name"
```

(_Użyj właściwego `repo-name`._)

Jeśli wolisz nie ustawiać niczego, możesz po prostu skasować tę linię.

Następnie zapisz i zrób commit.

---

## 4. Ponownie wdroż projekt (`npm run deploy`)

1. Wejdź w katalog `frontend`:
   ```bash
   cd frontend
   ```
2. Uruchom:
   ```bash
   npm run deploy
   ```
3. Gh-pages zbuduje projekt, zaktualizuje branch `gh-pages` bez pliku `CNAME` i bez wpisu o własnej domenie.

---
