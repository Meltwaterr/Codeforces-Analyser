# ui_components.py

import streamlit as st
from config import (LANGUAGE_OPTIONS, DEFAULT_SLEEP, DEFAULT_SINGLE_SOLUTION_PROMPT, 
                    DEFAULT_COMPARISON_PROMPT, DEFAULT_ALL_TOGETHER_PROMPT, 
                    LANGUAGE_SYNTAX, ANALYSIS_MODES)
from gemini_integration import display_chat_interface, initialize_chat

def apply_styling():
    st.markdown("""
        <style>
            @keyframes wave {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            @keyframes sidebar-glow {
                0% { border-right-color: rgba(255, 0, 230, 0.3); }
                50% { border-right-color: rgba(255, 0, 230, 0.8); }
                100% { border-right-color: rgba(255, 0, 230, 0.3); }
            }
            .stApp {
                background: linear-gradient(135deg, #000000, #0b0014, #14001f, #000000);
                background-size: 400% 400%;
                animation: wave 20s ease infinite;
                color: #e0e1dd;
            }
            [data-testid="stSidebar"] { 
                background-color: rgba(0, 0, 0, 0.85); 
                backdrop-filter: blur(8px); 
                border-right: 2px solid;
                animation: sidebar-glow 4s ease-in-out infinite;
            }
            .stButton > button { 
                border-radius: 25px; 
                border: 2px solid #ff00e6; 
                background: transparent;
                color: #ff00e6; 
                font-weight: bold; 
                transition: all 0.4s ease; 
                position: relative;
                overflow: hidden;
            }
            .stButton > button:hover {
                background: #ff00e6;
                color: #000000;
                box-shadow: 0 0 25px rgba(255, 0, 230, 0.7);
                transform: scale(1.05);
            }
            h1, h2, h3, h4, h5 { 
                color: #ff00e6; 
                font-weight: 600;
                text-shadow: 0 0 8px rgba(255, 0, 230, 0.5);
            }
            .display-panel {
                padding: 30px;
                border-radius: 15px;
                background: rgba(5, 0, 10, 0.75);
                border: 1px solid rgba(255, 0, 230, 0.4);
                backdrop-filter: blur(5px);
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            }
            div[role="radiogroup"] > label {
                display: block;
                padding: 12px;
                margin-bottom: 10px;
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.1);
                cursor: pointer;
                transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s;
            }
            div[role="radiogroup"] > label:hover {
                background-color: rgba(255, 0, 230, 0.15);
                transform: scale(1.02);
                box-shadow: 0 0 15px rgba(255, 0, 230, 0.4);
            }
            [data-testid="stCodeBlock"] pre {
                max-height: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🌌 Codeforces AI Analyst")
        st.markdown("---")
        
        st.markdown("##### 🎯 Core Target")
        contest_id = st.text_input("🆔 Contest ID", placeholder="e.g. 1922")
        problem_index = st.text_input("📝 Problem Index", placeholder="e.g. A")
        language_name = st.selectbox("📜 Language", LANGUAGE_OPTIONS)
        
        st.markdown("---")
        st.markdown("##### ⚙️ Fetch & Analyze")
        analysis_mode = st.radio("✨ Analysis Mode", ANALYSIS_MODES, index=0, horizontal=True)
        n = st.number_input("🔍 Solutions to fetch", 1, 10, 3)
        sleep_time = st.slider("⏳ Browser wait time (s)", 2, 15, DEFAULT_SLEEP)
        max_chars = st.slider("✂️ Max chars for analysis", 500, 8000, 4000)

        st.markdown("---")
        with st.expander("🧠 AI Prompts (Advanced)", expanded=False):
            single_prompt = st.text_area("Single Solution Analysis Prompt", height=200, value=DEFAULT_SINGLE_SOLUTION_PROMPT)
            comp_prompt = st.text_area("Comparative Analysis Prompt", height=200, value=DEFAULT_COMPARISON_PROMPT)
            all_together_prompt = st.text_area("All Together Analysis Prompt", height=200, value=DEFAULT_ALL_TOGETHER_PROMPT)
        
        return analysis_mode, contest_id, problem_index, language_name, n, sleep_time, max_chars, single_prompt, comp_prompt, all_together_prompt

def render_results_area(res, language_name, max_chars):
    if res.get("mode") == "One by One":
        render_one_by_one_dashboard(res, language_name, max_chars)
    elif res.get("mode") == "All Together":
        render_all_together_results(res)

def render_one_by_one_dashboard(res, language_name, max_chars):
    left_panel, right_panel = st.columns([1, 5])

    with left_panel:
        st.subheader("Solutions")
        solution_options = {sol['id']: f"Solution #{i+1}" for i, sol in enumerate(res['solutions'])}
        
        active_id = st.radio(
            "Select a solution:",
            options=list(solution_options.keys()),
            format_func=lambda x: solution_options[x],
            label_visibility="collapsed",
            key="active_solution_id"
        )

    with right_panel:
        active_sol = next((s for s in res['solutions'] if s['id'] == active_id), None)
        if active_sol:
            with st.container():
                st.markdown('<div class="display-panel">', unsafe_allow_html=True)
                st.header(f"Analysis for Solution ID: {active_sol['id']}")
                
                tab1, tab2, tab3 = st.tabs(["🤖 Analysis", "📄 Code", "💬 Chat"])
                with tab1:
                    st.markdown(active_sol['analysis'])
                with tab2:
                    st.code(active_sol['code'], language=LANGUAGE_SYNTAX.get(language_name, "text"))
                with tab3:
                    st.info("Converse with the AI about this specific solution.")
                    chat_context = f"Problem Statement:\n{res['problem_statement']}\n\nSolution Code (ID: {active_sol['id']}):\n```\n{active_sol['code']}\n```\n\nAI Analysis:\n{active_sol['analysis']}"
                    if f"chat_session_{active_sol['id']}" not in st.session_state:
                        st.session_state[f"chat_session_{active_sol['id']}"] = initialize_chat(chat_context)
                    display_chat_interface(chat_key=active_sol['id'])
                st.markdown('</div>', unsafe_allow_html=True)

    if 'comparison' in res:
        with st.container(border=True):
            st.subheader("🏆 Final Verdict")
            with st.expander("View Comparative Analysis"):
                st.markdown(res['comparison'])

def render_all_together_results(res):
    with st.container(border=True):
        st.subheader("📚 Combined Analysis Report")
        for i, sol in enumerate(res['solutions']):
            with st.expander(f"View Code for Solution #{i+1} (ID: {sol['id']})"):
                st.code(sol['code'], language=LANGUAGE_SYNTAX.get(res.get("language"), "text"))
        
        st.markdown("---")
        st.markdown(res.get('combined_analysis', "No analysis was generated."))