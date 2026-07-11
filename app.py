import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import tempfile

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- INITIALIZE STATE ---------------- #
if "source_lang" not in st.session_state:
    st.session_state.source_lang = "English"
if "target_lang" not in st.session_state:
    st.session_state.target_lang = "Hindi"
if "translated_output" not in st.session_state:
    st.session_state.translated_output = ""
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* ---------- Global ---------- */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    background-attachment: fixed;
}

/* ---------- Headings ---------- */
.title {
    text-align: center;
    font-size: 48px;
    font-weight: 700;
    color: white;
    margin-bottom: 8px;
}

.subtitle {
    text-align: center;
    color: #F8FAFC;
    font-size: 18px;
    margin-bottom: 30px;
}

/* ---------- Main Card ---------- */
.main-card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 24px;
    padding: 35px;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 10px 35px rgba(0,0,0,0.25);
}

/* ---------- Input ---------- */
textarea {
    border-radius: 15px !important;
    border: 2px solid #E5E7EB !important;
    font-size: 16px !important;
}

/* ---------- Select Box ---------- */
div[data-baseweb="select"] > div {
    border-radius: 12px !important;
    border: 2px solid #E5E7EB !important;
}

/* ---------- Buttons ---------- */
.stButton > button {
    width: 100%;
    height: 52px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(90deg,#4F46E5,#6366F1);
    color: white;
    font-size: 17px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(79,70,229,.4);
}

/* ---------- Result ---------- */
.result {
    background: white;
    color: #111827;
    border-left: 6px solid #4F46E5;
    border-radius: 15px;
    padding: 20px;
    margin-top: 20px;
    font-size: 20px;
    line-height: 1.8;
    box-shadow: 0 8px 18px rgba(0,0,0,.15);
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(18px);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ---------- Footer ---------- */
footer {
    text-align: center;
    color: white;
    margin-top: 40px;
    font-size: 15px;
}

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #6366F1;
    border-radius: 20px;
}

::-webkit-scrollbar-track {
    background: transparent;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("🌍 AI Translator")
st.sidebar.info(
"""
Professional Language Translator
✔ 100+ Languages
✔ Text-to-Speech
✔ Copy Translation
✔ Download Output
"""
)

dark = st.sidebar.toggle("🌙 Dark Mode")

# ---------------- HEADER ---------------- #
st.markdown("<div class='title'>🌍 AI Language Translator</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Translate text instantly into 100+ languages</div>", unsafe_allow_html=True)
st.markdown("<div class='main-card'>", unsafe_allow_html=True)

languages = {
    "English": "en", "Hindi": "hi", "French": "fr", "German": "de",
    "Spanish": "es", "Italian": "it", "Japanese": "ja", "Korean": "ko",
    "Chinese": "zh-CN", "Arabic": "ar", "Russian": "ru", "Portuguese": "pt",
    "Bengali": "bn", "Punjabi": "pa", "Tamil": "ta", "Telugu": "te",
    "Gujarati": "gu", "Urdu": "ur"
}

col1, col2 = st.columns(2)
with col1:
    source = st.selectbox("Translate From", list(languages.keys()), key="source_lang")
with col2:
    target = st.selectbox("Translate To", list(languages.keys()), key="target_lang")

text = st.text_area("Enter Text", height=220, placeholder="Type or paste your text here...")
chars = len(text)
words = len(text.split())
st.caption(f"Characters: {chars} | Words: {words}")

# ---------------- TRANSLATE & SWAP ---------------- #
col3, col4 = st.columns([5, 1])
with col3:
    translate = st.button("🚀 Translate")
with col4:
    swap = st.button("🔄")

if swap:
    old_source = st.session_state.source_lang
    st.session_state.source_lang = st.session_state.target_lang
    st.session_state.target_lang = old_source
    st.rerun()

if translate:
    if text.strip() == "":
        st.warning("⚠ Please enter some text.")
    else:
        with st.spinner("Translating..."):
            translated = GoogleTranslator(
                source=languages[source],
                target=languages[target]
            ).translate(text)
            st.session_state.translated_output = translated

        st.session_state.history.insert(
            0,
            {
                "from": source,
                "to": target,
                "input": text,
                "output": translated
            }
        )

# ---------------- DISPLAY & EXTRA ACTIONS ---------------- #
if st.session_state.translated_output:
    st.success("✅ Translation Complete")
    st.markdown("### ✨ Translated Text")
    st.markdown(
        f"<div class='result'>{st.session_state.translated_output}</div>",
        unsafe_allow_html=True
    )
    
    st.write("📋 **Copy Translation:**")
    st.code(st.session_state.translated_output, language=None)

    col_actions1, col_actions2 = st.columns(2)
    
    with col_actions1:
        st.download_button(
            label="📥 Download Translation",
            data=st.session_state.translated_output,
            file_name="translation.txt",
            mime="text/plain"
        )
        
    with col_actions2:
        if st.button("🔊 Listen"):
            with st.spinner("Generating Audio..."):
                tts = gTTS(st.session_state.translated_output, lang=languages[target])
                temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(temp.name)
                
                with open(temp.name, "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
                
                try:
                    os.unlink(temp.name)
                except Exception:
                    pass

# ---------------- HISTORY ---------------- #
st.sidebar.markdown("---")
st.sidebar.subheader("🕒 Translation History")

if len(st.session_state.history) == 0:
    st.sidebar.write("No translations yet.")
else:
    for item in st.session_state.history[:10]:
        with st.sidebar.expander(f"{item['from']} ➜ {item['to']}"):
            st.write("**Input:**")
            st.write(item["input"])
            st.write("**Output:**")
            st.write(item["output"])

# ---------------- FOOTER ---------------- #
st.markdown("</div>", unsafe_allow_html=True)
st.markdown(
"""
<footer>
Made with ❤️ by <b>Anisha Tripathi</b><br>
AI Language Translator • CodeAlpha Internship
</footer>
""",
unsafe_allow_html=True
)
