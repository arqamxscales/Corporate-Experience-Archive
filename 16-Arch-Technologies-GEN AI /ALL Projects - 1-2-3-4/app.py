import requests
import streamlit as st

OLLAMA_BASE_URL = "http://localhost:11434"


def get_installed_models() -> list[str]:
    """Fetch locally available Ollama models."""
    try:
        resp = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        models = [m.get("name", "") for m in data.get("models", []) if m.get("name")]
        return models
    except requests.RequestException:
        return []


def query_ollama(model: str, prompt: str, temperature: float, max_tokens: int) -> str:
    """Send user prompt to Ollama and return the generated response."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }

    try:
        resp = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "(No response received from model)")
    except requests.RequestException as exc:
        return f"Error communicating with Ollama: {exc}"


def reset_chat() -> None:
    st.session_state.history = []
    st.session_state.user_input = ""


st.set_page_config(page_title="Local LLM Chat (Ollama)", page_icon="💬", layout="wide")
st.title("💬 Local LLM Chat Interface")
st.caption("Streamlit + Ollama (local LLM)")

if "history" not in st.session_state:
    st.session_state.history = []

models = get_installed_models()

with st.sidebar:
    st.header("⚙️ Settings")

    if models:
        selected_model = st.selectbox("Choose a local model", models)
    else:
        selected_model = st.text_input("Model name", value="llama3.2")
        st.warning("No models were detected from Ollama. Enter a model name manually.")

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Higher values make output more random, lower values more focused.",
    )

    max_tokens = st.slider(
        "Max tokens",
        min_value=32,
        max_value=2048,
        value=512,
        step=32,
        help="Maximum number of tokens the model may generate.",
    )

    st.button("🗑️ Reset Conversation", on_click=reset_chat, use_container_width=True)

    st.divider()
    st.subheader("🕘 Conversation History")
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history, start=1):
            model_name = item.get("model", "-")
            st.markdown(f"**{i}. [{model_name}] You:** {item['user']}")
            st.markdown(f"**{i}. Model:** {item['assistant']}")
            st.markdown("---")
    else:
        st.info("No conversation yet.")

st.subheader("Ask your question")

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Enter your prompt", placeholder="Type your query here...", height=120)
    submitted = st.form_submit_button("Send")

if submitted:
    prompt = user_input.strip()
    if not prompt:
        st.warning("Please enter a prompt before sending.")
    else:
        # Build multi-turn conversation context for the selected model only
        context_history = [h for h in st.session_state.history if h.get("model") == selected_model]

        conversation_prompt_lines: list[str] = []
        for item in context_history:
            conversation_prompt_lines.append(f"User: {item['user']}")
            conversation_prompt_lines.append(f"Assistant: {item['assistant']}")
        conversation_prompt_lines.append(f"User: {prompt}")
        conversation_prompt_lines.append("Assistant:")
        conversation_prompt = "\n".join(conversation_prompt_lines)

        with st.spinner("Generating response..."):
            answer = query_ollama(selected_model, conversation_prompt, temperature, max_tokens)

        st.session_state.history.append({"user": prompt, "assistant": answer, "model": selected_model})

st.subheader("Model Response")
if st.session_state.history:
    latest = st.session_state.history[-1]
    st.markdown("**Your Prompt:**")
    st.write(latest["user"])
    st.markdown("**LLM Answer:**")
    st.write(latest["assistant"])
else:
    st.info("Responses will appear here.")
