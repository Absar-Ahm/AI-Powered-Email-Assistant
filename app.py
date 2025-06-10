import streamlit as st
import speech_recognition as sr
import pyttsx3
import time
from textblob import TextBlob
from prompts import build_prompt
from email_generator import generate_email

# === Text-to-Speech ===
def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Use voices[0] for male voice
    engine.say(text)
    engine.runAndWait()

# === Speech-to-Text with UI-first flow ===
def capture_voice_input(prompt_text):
    st.info(prompt_text)               # 1. Show visually
    time.sleep(0.5)                    # 2. Wait for UI to update
    speak_text(prompt_text)           # 3. Then speak it
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.warning("🎤 Listening... Please speak.")
        audio = recognizer.listen(source, phrase_time_limit=7)
        st.success("Processing...")
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand your voice.")
            return ""
        except sr.RequestError as e:
            st.error(f"Speech recognition error: {e}")
            return ""

# === Auto-tone Detection ===
def suggest_tone(email_text):
    polarity = TextBlob(email_text).sentiment.polarity
    if polarity > 0.3:
        return "Friendly"
    elif polarity < -0.3:
        return "Apologetic"
    else:
        return "Formal"

# === UI Setup ===
st.set_page_config(page_title="Smart Email Writer", layout="centered")
st.title("📧 AI-Powered Email Assistant")

mode = st.radio("Choose Mode:", ["Compose New Email", "Generate Reply", "🎙️ Voice Assistant"])

# === Mode 1: Compose ===
if mode == "Compose New Email":
    with st.form("compose_form"):
        topic = st.text_area("Brief (What is this about?)", height=100)
        recipient = st.selectbox("Recipient Type", ["Client", "Manager", "HR", "Colleague", "Other"])
        purpose = st.text_input("Purpose (e.g., follow-up, apology, proposal)")
        tone = st.selectbox("Tone", ["Formal", "Friendly", "Persuasive", "Apologetic"])
        submitted = st.form_submit_button("Generate Email")

    if submitted:
        if not topic.strip() or not purpose.strip():
            st.warning("Please fill in both the topic and purpose.")
        else:
            prompt = build_prompt(tone=tone, recipient=recipient, purpose=purpose, topic=topic, mode="new")
            with st.spinner("Writing your email..."):
                email = generate_email(prompt)
                st.success("Here's your email:")
                st.markdown(f"---\n\n{email}\n\n---")
                st.code(email, language="markdown")
                st.download_button("📥 Download Email", data=email, file_name="generated_email.txt")

# === Mode 2: Generate Reply ===
elif mode == "Generate Reply":
    with st.form("reply_form"):
        original_email = st.text_area("Paste the email you received", height=250)
        recipient = st.selectbox("Replying to", ["Client", "Manager", "HR", "Colleague", "Other"])
        purpose = st.text_input("Purpose of your reply (e.g., apology, clarification, proposal)")
        auto_detect = st.checkbox("Auto-detect tone from received email", value=True)

        if auto_detect and original_email.strip():
            detected_tone = suggest_tone(original_email)
            st.info(f"Detected Tone: {detected_tone}")
            tone = st.selectbox("Tone of your reply", ["Formal", "Friendly", "Apologetic", "Assertive"],
                                index=["Formal", "Friendly", "Apologetic", "Assertive"].index(detected_tone))
        else:
            tone = st.selectbox("Tone of your reply", ["Formal", "Friendly", "Apologetic", "Assertive"])
        submitted = st.form_submit_button("Generate Reply")

    if submitted:
        if not original_email.strip() or not purpose.strip():
            st.warning("Please paste the original email and provide the purpose of your reply.")
        else:
            prompt = build_prompt(
                tone=tone,
                recipient=recipient,
                original_email=original_email,
                purpose=purpose,
                mode="reply"
            )
            with st.spinner("Writing your reply..."):
                email = generate_email(prompt)
                st.success("Here's your reply:")
                st.markdown(f"---\n\n{email}\n\n---")
                st.code(email, language="markdown")
                st.download_button("📥 Download Email", data=email, file_name="generated_reply.txt")

# === Mode 3: Voice Assistant (with spoken questions) ===
elif mode == "🎙️ Voice Assistant":
    st.markdown("### 🎤 Speak Your Answers Below")

    if st.button("🎙️ Start Voice Q&A"):
        topic = capture_voice_input("What is the topic of your email?")
        recipient = capture_voice_input("Who are you sending this to?")
        purpose = capture_voice_input("What is the purpose of the email?")
        tone = capture_voice_input("What tone should the email have?")

        st.session_state["topic"] = topic
        st.session_state["recipient"] = recipient
        st.session_state["purpose"] = purpose
        st.session_state["tone"] = tone

        if all([topic, recipient, purpose, tone]):
            prompt = build_prompt(
                tone=tone.capitalize(),
                recipient=recipient.capitalize(),
                purpose=purpose,
                topic=topic,
                mode="new"
            )
            with st.spinner("Writing your email..."):
                email = generate_email(prompt)
                st.success("Here's your email:")
                st.markdown(f"---\n\n{email}\n\n---")
                st.code(email, language="markdown")
                st.download_button("📥 Download Email", data=email, file_name="generated_voice_email.txt")
        else:
            st.warning("Some inputs were empty or unclear. Please try again.")
