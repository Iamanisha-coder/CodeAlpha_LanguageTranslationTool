import streamlit as st
from deep_translator import GoogleTranslator
import pyperclip
from gtts import gTTS
import base64
import os
import tempfile

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]{
    font-family:'Poppins', sans-serif;
}

.stApp{
background:linear-gradient(135deg,#667eea,#764ba2);
}

.main-card{
background:rgba(255,255,255,0.18);
backdrop-filter:blur(15px);
padding:35px;
border-radius:25px;
box-shadow:0 10px 35px rgba(0,0,0,.25);
}

.title{
text-align:center;
font-size:42px;
font-weight:700;
color:white;
}

.subtitle{
text-align:center;
color:#eeeeee;
margin-bottom:30px;
font-size:18px;
}

.result{
background:white;
padding:20px;
border-radius:15px;
font-size:20px;
font-weight:500;
color:#222;
box-shadow:0 4px 12px rgba(0,0,0,.15);
}

footer{
text-align:center;
color:white;
margin-top:40px;
}

.stButton>button{
width:100%;
height:55px;
border-radius:12px;
border:none;
background:#4F46E5;
color:white;
font-size:18px;
font-weight:bold;
transition:0.3s;
}

.stButton>button:hover{
background:#3730A3;
transform:scale(1.02);
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

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- HEADER ---------------- #

st.markdown("<div class='title'>🌍 AI Language Translator</div>",
unsafe_allow_html=True)

st.markdown("<div class='subtitle'>Translate text instantly into 100+ languages</div>",
unsafe_allow_html=True)

st.markdown("<div class='main-card'>",unsafe_allow_html=True)

languages={
"English":"en",
"Hindi":"hi",
"French":"fr",
"German":"de",
"Spanish":"es",
"Italian":"it",
"Japanese":"ja",
"Korean":"ko",
"Chinese":"zh-CN",
"Arabic":"ar",
"Russian":"ru",
"Portuguese":"pt",
"Bengali":"bn",
"Punjabi":"pa",
"Tamil":"ta",
"Telugu":"te",
"Gujarati":"gu",
"Urdu":"ur"
}

col1,col2=st.columns(2)

with col1:
    source=st.selectbox(
        "Translate From",
        list(languages.keys())
    )

with col2:
    target=st.selectbox(
        "Translate To",
        list(languages.keys()),
        index=1
    )

text=st.text_area(
    "Enter Text",
    height=220,
    placeholder="Type or paste your text here..."
)

chars=len(text)
words=len(text.split())

st.caption(f"Characters: {chars} | Words: {words}")

# ---------------- TRANSLATE ---------------- #

translated_text = ""

col3, col4 = st.columns([5, 1])

with col3:
    translate = st.button("🚀 Translate")

with col4:
    swap = st.button("🔄")

# Swap Languages
if swap:
    source, target = target, source

# Translate
if translate:

    if text.strip() == "":
        st.warning("⚠ Please enter some text.")
    else:

        with st.spinner("Translating..."):

            translated_text = GoogleTranslator(
                source=languages[source],
                target=languages[target]
            ).translate(text)

        st.success("✅ Translation Complete")

        st.markdown("### ✨ Translated Text")

        st.markdown(
            f"<div class='result'>{translated_text}</div>",
            unsafe_allow_html=True
        )

        # Store history
        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.insert(
            0,
            {
                "from": source,
                "to": target,
                "input": text,
                "output": translated_text
            }
        )

# ---------------- COPY ---------------- #

if translated_text:

    if st.button("📋 Copy Translation"):
        pyperclip.copy(translated_text)
        st.success("Copied to Clipboard!")

# ---------------- DOWNLOAD ---------------- #

if translated_text:

    st.download_button(
        label="📥 Download Translation",
        data=translated_text,
        file_name="translation.txt",
        mime="text/plain"
    )

# ---------------- TEXT TO SPEECH ---------------- #

if translated_text:

    if st.button("🔊 Listen"):

        tts = gTTS(
            translated_text,
            lang=languages[target]
        )

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

        tts.save(temp.name)

        audio = open(temp.name, "rb")

        st.audio(audio.read())

# ---------------- HISTORY ---------------- #

st.sidebar.markdown("---")
st.sidebar.subheader("🕒 Translation History")

if "history" in st.session_state:

    if len(st.session_state.history) == 0:
        st.sidebar.write("No translations yet.")

    else:

        for item in st.session_state.history[:10]:

            with st.sidebar.expander(
                f"{item['from']} ➜ {item['to']}"
            ):
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
