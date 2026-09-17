# 🤖 Custom AI Chatbot with Memory

A stateful, interactive AI chatbot built during my **Generative AI Internship at DecodeLabs**. The application uses **Streamlit** for the interface and **Google Gemini** for response generation, while a custom memory manager maintains conversational context across multiple turns.

## ✨ Features

- **Multi-turn conversation memory** — preserves recent user/assistant interactions.
- **FIFO sliding-window memory** — keeps the latest configurable number of turns and removes older entries when the limit is exceeded.
- **Input validation** — blocks empty or whitespace-only messages and limits input length to 2,000 characters.
- **Gemini LLM integration** — generates contextual responses through Google's Generative AI SDK.
- **Streamlit chat UI** — simple, interactive browser-based interface.
- **Session state** — keeps the chatbot's memory and displayed messages during the active session.
- **Reset Memory** — clears the current conversation with one click.
- **Memory inspection** — sidebar option to view the internal conversation array.
- **Modular architecture** — separates LLM communication, memory management, and UI/session handling.
- **Response timing** — displays generation latency and current turn information.
- **Error handling** — handles missing API configuration, missing dependencies, and model/API errors.

## 🧠 How It Works

```text
User Input
    │
    ▼
Input Validation
    │
    ▼
Memory Manager
    │
    ├── Append user message
    ├── Enforce FIFO window
    │
    ▼
Gemini LLM
    │
    ▼
Generated Response
    │
    ▼
Append model response to memory
    │
    ▼
Streamlit Chat Interface
```

The chatbot stores messages in a structured history such as:

```python
[
    {"role": "user", "parts": ["Hello"]},
    {"role": "model", "parts": ["Hi! How can I help you?"]},
]
```

The default configuration keeps the most recent **10 conversation turns** (20 message entries: user + model). This provides contextual continuity while preventing unbounded history growth.

## 🛠️ Technology Stack

- **Python**
- **Streamlit**
- **Google Gemini API**
- **google-generativeai**
- **python-dotenv**

## 📁 Project Structure

```text
Decode-labs-project1-chatbot/
├── chatbot.py          # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # Local API configuration (do not commit)
└── README.md           # Project documentation
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Tauhid-Topu-007/Decode-labs-project1-chatbot.git
cd Decode-labs-project1-chatbot
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The project currently requires Streamlit, python-dotenv, and Google's Generative AI Python package.

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Never commit your real API key to GitHub.** Add `.env` to `.gitignore` if it is not already ignored.

### 5. Run the application

```bash
streamlit run chatbot.py
```

Then open the local Streamlit URL shown in the terminal.

## ⚙️ Configuration

The main configuration values are defined near the top of `chatbot.py`:

```python
MODEL_NAME = "gemini-3.6-flash"
MAX_HISTORY_TURNS = 10
MAX_INPUT_CHARS = 2000
```

You can adjust the history window and input limit according to your application requirements. The model name should correspond to a model available to your Gemini API account.

## 🔐 Security Notes

- Store API credentials in environment variables or a `.env` file.
- Do not hard-code secrets in source code.
- Do not commit `.env` or other credential files.
- For production deployments, use the hosting platform's secret/environment-variable management instead of exposing credentials.

## 📚 Learning Outcomes

This project provided hands-on experience with:

- Stateful conversational AI
- LLM API integration
- Conversation history management
- FIFO sliding-window memory
- Streamlit session state
- Input validation
- Error handling
- Modular software architecture
- Separation of concerns
- Context-aware prompt/response workflows

## 🎯 Project Goal

The goal of this project was to understand how a stateless LLM API can be wrapped with application-level memory and session management to create a more natural, contextual, and interactive conversational experience.

## 🙏 Acknowledgement

This project was developed as part of my **Generative AI Internship at DecodeLabs**. Special thanks to **DecodeLabs** for providing the opportunity to learn and build practical Generative AI applications through hands-on projects.

## 👨‍💻 Author

**Tauhidul Islam Topu**  
CSE, Hajee Mohammad Danesh Science & Technology University (HSTU)

- GitHub: https://github.com/Tauhid-Topu-007
- LinkedIn: https://www.linkedin.com/in/tauhidul-islam-topu-1a04b31ab/

## 📄 License

This project is intended for educational and portfolio purposes.
