<h1 align="center">📊 Group Chat Analysis</h1>
<p align="center">Discover who talks the most, how conversations grow over time, and who gets replies vs. gets ignored — in a clean Streamlit app and a reproducible Jupyter notebook.</p>

<p align="center">
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white"></a>
  <a href="https://streamlit.io/"><img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-app-FF4B4B?logo=streamlit&logoColor=white"></a>
  <a href="https://pandas.pydata.org/"><img alt="Pandas" src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white"></a>
  <a href="https://altair-viz.github.io/"><img alt="Altair" src="https://img.shields.io/badge/Altair-Charts-1F77B4"></a>
</p>

<p align="center">
  <a href="app.py">app.py</a> • <a href="main.ipynb">main.ipynb</a> • <a href="result.json">result.json</a>
</p>

---

## ✨ Highlights

- Upload a chat JSON and get:
  - Who talks the most (bar chart)
  - Chat growth per person over time (line charts)
  - Reply vs. ignore percentages by person
  - Top “who replies to whom” pairs
- Built with Streamlit for fast, interactive exploration.
- Notebook provides a reproducible analysis pipeline.

---

## 🚀 Quick Start

Create a virtual environment and install dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -U streamlit pandas altair matplotlib seaborn
```

Run the app:

```sh
streamlit run app.py
```

Open the notebook in VS Code:

- Open `main.ipynb` and Run All cells.
- It reads `result.json` and renders the same analyses in Matplotlib/Seaborn.

---

## 📈 What You’ll See

- Who talks the most:
  - Altair bar chart using aggregated counts per person.
- Chat growth over time:
  - Cumulative message counts per person by date (split into two groups for clarity).
- Replies and ignores:
  - Reply percentage per person computed as round(replies / messages × 100, 1); ignored = 100 − percentage.
- Top reply pairs:
  - “Person → Replied-to” with maximum counts per sender.

---

## 🔒 Data & Privacy

- Member display names are anonymized to generic labels (e.g., “User_1”, “User_2”) before plotting.
- Input format: a JSON with a top-level `messages` list (Telegram-style exports work). The notebook normalizes `df['messages']` into a flat table.

---

## 📝 Notes

- Charts in the app use Altair; the notebook uses Matplotlib/Seaborn.
- The app expects a single JSON upload and computes aggregates in-browser.
- The Streamlit app is currently tailored to the example JSON format used for this project; broader support for various group chat export schemas is in progress.

---

## 💡 Inspiration

This chat analysis focuses on a group I was part of for quite some time. In that group, we’d casually say things like “this person isn’t active” or “they don’t talk much.” One day, a friend jokingly said, “You’re a statistics student—why not do some analysis and come up with real stats?” That’s how this project came to life, and some of the results were genuinely surprising.

Important context: a few members accidentally deleted entire message histories. You can see this in the charts. For example, if two people were chatting and one person’s past messages were removed, it can skew metrics like “who gets ignored the most.” Keep this in mind when interpreting the graphs.

I’m actively adding more statistics and will include a feature to detect and handle deleted messages so they don’t distort the analysis.

---

## 📂 Project Structure

- `app.py`: Streamlit app for interactive charts and file upload.
- `main.ipynb`: Full analysis pipeline, plotting, and derived metrics.
- `result.json`: Example chat export used by both the app and notebook.
- `.gitignore`: Standard Git exclusions.

---
