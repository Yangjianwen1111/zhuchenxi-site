import base64
import mimetypes
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="朱晨希 | 高中数学一对一教师",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit chrome so the page looks like the original site
st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden;}
      .block-container {padding: 0 !important; max-width: 100% !important;}
      [data-testid="stAppViewContainer"] > .main {padding: 0 !important;}
      [data-testid="stHeader"] {display: none;}
      iframe {width: 100% !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

ROOT = Path(__file__).parent


def to_data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    mime = mime or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def inline_assets(html: str) -> str:
    # Replace local image references with base64 data URIs
    pattern = re.compile(r'(src|href)=["\'](\./)?([^"\']+\.(?:jpg|jpeg|png|gif|svg|webp))["\']', re.IGNORECASE)

    def repl(match: re.Match) -> str:
        attr, _, filename = match.group(1), match.group(2), match.group(3)
        asset = ROOT / filename
        if asset.exists():
            return f'{attr}="{to_data_uri(asset)}"'
        return match.group(0)

    return pattern.sub(repl, html)


html = (ROOT / "index.html").read_text(encoding="utf-8")
html = inline_assets(html)

components.html(html, height=4200, scrolling=True)
