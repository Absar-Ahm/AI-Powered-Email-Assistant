📧 AI-Powered Email Assistant
An intelligent Streamlit-based application that helps you generate professional emails using AI — via text or voice input. Built using Python, NLP tools, and speech interfaces, this assistant can compose new emails, reply to existing ones, or guide users through voice-driven Q&A.

🚀 Features
✍️ Compose Mode: Generate new emails by specifying tone, recipient, topic, and purpose.

🔁 Reply Mode: Generate a smart reply to an existing email with auto tone detection and reply purpose.

🎙️ Voice Assistant Mode: Speak your answers — the assistant will ask questions aloud and transcribe your spoken responses.

🧠 Tone Detection: Uses TextBlob to auto-suggest tone from received messages.

🔊 Assistant-voiced questions: Integrated offline TTS (pyttsx3) for a human-like assistant experience.

📦 Installation
'''1️⃣ Clone the repository
'''git clone https://github.com/Absar-Ahm/AI-Powered-Email-Assistant.git
'''cd AI-Powered-Email-Assistant
'''2️⃣ Set up virtual environment
python -m venv venv
venv\Scripts\activate          # For Windows
'''OR
source venv/bin/activate       # For Mac/Linux
3️⃣ Install dependencies
pip install -r requirements.txt
python -m textblob.download_corpora
4️⃣ Set up your .env file
Create a .env file inside the root directory and add:
TOGETHER_API_KEY=your_api_key_here
▶️ Running the App
streamlit run app.py
Open your browser at: http://localhost:8501

⚙️ Tech Stack
Python
Streamlit
SpeechRecognition (Voice Input)
pyttsx3 (Text-to-Speech)
TextBlob (Tone Detection)
Together API (LLM integration)
dotenv (Environment Config)

💼 Why This Project?
Combines NLP, LLMs, voice recognition, and real-world UI design

Demonstrates multi-modal AI capabilities

Fully production-ready architecture for portfolio demonstration

