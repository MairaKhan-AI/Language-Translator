import html

import streamlit as st
from deep_translator import GoogleTranslator
from translator import LANGUAGES

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------
# Custom Styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* ================================
       Global
       ================================ */

    .stApp {
        background: #f7faf8;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.5rem;
        padding-bottom: 2rem;
    }


    /* ================================
       Header
       ================================ */

    .hero {
        text-align: center;
        padding: 0.5rem 0 2rem 0;
    }

    .hero h1 {
        color: #176b4d;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .hero p {
        color: #66756e;
        font-size: 1.05rem;
        margin-top: 0.5rem;
    }


    /* ================================
       Language Section
       ================================ */

    .language-label {
        color: #176b4d;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }

    .language-direction {
        text-align: center;
        font-size: 1.4rem;
        color: #176b4d;
        padding-top: 1.65rem;
    }


    /* ================================
       Select Boxes
       ================================ */

    .stSelectbox > div > div {
        border-radius: 10px;
        border-color: #d5e4dc;
        background: #ffffff;
    }


    /* ================================
       Panel Titles
       ================================ */

    .panel-title {
        color: #34463e;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.45rem;
    }


    /* ================================
       Text Areas
       ================================ */

    .stTextArea textarea {
        min-height: 250px;
        border-radius: 12px;
        border: 1px solid #d5e4dc;
        background: #ffffff;
        color: #26352e !important;
        font-size: 1rem;
        line-height: 1.6;
        padding: 1rem;
        box-sizing: border-box;
    }

    .stTextArea textarea:focus {
        border-color: #176b4d;
        box-shadow: 0 0 0 1px #176b4d;
    }


    /* ================================
       Translation Box
       ================================ */

    .translation-box {
        width: 100%;
        height: 250px;

        box-sizing: border-box;

        padding: 1rem;

        border: 1px solid #d5e4dc;
        border-radius: 12px;

        background: #ffffff;

        color: #26352e;

        font-size: 1rem;
        line-height: 1.6;

        overflow-y: auto;
        overflow-x: hidden;

        white-space: pre-wrap;
        overflow-wrap: break-word;
        word-break: normal;

        /* Important for Arabic/Urdu/Persian/etc. */
        unicode-bidi: plaintext;
    }


    /* Placeholder */

    .translation-placeholder {
        color: #9aa7a1;
        font-style: italic;
        direction: ltr;
        text-align: left;
    }


    /* ================================
       Buttons
       ================================ */

    .stButton > button {
        min-height: 44px;
        border-radius: 10px;
        font-weight: 600;
        transition: 0.2s ease;
    }

    .stButton > button[kind="primary"] {
        background: #176b4d;
        border: 1px solid #176b4d;
        color: white;
    }

    .stButton > button[kind="primary"]:hover {
        background: #12543c;
        border-color: #12543c;
        color: white;
    }

    .stButton > button:not([kind="primary"]) {
        background: white;
        border: 1px solid #176b4d;
        color: #176b4d;
    }

    .stButton > button:not([kind="primary"]):hover {
        background: #eef7f2;
        border-color: #12543c;
        color: #12543c;
    }


    /* ================================
       Status Information
       ================================ */

    .status {
        text-align: center;
        color: #66756e;
        font-size: 0.84rem;
        margin-top: 1.2rem;
    }


    /* ================================
       Footer
       ================================ */

    .footer {
        text-align: center;
        color: #7a8781;
        font-size: 0.82rem;
        padding-top: 0.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# RTL Language Support
# --------------------------------------------------

RTL_CODES = {
    "ar",  # Arabic
    "fa",  # Persian
    "he",  # Hebrew
    "iw",  # Hebrew (Google Translate code)
    "ur",  # Urdu
    "ps",  # Pashto
    "sd",  # Sindhi
}


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "last_source" not in st.session_state:
    st.session_state.last_source = ""

if "last_target" not in st.session_state:
    st.session_state.last_target = ""


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🌍 Language Translator</h1>
        <p>Translate naturally. Connect globally.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Language Selection
# --------------------------------------------------

language_col1, direction_col, language_col2 = st.columns([5, 1, 5])


with language_col1:

    st.markdown(
        '<div class="language-label">From</div>',
        unsafe_allow_html=True,
    )

    source = st.selectbox(
        "Source Language",
        list(LANGUAGES.keys()),
        label_visibility="collapsed",
    )


with direction_col:

    st.markdown(
        '<div class="language-direction">→</div>',
        unsafe_allow_html=True,
    )


with language_col2:

    st.markdown(
        '<div class="language-label">To</div>',
        unsafe_allow_html=True,
    )

    target = st.selectbox(
        "Target Language",
        list(LANGUAGES.keys()),
        index=1,
        label_visibility="collapsed",
    )


st.write("")


# --------------------------------------------------
# Determine Text Direction
# --------------------------------------------------

target_code = LANGUAGES[target]

is_rtl = target_code in RTL_CODES

if is_rtl:
    text_direction = "rtl"
    text_alignment = "right"
else:
    text_direction = "ltr"
    text_alignment = "left"


# --------------------------------------------------
# Translation Workspace
# --------------------------------------------------

source_col, result_col = st.columns(
    2,
    gap="large",
)


# --------------------------------------------------
# Source Text
# --------------------------------------------------

with source_col:

    st.markdown(
        '<div class="panel-title">✍️ Original Text</div>',
        unsafe_allow_html=True,
    )

    text = st.text_area(
        "Original text",
        placeholder="Type or paste your text here...",
        height=250,
        label_visibility="collapsed",
        key="source_text",
    )


# --------------------------------------------------
# Translation Result
# --------------------------------------------------

with result_col:

    st.markdown(
        '<div class="panel-title">✨ Translation</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.translated_text:

        # Safely escape translated text before inserting it into HTML.
        translated_text = html.escape(st.session_state.translated_text)

        st.markdown(
            f"""
            <div
                class="translation-box"
                dir="{text_direction}"
                style="
                    direction: {text_direction};
                    text-align: {text_alignment};
                    unicode-bidi: plaintext;
                "
            >{translated_text}</div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <div
                class="translation-box translation-placeholder"
                dir="ltr"
            >
                Your translation will appear here...
            </div>
            """,
            unsafe_allow_html=True,
        )

# --------------------------------------------------
# Clear Function
# --------------------------------------------------


def clear_translation():
    st.session_state.source_text = ""
    st.session_state.translated_text = ""
    st.session_state.last_source = ""
    st.session_state.last_target = ""


# --------------------------------------------------
# Action Buttons
# --------------------------------------------------

st.write("")

button_col1, button_col2, spacer = st.columns([1, 1, 2])


with button_col1:

    translate_btn = st.button(
        "🔄 Translate",
        type="primary",
        use_container_width=True,
    )


with button_col2:

    clear_btn = st.button(
        "🧹 Clear",
        use_container_width=True,
        on_click=clear_translation,
    )

# --------------------------------------------------
# Translation Logic
# --------------------------------------------------

if translate_btn:

    if not text.strip():

        st.warning("⚠️ Please enter some text to translate.")

    elif source == target:

        st.warning("⚠️ Source and target languages cannot be the same.")

    else:

        try:

            with st.spinner("Translating..."):

                translated = GoogleTranslator(
                    source=LANGUAGES[source],
                    target=LANGUAGES[target],
                ).translate(text)

            st.session_state.translated_text = translated
            st.session_state.last_source = source
            st.session_state.last_target = target

            st.rerun()

        except Exception:

            st.error(
                "Translation failed. Please check your "
                "internet connection or selected language."
            )


# --------------------------------------------------
# Application Information
# --------------------------------------------------

st.markdown(
    f"""
    <div class="status">
        🌐 {len(LANGUAGES)} languages
        &nbsp;•&nbsp;
        ⚡ Powered by Google Translate
        &nbsp;•&nbsp;
        🐍 Built with Python & Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption("Developed by Maira Khan • 2026")
