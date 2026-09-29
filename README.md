# Dragon Village 3 Field Guide

A player-focused, searchable reference site for Dragon Village 3. It is plain HTML, CSS, and JavaScript with no build step, so it can be hosted on GitHub Pages.

## Run locally

Open `index.html` in a browser, or serve this folder with any static web server.

## Site contents

- `data/catalog-data.js` contains a static reference catalog of 113 Dragons and 64 Orbs, generated from the supplied 1.0.18 game tables. English names are reconciled with the local English research corpus.
- `data/stage-data.js` contains 96 Expedition stages and 72 grouped Dungeon stages, including enemy references, levels, Fatigue, and recommended power where supplied by the game tables.
- `guide-data.js`, `guide-extra.js`, `guide-more.js`, and `guide-reference.js` contain the question-led system/reference articles.
- `strategy-data.js` contains beginner routes and practical guides for draws, Raids, stages, collection, and farming.
- `tools/build-stage-data.py` regenerates the stage index when given the decoded 1.0.18 table directory and local English translation file with `--tables` and `--lang`. These local inputs are not included in the published site.
- `tools/translate-ability-descriptions.py` fills English ability descriptions in the static catalog using the local 1.0.18 tables and research translation files.
- `app.js` builds navigation, filters, search, catalog detail pages, stage pages, and guide pages.

Catalogs describe the 1.0.18 data snapshot. Live banners, shop stock, season rules, and event details can change; the relevant guides point players to the current in-game view or official notice. Tier-list recommendations are dated community snapshots, not game data.

## Add guide information

Add an article to an existing category in a guide data file, or add a category with `{category: "Category name", items: [...]}`. Each article has an `id`, `title`, `summary`, searchable `tags`, `updated`, and `sections`. Sections have a `title` and an `html` string. Add a linked `source` for claims that depend on a version, notice, or community reference.

All data scripts are loaded before `app.js` in `index.html`. Use `/` to focus global search. The global search covers Dragon and Orb fields, stage entries, and guide text.

## Publish

GitHub Actions deploys changes pushed to `main`. GitHub Pages uses the **GitHub Actions** source. The published site is <https://zokkaxdj9.github.io/dv3-game-guide/>.

## Sources and attribution

Core catalog data comes from the user-supplied Dragon Village 3 version 1.0.18 package. English table labels use the supplied DV3 Research Complete corpus. Later or rotating rules link to official Dragon Village 3 community notices; dated tier-list notes link to the community article used. This is an independent fan guide and is not affiliated with Highbrow.
