## 1. Remove the custom domain entry in GitHub Pages

1. Go to **Settings** → **Pages** in your repository.

2. In the **Custom domain** section, click **Remove** (if it's still set to "smartrecommender.dawidolko.pl").

3. Save your changes.

4. (Optional) Uncheck / disable **Enforce HTTPS** (if checked).

After this step, GitHub Pages will stop trying to use your domain and go back to the default address.

---

## 2. Delete / change the `CNAME` file in the project

1. Go to the `frontend/public/` folder and **delete** the `CNAME` file (or rename / clear its contents).

- The `CNAME` file is responsible for configuring your custom domain - if you don't delete it, then with each `npm run deploy` GitHub Pages will try to assign this custom domain again. 2. Save and commit changes:

```bash
git add public/CNAME
git commit -m "Remove CNAME for custom domain"
```

_(or delete the file completely and commit it too)._

---

## 3. Change the `homepage` value in `package.json` (or remove it)

In the `frontend/package.json` file you probably have an entry like:

```json
"homepage": "https://project.dawidolko.pl",
```

You can **delete** it or replace it with the default GitHub Pages address, e.g.:

```json
"homepage": "https://dawidolko.github.io/repo-name"
```

(_Use the correct `repo-name`._)

If you prefer not to set anything, you can simply delete this line.

Then save and commit.

---

## 4. Redeploy the project (`npm run deploy`)

1. Go to the `frontend` directory:

```bash
cd frontend
```

2. Run:

```bash
npm run deploy
```

3. Gh-pages will build the project, update the `gh-pages` branch without the `CNAME` file and without the entry about your own domain.
