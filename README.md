# Dragon Village 3 Guide

A searchable, question-led reference site for Dragon Village 3. The site is plain HTML, CSS, and JavaScript and is published with GitHub Pages.

## Run locally

Open `index.html` in a browser. No build step or dependencies are required.

## Add or update guide information

- `guide-data.js` contains Getting Started, Dragon Collection, Growth, and Breeding articles.
- `guide-extra.js` contains battle, activity, Orb, Gem, item, and currency articles.
- `guide-more.js` contains Village, events, guild, and support articles.
- `guide-reference.js` contains summons, competition, and Dragon reference articles.
- `app.js` builds the navigation, search results, and article pages from those entries.

Add a category with `{category: "Category name", items: [...]}`. Each article uses an `id`, `title`, `summary`, searchable `tags`, `updated`, and `sections`. Each section has a `title` and an `html` string. Add a `source` link when a detail depends on a game version, notice, or other reference. Keep all four data files loaded before `app.js` in `index.html`.

For time-sensitive details such as event dates, draw rates, and availability, link to the current official notice and identify its date. Check the in-game screen for account-specific or live values. The site search covers titles, summaries, tags, and article text. Use `/` to focus search.

## Publish

GitHub Actions deploys changes pushed to `main`. GitHub Pages uses the **GitHub Actions** source. The published site is `https://zokkaxdj9.github.io/dv3-game-guide/`.

## Sources

Guide notes use the locally supplied Dragon Village 3 1.0.18 package and DV3 Research Complete corpus for game-system context, plus official community notices for later or rotating systems. Community references are linked in the relevant articles.

This is a fan-made reference and is not affiliated with Highbrow.
