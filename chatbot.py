import os
import time
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "gemini-3.6-flash"
MAX_HISTORY_TURNS = 10
MAX_INPUT_CHARS = 2000
SYSTEM_PROMPT = (
    "You are a helpful, friendly AI assistant with memory of this conversation. "
    "Always remember what the user told you earlier and refer back to it naturally."
)


class LLMClient:
    def __init__(self, api_key: str, model_name: str = MODEL_NAME):
        try:
            import google.generativeai as genai
        except ImportError:
            st.error("google-generativeai is not installed. Run: pip install google-generativeai")
            st.stop()

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=SYSTEM_PROMPT,
        )
        self.genai = genai

    def generate(self, history: list) -> str:
        try:
            response = self.model.generate_content(history)
            if hasattr(response, "text") and response.text:
                return response.text.strip()
            if response.candidates and response.candidates[0].content.parts:
                return "".join(p.text for p in response.candidates[0].content.parts).strip()
            return "[Empty response from model]"
        except Exception as e:
            return f"[API Error] {type(e).__name__}: {e}"


class MemoryManager:
    def __init__(self, max_turns: int = MAX_HISTORY_TURNS):
        self.max_turns = max_turns
        self.history: list = []

    @staticmethod
    def validate(user_input: str):
        if user_input is None:
            return False, ""
        cleaned = user_input.strip()
        if not cleaned:
            return False, ""
        if len(cleaned) > MAX_INPUT_CHARS:
            cleaned = cleaned[:MAX_INPUT_CHARS]
        return True, cleaned

    def append_user(self, text: str) -> None:
        self.history.append({"role": "user", "parts": [text]})

    def append_model(self, text: str) -> None:
        self.history.append({"role": "model", "parts": [text]})

    def enforce_window(self) -> None:
        cap = self.max_turns * 2
        if len(self.history) > cap:
            overflow = len(self.history) - cap
            self.history = self.history[overflow:]

    def turn_count(self) -> int:
        return len(self.history) // 2

    def size(self) -> int:
        return len(self.history)


def init_session():
    if "memory" not in st.session_state:
        st.session_state.memory = MemoryManager(max_turns=MAX_HISTORY_TURNS)
    if "client" not in st.session_state:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("GEMINI_API_KEY not found. Set it in your .env file.")
            st.stop()
        st.session_state.client = LLMClient(api_key=api_key)
    if "messages" not in st.session_state:
        st.session_state.messages = []


def render_sidebar():
    with st.sidebar:
        st.header("Controls")
        st.caption(f"Model: {MODEL_NAME}")
        st.caption(f"Window: {MAX_HISTORY_TURNS} turns")
        st.caption(f"Turns used: {st.session_state.memory.turn_count()}")
        st.caption(f"Entries: {st.session_state.memory.size()}")

        if st.button("Reset Memory"):
            st.session_state.memory.history.clear()
            st.session_state.messages.clear()
            st.rerun()

        with st.expander("Show memory array"):
            if not st.session_state.memory.history:
                st.write("Memory is empty.")
            else:
                for i, item in enumerate(st.session_state.memory.history):
                    role = item["role"]
                    text = item["parts"][0]
                    preview = text if len(text) < 120 else text[:117] + "..."
                    st.markdown(f"**[{i}] {role}** → {preview}")


def main():
    st.set_page_config(page_title="Custom AI Chatbot with Memory", page_icon="🤖")
    st.title("🤖 Custom AI Chatbot with Memory")
    st.caption("DecodeLabs · Generative AI Project 1 · Batch 2026")

    init_session()
    render_sidebar()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    raw = st.chat_input("Type your message...")

    if raw is not None:
        is_valid, cleaned = MemoryManager.validate(raw)
        if not is_valid:
            st.warning("Empty or whitespace-only input blocked.")
            return

        memory = st.session_state.memory
        client = st.session_state.client

        memory.append_user(cleaned)
        st.session_state.messages.append({"role": "user", "content": cleaned})
        with st.chat_message("user"):
            st.markdown(cleaned)

        memory.enforce_window()

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("_thinking..._")
            t0 = time.time()
            response_text = client.generate(memory.history)
            elapsed = time.time() - t0

            if response_text.startswith("[API Error]"):
                placeholder.error(response_text)
                memory.history.pop()
                st.session_state.messages.pop()
                return

            placeholder.markdown(response_text)
            st.caption(f"{elapsed:.2f}s · turn {memory.turn_count()}")

        memory.append_model(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})


if __name__ == "__main__":
    main()