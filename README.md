# 🃏 MTG Card Browser

> A slick little **Streamlit** app for browsing _Magic: The Gathering_ cards straight from [Scryfall](https://scryfall.com) bulk data — with live previews, prices, and inline editing.

<p align="center">
  <img alt="Streamlit" src="https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.14%2B-3776AB?logo=python&logoColor=white">
  <img alt="Pandas" src="https://img.shields.io/badge/Powered%20by-pandas-150458?logo=pandas&logoColor=white">
  <img alt="Data" src="https://img.shields.io/badge/Data-Scryfall-EAB308">
</p>

---

## ✨ What it does

[`run_streamlit_test.py`](run_streamlit_test.py) spins up a one-screen web app that lets you:

- 🖼️ **See the cards** — small preview art rendered right inside the table
- 🔎 **Filter by set** — type a set name and instantly narrow the list
- 💲 **Check the price** — USD value pulled from Scryfall, formatted as currency
- ✏️ **Edit inline** — flip on edit mode to tweak the data live in the grid

| Column      | Source field    | Notes                          |
| ----------- | --------------- | ------------------------------ |
| `Preview`   | `image_uris.small` | Rendered as an image          |
| `Name`      | `name`          |                                |
| `Mana Cost` | `mana_cost`     |                                |
| `Type`      | `type_line`     |                                |
| `Rarity`    | `rarity`        | Capitalized for display        |
| `Set`       | `set_name`      | Used by the filter             |
| `USD`       | `prices.usd`    | Formatted as `$%.2f`           |

---

## 🚀 Quick start

### 1. Get the card data

The app reads from a `default-cards.json` file — Scryfall's
[**Default Cards** bulk export](https://scryfall.com/docs/api/bulk-data).
Download it and drop it in the project root:

```bash
# grab the latest "default_cards" bulk download URL from the Scryfall API
curl -L -o default-cards.json "$(curl -s https://api.scryfall.com/bulk-data \
  | python -c 'import json,sys; print(next(d["download_uri"] for d in json.load(sys.stdin)["data"] if d["type"]=="default_cards"))')"
```

> On Windows PowerShell:
> ```powershell
> $uri = (Invoke-RestMethod https://api.scryfall.com/bulk-data).data `
>   | Where-Object type -eq 'default_cards' | Select-Object -Expand download_uri
> Invoke-WebRequest $uri -OutFile default-cards.json
> ```

### 2. Install dependencies

This project uses [`uv`](https://github.com/astral-sh/uv):

```bash
uv sync
```

### 3. Run it

```bash
uv run streamlit run run_streamlit_test.py
```

Streamlit opens the app in your browser (usually <http://localhost:8501>).

---

## 🕹️ Using the app

1. The table loads every card from `default-cards.json` (cached, so it's only parsed once).
2. Type a **set name** into the box — e.g. `The Lord of the Rings: Tales of Middle-earth` —
   to filter to just that set. Matching is case-insensitive and matches the full name.
3. Toggle **Enable editing** to switch from a read-only `st.dataframe` to an
   editable `st.data_editor`.

---

## 🧠 How it works

```text
default-cards.json  ──▶  load_data()  ──▶  pandas DataFrame  ──▶  filter by set  ──▶  st.dataframe / st.data_editor
   (Scryfall bulk)        @st.cache_data        7 columns           text_input            with column_config
```

- **`@st.cache_data`** keeps the JSON parse + DataFrame build off the hot path on every rerun.
- **`column_config`** turns the `Preview` column into images and money-formats `USD`.

---

## 📦 Requirements

- Python **3.14+**
- [`streamlit`](https://streamlit.io) · [`pandas`](https://pandas.pydata.org)
- A local `default-cards.json` from Scryfall

---

<p align="center"><sub>Card data courtesy of <a href="https://scryfall.com">Scryfall</a>. Not affiliated with Wizards of the Coast.</sub></p>
