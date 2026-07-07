# 🎯 IdeaRadar

Scan your project idea against GitHub and Product Hunt to see how saturated the space is — and get specific suggestions to make it more unique.

No more finding out someone already built your idea *after* you've spent a week on it.

## How it works

1. **Describe your idea** in plain text
2. **Search** — checks GitHub (repos) and Product Hunt (products) for similar existing work
3. **Score** — calculated directly from real result counts (fewer matches = more original), not a guessed number
4. **Analyze** — Groq's Llama 3.3 explains what already exists, how to stand out, and whether the space is growing or saturated

## Tech stack

`GitHub API` (repo search) · `Product Hunt API` (product search) · `Groq API` (Llama 3.3 analysis) · `Streamlit` (UI)

## Run it locally

```bash
git clone https://github.com/POORVIKA0608/IdeaRadar.git
cd IdeaRadar
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Add a `.env` file:
```
GROQ_API_KEY=your_groq_key_here
GITHUB_TOKEN=your_github_token_here
PRODUCTHUNT_TOKEN=your_producthunt_token_here
```

Then run:
```bash
streamlit run app.py
```

## Example

> **Idea:** "AI resume maker"
> **Score:** 20/100 — Highly competitive
> **Found:** 491 GitHub repos, 0 Product Hunt products
> **Verdict:** Overly saturated — hard to differentiate without a specific niche angle

## Limitations

- Score is based on result count only, not deep semantic similarity
- Product Hunt search quality depends on how the idea is phrased
- No historical trend data (can't yet show if a space is growing/shrinking over time)