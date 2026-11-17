import streamlit as st
from modules.pdf_extractor import extract_pdf_text
from modules.summarizer import load_summarizer, summarize_long_text

st.set_page_config(
    page_title="SmartSummarizer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Visual theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --ink: #182238;
    --muted: #68758b;
    --purple: #7357e8;
    --purple-dark: #5b43c7;
    --cyan: #37b9c8;
    --surface: #ffffff;
    --line: #e8eaf2;
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp {
    background:
      radial-gradient(circle at 88% 3%, rgba(115,87,232,.11), transparent 25rem),
      radial-gradient(circle at 4% 25%, rgba(55,185,200,.08), transparent 24rem),
      #f6f7fb;
    color: var(--ink);
}
.block-container { max-width: 1240px; padding-top: 2.1rem; padding-bottom: 3rem; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #171d35 0%, #222b4a 100%);
    border-right: 0;
}
[data-testid="stSidebar"] * { color: #eef1ff !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #c3cbe2 !important; }
[data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] { margin-top: .8rem; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.15); }
[data-testid="stSidebar"] .stCaption { color: #aeb8d4 !important; }
.hero {
    padding: 2rem 2.15rem;
    border-radius: 26px;
    background: linear-gradient(118deg, #202a4b 0%, #443b83 58%, #7357e8 100%);
    color: white;
    box-shadow: 0 18px 45px rgba(50,49,110,.18);
    position: relative;
    overflow: hidden;
    margin-bottom: 1.35rem;
}
.hero:after {
    content: "✦";
    position: absolute; right: 4%; top: -48px;
    font-size: 220px; line-height: 1; color: rgba(255,255,255,.07);
}
.hero-kicker {
    text-transform: uppercase; letter-spacing: .16em; font-size: .72rem;
    font-weight: 800; color: #b9e9f0; margin-bottom: .8rem;
}
.hero h1 {
    font-family: 'Manrope', sans-serif; font-size: clamp(2rem, 4vw, 3.25rem);
    line-height: 1.08; color: white; margin: 0 0 .7rem 0; font-weight: 800;
}
.hero p { color: #e2e5ff; font-size: 1.02rem; max-width: 680px; margin: 0; }
.pill-row { display:flex; gap:.55rem; flex-wrap:wrap; margin-top:1.25rem; }
.pill {
    border: 1px solid rgba(255,255,255,.22); background:rgba(255,255,255,.10);
    color:#f7f8ff; border-radius:999px; padding:.38rem .75rem; font-size:.78rem;
}
.section-title {
    font-family:'Manrope',sans-serif; font-size:1.2rem; font-weight:800;
    color:#202a43; margin:.35rem 0 .15rem 0;
}
.section-sub { color:var(--muted); font-size:.9rem; margin-bottom:1rem; }
.panel {
    background:var(--surface); border:1px solid var(--line); border-radius:20px;
    padding:1.2rem 1.3rem; box-shadow:0 8px 24px rgba(34,45,78,.045);
}
.metric {
    background:white; border:1px solid var(--line); border-radius:17px;
    padding:1rem 1.1rem; box-shadow:0 6px 18px rgba(34,45,78,.035);
}
.metric-label { color:#7b879a; font-size:.76rem; font-weight:700; text-transform:uppercase; letter-spacing:.08em; }
.metric-value { color:#202a43; font-family:'Manrope',sans-serif; font-size:1.45rem; font-weight:800; margin-top:.2rem; }
.drop-hint {
    border:1.5px dashed #b9b5ee; background:linear-gradient(135deg,#faf9ff,#f3fbfc);
    padding:1.1rem; border-radius:16px; color:#59647b; text-align:center; margin:.4rem 0 1rem;
}
.stButton > button, .stDownloadButton > button {
    border:0 !important; border-radius:12px !important; padding:.62rem 1.2rem !important;
    font-weight:700 !important; color:white !important;
    background:linear-gradient(100deg,#7357e8,#5c77e8) !important;
    box-shadow:0 7px 18px rgba(102,87,220,.20);
}
.stButton > button:hover, .stDownloadButton > button:hover { filter:brightness(1.06); transform:translateY(-1px); }
.stTextArea textarea { border-radius:13px !important; border:1px solid #e3e6ef !important; background:#fbfcff !important; }
[data-testid="stFileUploader"] {
    background:#fff; border:1px solid #e7e8f2; border-radius:17px; padding:.5rem;
}
[data-testid="stFileUploader"] section { border:0 !important; }
div[data-testid="stAlert"] { border-radius:13px; }
.result-card {
    background:linear-gradient(145deg,#fff 0%,#fbfaff 100%);
    border:1px solid #e8e5fb; border-radius:18px; padding:1.35rem;
    box-shadow:0 8px 25px rgba(48,43,100,.05); min-height:220px;
}
.result-label { color:#7357e8; font-size:.73rem; text-transform:uppercase; letter-spacing:.12em; font-weight:800; margin-bottom:.7rem; }
.footer-note { text-align:center; color:#98a1b2; font-size:.78rem; padding-top:2rem; }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ✨ SmartSummarizer")
    st.markdown("Your document, distilled.")
    st.divider()
    st.markdown("### ⚙️ Summary controls")
    length = st.select_slider(
        "Summary detail",
        options=["Short", "Medium", "Detailed"],
        value="Medium",
    )
    st.markdown("---")
    st.markdown("**🧠 AI model**")
    st.code("DistilBART CNN 12-6", language=None)
    st.caption("Pretrained BART-family transformer")
    st.markdown("**🔒 Privacy**")
    st.caption("Documents are processed locally on your machine. No paid API is used.")
    st.markdown("---")
    st.caption("Tip: Start with a text-based PDF. Scanned PDFs need OCR.")

# ---------- Hero ----------
st.markdown("""
<div class="hero">
  <div class="hero-kicker">AI-powered reading companion</div>
  <h1>Less reading.<br>More understanding.</h1>
  <p>Turn lengthy PDF documents into clear, focused summaries with a locally running BART Transformer.</p>
  <div class="pill-row">
    <span class="pill">✦ BART Transformer</span>
    <span class="pill">⌁ Local processing</span>
    <span class="pill">↓ Downloadable summaries</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Start with a document</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Upload your PDF and let SmartSummarizer pull out the ideas that matter.</div>', unsafe_allow_html=True)

uploaded = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")

if not uploaded:
    st.markdown("""
    <div class="drop-hint">
      <div style="font-size:2rem;margin-bottom:.25rem">📄</div>
      <b>Your next great summary starts here</b><br>
      <span style="font-size:.86rem">Choose a PDF using the upload control above · PDF files only</span>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, number, title, desc in [
        (c1, "01", "Upload", "Add a lecture note, article or research paper."),
        (c2, "02", "Summarize", "BART reads the text in manageable chunks."),
        (c3, "03", "Take it with you", "Review and download your concise summary."),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric">
              <div class="metric-label">STEP {number}</div>
              <div class="metric-value" style="font-size:1.08rem">{title}</div>
              <div style="color:#748096;font-size:.86rem;margin-top:.35rem">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="panel" style="margin:.7rem 0 1rem">
      <div style="color:#7b879a;font-size:.75rem;font-weight:800;letter-spacing:.1em">DOCUMENT READY</div>
      <div style="font-size:1.08rem;font-weight:800;color:#202a43;margin-top:.25rem">📎 {uploaded.name}</div>
      <div style="color:#7b879a;font-size:.82rem">{uploaded.size / 1024:.1f} KB · PDF document</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✨ Generate my summary", type="primary", use_container_width=False):
        with st.spinner("Reading your PDF..."):
            try:
                text = extract_pdf_text(uploaded.getvalue())
            except Exception as exc:
                st.error(f"Could not read this PDF: {exc}")
                st.stop()

        if not text.strip():
            st.error("No selectable text was found. This may be a scanned PDF; OCR is not included in this version.")
            st.stop()

        word_count = len(text.split())
        with st.spinner("Waking up BART and crafting your summary. The first run downloads the model..."):
            try:
                summarizer, tokenizer = load_summarizer()
                summary = summarize_long_text(text, summarizer, tokenizer, length)
            except Exception as exc:
                st.error(f"Summarization failed: {exc}")
                st.stop()

        st.success("Your summary is ready.")
        summary_words = len(summary.split())
        compression = round((1 - summary_words / max(word_count, 1)) * 100)

        m1, m2, m3 = st.columns(3)
        for col, label, value in [
            (m1, "SOURCE WORDS", f"{word_count:,}"),
            (m2, "SUMMARY WORDS", f"{summary_words:,}"),
            (m3, "SHORTER BY", f"{compression}%"),
        ]:
            with col:
                st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

        st.markdown("")
        left, right = st.columns([1.15, 0.85], gap="large")
        with left:
            st.markdown('<div class="result-card"><div class="result-label">✦ Your AI-generated summary</div>', unsafe_allow_html=True)
            st.markdown(summary)
            st.markdown('</div>', unsafe_allow_html=True)
            st.download_button(
                "⬇️ Download summary (.txt)",
                data=summary.encode("utf-8"),
                file_name=f"{uploaded.name.rsplit('.', 1)[0]}_summary.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with right:
            st.markdown('<div class="section-title">Document insights</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-sub">A quick look at the source text.</div>', unsafe_allow_html=True)
            st.text_area("Extracted text preview", text[:10000], height=300)
            st.caption(f"Summary detail: {length} · Model: DistilBART CNN 12-6")

st.markdown('<div class="footer-note">SmartSummarizer · Built with Streamlit, PyMuPDF and Hugging Face Transformers</div>', unsafe_allow_html=True)
