import streamlit as st
import requests
import os
import re
import html
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="IdeaRadar", page_icon="🎯", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #eef0ff 0%, #f4f6fb 40%, #fdf0ff 100%);
    background-attachment: fixed;
}

#MainMenu, footer, header { visibility: hidden; }

/* remove Streamlit's default block padding that creates empty bars */
.block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; }
div[data-testid="stVerticalBlock"] > div:empty { display: none !important; }
div[data-testid="stVerticalBlock"] > div[style*="height"] { display: none !important; }

/* target the stMarkdown containers to add card styling without open/close divs */
div[data-testid="stMarkdownContainer"] .header-wrap,
div[data-testid="stMarkdownContainer"] .input-card-static {
    display: block;
}

.header-wrap {
    display: flex; align-items: center; gap: 14px;
    background: white; border-radius: 16px;
    padding: 1.2rem 1.6rem; margin-bottom: 0.8rem;
    border: 1px solid #e8ecf4;
    box-shadow: 0 2px 12px rgba(99,102,241,0.06);
}
.header-icon {
    width: 44px; height: 44px; border-radius: 12px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
}
.header-title { font-size: 1.4rem; font-weight: 800; color: #1e1b4b; letter-spacing: -0.5px; }
.header-sub { font-size: 0.82rem; color: #94a3b8; margin-top: 1px; }

/* input section — style the Streamlit elements directly, no wrapper divs */
.input-label { font-size: 0.9rem; font-weight: 700; color: #1e1b4b; margin-bottom: 4px; }
.input-hint { font-size: 0.78rem; color: #94a3b8; margin-bottom: 0.8rem; }

.stTextArea textarea {
    background: #f8faff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #1e1b4b !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}

.stButton button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important; font-weight: 700 !important;
    border: none !important; border-radius: 10px !important;
    width: 100% !important; padding: 0.65rem !important;
    font-size: 0.95rem !important; letter-spacing: 0.2px !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.3) !important;
}

.metric-card {
    background: white; border-radius: 14px;
    border: 1px solid #e8ecf4; padding: 1.2rem;
    text-align: center;
}
.metric-label { font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
.metric-value { font-size: 2.4rem; font-weight: 800; line-height: 1; }
.metric-sub { font-size: 0.78rem; margin-top: 4px; font-weight: 600; }

.verdict-card {
    border-radius: 14px; padding: 1.1rem 1.4rem;
    margin-bottom: 1.2rem; display: flex; gap: 12px; align-items: flex-start;
}
.verdict-icon { font-size: 1.3rem; margin-top: 1px; }
.verdict-title { font-size: 0.8rem; font-weight: 700; margin-bottom: 3px; }
.verdict-body { font-size: 0.88rem; color: #334155; line-height: 1.55; }

.section-card {
    background: white; border-radius: 14px;
    border: 1px solid #e8ecf4; padding: 1.3rem 1.4rem;
    margin-bottom: 1.2rem;
}
.section-title {
    font-size: 0.82rem; font-weight: 700; color: #64748b;
    text-transform: uppercase; letter-spacing: 0.6px;
    margin-bottom: 1rem; padding-bottom: 0.6rem;
    border-bottom: 1px solid #f1f5f9;
}

.repo-row {
    border: 1px solid #f1f5f9; border-radius: 10px;
    padding: 0.85rem 1rem; margin-bottom: 0.6rem;
    background: #fafbff;
}
.repo-name { font-size: 0.88rem; font-weight: 700; color: #6366f1; text-decoration: none; }
.repo-meta { font-size: 0.75rem; color: #94a3b8; margin-top: 2px; }
.repo-desc { font-size: 0.82rem; color: #475569; margin-top: 4px; line-height: 1.4; }

.ph-row {
    border: 1px solid #fde8f0; border-radius: 10px;
    padding: 0.85rem 1rem; margin-bottom: 0.6rem;
    background: #fff8fb;
}
.ph-name { font-size: 0.88rem; font-weight: 700; color: #e11d48; }
.ph-meta { font-size: 0.75rem; color: #94a3b8; margin-top: 2px; }
.ph-desc { font-size: 0.82rem; color: #475569; margin-top: 4px; line-height: 1.4; }

.empty-note { text-align: center; padding: 1.5rem; font-size: 0.85rem; color: #94a3b8; }

.analysis-section { margin-bottom: 1rem; }
.analysis-heading { font-size: 0.82rem; font-weight: 700; color: #475569; margin-bottom: 6px; }
.analysis-item { font-size: 0.85rem; color: #334155; margin-bottom: 4px; padding-left: 12px; position: relative; line-height: 1.5; }
.analysis-item::before { content: "·"; position: absolute; left: 0; color: #6366f1; }
</style>
""", unsafe_allow_html=True)

# ---- clients ----
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
PH_TOKEN = os.environ.get("PRODUCTHUNT_TOKEN")

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
# Guard against sending "token None" as a header when GITHUB_TOKEN is missing
GITHUB_HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}


# ---- score from real data (not LLM) ----
def calculate_score(total_github, total_ph):
    """
    Score based on actual search counts.
    Fewer matches = more original = higher score.
    GitHub count weighted more than PH since there are more repos.
    """
    github_score = max(0, 100 - (total_github * 0.15))
    ph_score = max(0, 100 - (total_ph * 2.5))
    score = int((github_score * 0.6) + (ph_score * 0.4))
    return max(5, min(95, score))


# ---- github search ----
@st.cache_data(ttl=3600, show_spinner=False)
def search_github(query, max_results=5):
    url = "https://api.github.com/search/repositories"
    params = {"q": query[:100], "sort": "stars", "order": "desc", "per_page": max_results}
    try:
        response = requests.get(url, headers=GITHUB_HEADERS, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        show_warning(f"GitHub search failed: {e}")
        return [], 0

    data = response.json()
    repos = []
    for repo in data.get("items", []):
        repos.append({
            "name": repo["full_name"],
            "description": repo.get("description") or "No description",
            "stars": repo["stargazers_count"],
            "url": repo["html_url"],
            "language": repo.get("language", "Unknown")
        })
    return repos, data.get("total_count", 0)


# ---- product hunt search ----
@st.cache_data(ttl=3600, show_spinner=False)
def search_producthunt(query):
    if not PH_TOKEN:
        return [], 0

    # NOTE: Product Hunt's v2 GraphQL API has no free-text "search" argument on `posts`.
    # We fetch a batch of posts (sorted by votes) and filter client-side by keyword match
    # against name/tagline. This means "total" below is an estimate based on the fetched
    # batch, not PH's full index.
    graphql_query = """
    query RecentPosts($first: Int!) {
        posts(first: $first, order: VOTES) {
            edges {
                node { name tagline votesCount website createdAt }
            }
        }
    }
    """
    headers = {
        "Authorization": f"Bearer {PH_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    try:
        response = requests.post(
            "https://api.producthunt.com/v2/api/graphql",
            json={"query": graphql_query, "variables": {"first": 50}},
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        show_warning(f"Product Hunt search failed: {e}")
        return [], 0

    data = response.json()
    if "errors" in data:
        show_warning(f"Product Hunt API error: {data['errors'][0].get('message', 'unknown error')}")
        return [], 0

    edges = data.get("data", {}).get("posts", {}).get("edges", [])

    # simple keyword match against name + tagline
    keywords = [w.lower() for w in re.findall(r"\w+", query) if len(w) > 2]

    def matches(node):
        haystack = f"{node.get('name', '')} {node.get('tagline', '')}".lower()
        return any(kw in haystack for kw in keywords)

    matched = [edge["node"] for edge in edges if matches(edge["node"])]

    posts = []
    for node in matched[:5]:
        posts.append({
            "name": node["name"],
            "tagline": node.get("tagline", ""),
            "votes": node.get("votesCount", 0),
            "url": node.get("website", "#"),
            "created": node.get("createdAt", "")[:10]
        })
    return posts, len(matched)


# ---- groq analysis (no score - we calculate that ourselves) ----
def analyze_idea(idea, repos, total_github, ph_posts, total_ph):
    if groq_client is None:
        show_warning("Groq API key not configured — skipping AI analysis.")
        return ""

    repo_summary = "\n".join([
        f"- {r['name']} ({r['stars']} stars): {r['description']}"
        for r in repos
    ]) if repos else "No similar repos found."

    ph_summary = "\n".join([
        f"- {p['name']} ({p['votes']} votes): {p['tagline']}"
        for p in ph_posts
    ]) if ph_posts else "No similar products found."

    prompt = f"""You are an expert product advisor. Analyze this project idea based on real search data.

PROJECT IDEA: {idea}

GITHUB DATA ({total_github} total similar repos):
{repo_summary}

PRODUCT HUNT DATA ({total_ph} total similar products):
{ph_summary}

Respond in this EXACT format with no extra text:

VERDICT:
[one punchy honest sentence about whether this is worth building]

WHAT ALREADY EXISTS:
[bullet 1]
[bullet 2]
[bullet 3]

HOW TO STAND OUT:
[specific suggestion 1]
[specific suggestion 2]
[specific suggestion 3]

MARKET INSIGHT:
[1-2 sentences about whether the space is growing, shrinking, or saturated]"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        show_warning(f"AI analysis failed: {e}")
        return ""


def parse_section(text, section_name):
    if not text:
        return ""
    pattern = rf'{section_name}:\s*(.*?)(?=\n[A-Z ]+:|$)'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def show_warning(message):
    """Styled warning banner matching the app's card aesthetic (used instead of st.warning)."""
    st.markdown(
        f'<div class="section-card" style="border-color:#fecdd3;background:#fff1f2;'
        f'color:#dc2626;font-size:0.85rem;font-weight:600;">⚠️ {html.escape(message)}</div>',
        unsafe_allow_html=True
    )


def build_list_items(text):
    """Turn newline-separated bullet text into escaped, single-line analysis-item divs."""
    if not text:
        return ""
    items = []
    for line in text.split("\n"):
        cleaned = line.strip().lstrip("-·•").strip()
        if cleaned:
            items.append(f'<div class="analysis-item">{html.escape(cleaned)}</div>')
    return "".join(items)


# ---- UI ----
st.markdown("""
<div class="header-wrap">
<div class="header-icon">🎯</div>
<div>
<div class="header-title">IdeaRadar</div>
<div class="header-sub">Scan your idea · Know the landscape · Stand out</div>
</div>
</div>
<div class="input-label">Describe your project idea</div>
<div class="input-hint">Be specific — the more detail you give, the more accurate the scan</div>
""", unsafe_allow_html=True)

idea = st.text_area(
    "idea_input",
    placeholder="e.g. A tool that lets developers ask questions about any GitHub repo using AI and returns answers with exact file and line citations...",
    height=120,
    label_visibility="collapsed"
)
scan = st.button("🎯  Scan My Idea")

if scan and idea:
    with st.spinner("Searching GitHub..."):
        repos, total_github = search_github(idea)

    with st.spinner("Searching Product Hunt..."):
        ph_posts, total_ph = search_producthunt(idea[:80])

    with st.spinner("Running AI analysis..."):
        score = calculate_score(total_github, total_ph)
        analysis = analyze_idea(idea, repos, total_github, ph_posts, total_ph)

    # score color
    if score >= 65:
        score_color = "#16a34a"
        score_label = "Fairly original"
        verdict_bg = "#f0fdf4"
        verdict_border = "#bbf7d0"
        verdict_icon = "🟢"
    elif score >= 35:
        score_color = "#d97706"
        score_label = "Moderately saturated"
        verdict_bg = "#fffbeb"
        verdict_border = "#fde68a"
        verdict_icon = "🟡"
    else:
        score_color = "#dc2626"
        score_label = "Highly competitive"
        verdict_bg = "#fff1f2"
        verdict_border = "#fecdd3"
        verdict_icon = "🔴"

    # metric cards row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Originality Score</div>'
            f'<div class="metric-value" style="color:{score_color};">{score}</div>'
            f'<div class="metric-sub" style="color:{score_color};">{score_label}</div></div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">GitHub Repos</div>'
            f'<div class="metric-value" style="color:#1e1b4b;">{total_github:,}</div>'
            f'<div class="metric-sub" style="color:#94a3b8;">similar repos found</div></div>',
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Product Hunt</div>'
            f'<div class="metric-value" style="color:#1e1b4b;">{total_ph}</div>'
            f'<div class="metric-sub" style="color:#94a3b8;">similar products found</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    # verdict banner
    verdict_text = html.escape(parse_section(analysis, "VERDICT"))
    if verdict_text:
        st.markdown(
            f'<div class="verdict-card" style="background:{verdict_bg};border:1px solid {verdict_border};">'
            f'<div class="verdict-icon">{verdict_icon}</div>'
            f'<div><div class="verdict-title" style="color:{score_color};">Verdict</div>'
            f'<div class="verdict-body">{verdict_text}</div></div></div>',
            unsafe_allow_html=True
        )

    # analysis + repos side by side
    col4, col5 = st.columns(2)

    with col4:
        exists_text = parse_section(analysis, "WHAT ALREADY EXISTS")
        standout_text = parse_section(analysis, "HOW TO STAND OUT")
        market_text = html.escape(parse_section(analysis, "MARKET INSIGHT"))

        exists_items = build_list_items(exists_text)
        standout_items = build_list_items(standout_text)

        market_block = (
            f'<div style="margin-top:1rem;padding:0.8rem;background:#f8faff;border-radius:8px;'
            f'border:1px solid #e2e8f0;font-size:0.82rem;color:#475569;line-height:1.55;">{market_text}</div>'
        ) if market_text else ""

        analysis_html = '<div class="section-card"><div class="section-title">Analysis</div>'
        if exists_items:
            analysis_html += '<div class="analysis-heading">What already exists</div>' + exists_items
        if standout_items:
            analysis_html += '<div class="analysis-heading" style="margin-top:1rem;">How to stand out</div>' + standout_items
        analysis_html += market_block
        analysis_html += '</div>'

        if not (exists_items or standout_items or market_block):
            analysis_html = '<div class="section-card"><div class="section-title">Analysis</div><div class="empty-note">No AI analysis available.</div></div>'

        st.markdown(analysis_html, unsafe_allow_html=True)

    with col5:
        # github repos — one block (single-line strings, no 4+ space indentation)
        if repos:
            repo_html = "".join([
                f'<div class="repo-row">'
                f'<a class="repo-name" href="{html.escape(r["url"])}" target="_blank">{html.escape(r["name"])}</a>'
                f'<div class="repo-meta">⭐ {r["stars"]:,} · {html.escape(r["language"] or "Unknown")}</div>'
                f'<div class="repo-desc">{html.escape(r["description"][:120])}{"..." if len(r["description"]) > 120 else ""}</div>'
                f'</div>'
                for r in repos[:4]
            ])
        else:
            repo_html = '<div class="empty-note">No similar repos found — great sign!</div>'

        st.markdown(
            f'<div class="section-card"><div class="section-title">Similar GitHub Repos</div>{repo_html}</div>',
            unsafe_allow_html=True
        )

        # product hunt — one block (single-line strings, no 4+ space indentation)
        if ph_posts:
            ph_html = "".join([
                f'<div class="ph-row">'
                f'<div class="ph-name">{html.escape(p["name"])}</div>'
                f'<div class="ph-meta">👍 {p["votes"]} votes · {html.escape(p["created"])}</div>'
                f'<div class="ph-desc">{html.escape(p["tagline"][:120])}{"..." if len(p["tagline"]) > 120 else ""}</div>'
                f'</div>'
                for p in ph_posts[:4]
            ])
        else:
            ph_html = '<div class="empty-note">No similar products found — opportunity!</div>'

        st.markdown(
            f'<div class="section-card"><div class="section-title">Similar Products on Product Hunt</div>{ph_html}</div>',
            unsafe_allow_html=True
        )

elif scan and not idea:
    show_warning("Describe your idea first.")