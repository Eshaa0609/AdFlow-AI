import streamlit as st
import plotly.graph_objects as go
from agent import adflow_agent
from data_provider import get_raw_bot_rate

st.set_page_config(page_title="AdFlow AI", page_icon="✨", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main Background */
    [data-testid="stAppViewContainer"] {
        background-color: #1E293B !important; 
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #334155 !important;
    }

    /* Chat Bubbles */
    [data-testid="stChatMessage"] {
        background-color: #475569 !important;
        border-radius: 12px !important;
        border: none !important;
    }
    
    /* Text Color */
    .stApp, .stMarkdown, p, div {
        color: #F1F5F9 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (The Visual Watchdog) ---
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d473530c273ad9000a4.svg", width=40)
    st.markdown("### Mumbai Real-time Health")
    
    try:
        mumbai_rate = get_raw_bot_rate("Mumbai")
        
        # GUARD: Only plot if we have actual data
        if mumbai_rate is None:
            st.info("⏳ Waiting for traffic data...")
        else:
            # Create the Gauge Chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = mumbai_rate,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Bot Traffic (%)", 'font': {'size': 16, 'color': "#e3e3e3"}},
                gauge = {
                    'axis': {'range': [0, 50], 'tickwidth': 1, 'tickcolor': "#888"},
                    'bar': {'color': "#f28b82" if mumbai_rate > 20 else "#8ab4f8"},
                    'bgcolor': "#2a2b2d",
                    'borderwidth': 0,
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 20
                    }
                }
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=20, r=20, t=50, b=0))
            st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
            
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

    # Status Cards
    st.markdown('<div class="status-card">🟢 System: Optimal</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-card" style="border-left-color: #f28b82;">⚠️ Alert: Mumbai Bot Traffic</div>', unsafe_allow_html=True)
    
    if st.button("New Consultation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CHAT ---
st.title("✨ AdFlow Intelligence")
st.caption("Strategic Campaign Guardian | Powered by Agentic AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask AdFlow about campaign health..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = adflow_agent(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})