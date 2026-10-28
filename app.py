"""Run with: python -m streamlit run app.py"""

import os

import streamlit as st

from ai import AIUnavailable, interview
from game import BRIEF, EVIDENCE, EXPLANATION, SUSPECTS, TITLE, accuse

st.set_page_config(page_title="Moonstone Detective", page_icon="🔎")
st.title(f"🔎 {TITLE}")
st.write(BRIEF)
mode = st.sidebar.radio("Dialogue mode", ["Demo (scripted)", "Live AI"])
live = mode == "Live AI"
if st.session_state.get("mode") != mode:
    st.session_state.mode = mode
    st.session_state.history = {name: [] for name in SUSPECTS}
    st.session_state.outcome = None
if st.sidebar.button("Restart investigation"):
    st.session_state.history = {name: [] for name in SUSPECTS}
    st.session_state.outcome = None
    st.rerun()
st.sidebar.caption("Changing dialogue mode starts a new investigation.")
if live:
    st.info("Suspect dialogue is AI-generated. Case facts and the verdict are fixed.")
    if not os.getenv("DETECTIVE_API_KEY", "").strip():
        st.warning("Live AI needs DETECTIVE_API_KEY in the server environment.")
else:
    st.warning("Demo mode uses predefined responses. It does not satisfy the assessment's runtime AI requirement.")
with st.expander("Examine the case evidence", expanded=True):
    for clue in EVIDENCE:
        st.write(f"• {clue}")
finished = st.session_state.outcome is not None
suspect = st.selectbox("Interview a suspect", list(SUSPECTS), disabled=finished)
st.caption(SUSPECTS[suspect]["role"])
for message in st.session_state.history[suspect]:
    with st.chat_message(message["role"]):
        st.write(message["content"])
with st.form("interview"):
    question = st.text_input("Your question", max_chars=500, disabled=finished)
    submitted = st.form_submit_button("Ask suspect", disabled=finished)
if submitted:
    try:
        with st.spinner("Waiting for the suspect…"):
            reply = interview(suspect, question, st.session_state.history[suspect], live)
        st.session_state.history[suspect].extend([
            {"role": "user", "content": question.strip()},
            {"role": "assistant", "content": reply},
        ])
        st.rerun()
    except (ValueError, AIUnavailable) as exc:
        st.error(str(exc))
st.subheader("Close the case")
with st.form("accusation"):
    choice = st.selectbox("Who stole the Moonstone?", list(SUSPECTS), disabled=finished)
    confirmed = st.checkbox("I'm ready to make my final accusation", disabled=finished)
    accuse_now = st.form_submit_button("Make accusation", disabled=finished)
if accuse_now:
    if not confirmed:
        st.error("Confirm your final accusation first.")
    else:
        st.session_state.outcome = {"suspect": choice, "correct": accuse(choice)}
        st.rerun()
if st.session_state.outcome is not None:
    outcome = st.session_state.outcome
    if outcome["correct"]:
        st.success(f"Case solved! You correctly accused {outcome['suspect']}.")
    else:
        st.error(f"You accused {outcome['suspect']}, but the evidence points to Alex.")
    st.write(EXPLANATION)
    st.caption("Use Restart investigation in the sidebar to play again.")
