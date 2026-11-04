
import os
from pathlib import Path

import duckdb
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Brazilian E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)

# =====================================================
# 2. LOAD ENVIRONMENT VARIABLES
# =====================================================

PROJECT_DIR = Path(__file__).parent

load_dotenv(PROJECT_DIR / ".env")

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:latest")
OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "https://ollama.com/v1"
)

# =====================================================
# 3. DATABASE CONNECTION
# =====================================================

DB_PATH = PROJECT_DIR / "ecommerce_analytics.duckdb"


@st.cache_resource
def get_connection():
    return duckdb.connect(
        database=str(DB_PATH),
        read_only=True
    )


# =====================================================
# 4. OLLAMA API CONNECTION
# =====================================================

@st.cache_resource
def get_ai_client(api_key, base_url):
    return OpenAI(
        api_key=api_key,
        base_url=base_url
    )


# =====================================================
# 5. APPLICATION HEADER
# =====================================================

st.title("🛒 Brazilian E-Commerce Analytics")

st.markdown(
    """
    Welcome to the Brazilian E-Commerce Analytics application.

    Explore business performance and interact with
    your AI-powered E-Commerce Assistant.
    """
)

st.divider()

# =====================================================
# 6. SIDEBAR NAVIGATION
# =====================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a section",
    [
        "Business Dashboard",
        "AI Business Assistant"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Python | Streamlit | DuckDB | AWS | Ollama"
)

# =====================================================
# 7. BUSINESS DASHBOARD
# =====================================================

if page == "Business Dashboard":

    st.header("📊 Business Overview")

    try:
        con = get_connection()

        total_orders = con.execute("""
            SELECT COUNT(*)
            FROM gold_orders
        """).fetchone()[0]

        total_revenue = con.execute("""
            SELECT ROUND(SUM(total_item_revenue), 2)
            FROM gold_revenue
        """).fetchone()[0]

        total_customers = con.execute("""
            SELECT COUNT(*)
            FROM gold_customers
        """).fetchone()[0]

        total_products = con.execute("""
            SELECT COUNT(*)
            FROM gold_products
        """).fetchone()[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Orders",
            f"{total_orders:,}"
        )

        col2.metric(
            "Total Item Revenue",
            (
                f"R$ {total_revenue:,.2f}"
                if total_revenue is not None
                else "N/A"
            )
        )

        col3.metric(
            "Customer Records",
            f"{total_customers:,}"
        )

        col4.metric(
            "Total Products",
            f"{total_products:,}"
        )

        st.divider()

        st.subheader("⚙️ Project Technology Stack")

        tech1, tech2, tech3, tech4 = st.columns(4)

        tech1.info("**Python**\n\nData Processing")
        tech2.info("**DuckDB**\n\nAnalytical Database")
        tech3.info("**PySpark**\n\nDistributed Processing")
        tech4.info("**AWS**\n\nCloud Analytics")

        st.divider()

        st.subheader("📁 Analytical Datasets")

        dataset1, dataset2, dataset3 = st.columns(3)

        dataset1.success("Gold Orders")
        dataset2.success("Gold Revenue")
        dataset3.success("Gold Customers")

        dataset4, dataset5, dataset6 = st.columns(3)

        dataset4.success("Gold Products")
        dataset5.success("Gold Sellers")
        dataset6.success("Gold Reviews")

        st.success(
            "Successfully connected to DuckDB "
            "and loaded the Gold datasets."
        )

    except Exception as e:

        st.error("Unable to load dashboard data.")
        st.exception(e)

# =====================================================
# 8. AI BUSINESS ASSISTANT
# =====================================================

elif page == "AI Business Assistant":

    st.header("🤖 AI Business Assistant")

    st.markdown(
        """
        Ask questions and interact with your local or
        cloud-hosted Llama model through Ollama.
        """
    )

    if not OLLAMA_API_KEY:
        st.error(
            "OLLAMA_API_KEY is missing. "
            "Please check your project .env file."
        )
        st.stop()

    # Initialize AI client
    try:
        client = get_ai_client(
            OLLAMA_API_KEY,
            OLLAMA_BASE_URL
        )
    except Exception as e:
        st.error("Unable to initialize the AI client.")
        st.exception(e)
        st.stop()

    # Conversation history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.button("🗑️ Clear Conversation"):
        st.session_state.chat_history = []
        st.rerun()

    st.divider()

    # Suggested questions
    st.subheader("💡 Suggested Questions")

    suggestions = [
        "What is an e-commerce data engineering pipeline?",
        "Explain the Silver and Gold data layers.",
        "What is DuckDB?",
        "Explain PySpark in simple words.",
        "What is AWS Glue and Amazon Athena?",
        "How can e-commerce businesses improve customer satisfaction?"
    ]

    selected_question = st.selectbox(
        "Choose a suggested question",
        ["Select a question"] + suggestions
    )

    if st.button("Ask Suggested Question"):

        if selected_question != "Select a question":
            st.session_state.pending_question = selected_question
            st.rerun()

    st.divider()

    # Display conversation history
    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    user_question = st.chat_input(
        "Ask your AI assistant anything..."
    )

    question = user_question

    if (
        not question
        and "pending_question" in st.session_state
    ):
        question = st.session_state.pop("pending_question")

    # Generate AI response
    if question:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        system_prompt = """
        You are an E-Commerce Business and Data Engineering
        Assistant.

        Help users understand:

        1. E-Commerce analytics
        2. Orders and revenue
        3. Customer behavior
        4. Products and sellers
        5. Customer reviews
        6. Python and SQL
        7. DuckDB and PySpark
        8. AWS S3, Glue and Athena
        9. Data engineering concepts

        Provide clear, accurate and beginner-friendly answers.
        Use examples whenever helpful.

        Do not invent business statistics or claim to have
        queried a database that you have not accessed.
        """

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        messages.extend(
            st.session_state.chat_history
        )

        try:

            with st.chat_message("assistant"):

                with st.spinner(
                    f"{OLLAMA_MODEL} is thinking..."
                ):

                    response = client.chat.completions.create(
                        model=OLLAMA_MODEL,
                        messages=messages
                    )

                    ai_answer = (
                        response.choices[0].message.content
                    )

                st.markdown(ai_answer)

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": ai_answer
                }
            )

        except Exception as e:

            st.error(
                "Unable to generate an AI response. "
                "Check your API key, model name, endpoint "
                "and provider access."
            )

            st.code(str(e))

# =====================================================
# 9. APPLICATION FOOTER
# =====================================================

st.divider()

st.caption(
    "Brazilian E-Commerce Analytics | "
    "Python | Streamlit | DuckDB | Ollama"
)
