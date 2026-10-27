import os
import streamlit as st

st.set_page_config(page_title="TradingAgents Dashboard", layout="wide")
st.title("📈 TradingAgents Dashboard")

st.sidebar.header("Configuration")
ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL")
date = st.sidebar.text_input("Analysis Date", value="2026-10-27")

provider = st.sidebar.selectbox("LLM Provider", ["OpenAI", "Anthropic", "Google"])
api_key = st.sidebar.text_input("API Key", type="password")

selected_analysts = st.sidebar.multiselect(
    "Analyst Team",
    ["market", "social", "news", "fundamentals"],
    default=["market", "fundamentals"]
)

if st.sidebar.button("Run Analysis"):
    if not api_key:
        st.error("Please provide your API key.")
    else:
        # Import inside the block after environment setup
        from tradingagents.graph import create_trading_graph

        env_var = {
            "OpenAI": "OPENAI_API_KEY",
            "Anthropic": "ANTHROPIC_API_KEY",
            "Google": "GEMINI_API_KEY"
        }[provider]
        os.environ[env_var] = api_key

        st.info(f"Running analysis for {ticker}...")
        
        init_state = {
            "ticker": ticker,
            "current_date": date,
            "analysts": selected_analysts,
            "messages": []
        }

        with st.spinner("Agents are analyzing..."):
            try:
                graph = create_trading_graph()
                results = graph.invoke(init_state)
                st.success("Analysis Complete!")
                st.subheader("Agent Output & Reports")
                for msg in results.get("messages", []):
                    st.write(getattr(msg, "content", str(msg)))
            except Exception as e:
                st.error(f"Error: {e}")
