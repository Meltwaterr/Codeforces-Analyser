# main_app.py

import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit.components.v1 as components

from config import LANGUAGE_OPTIONS
from ui_components import apply_styling, render_sidebar, render_results_area
from scraping_logic import fetch_problem_statement, extract_submission_ids, get_code_from_submission
from gemini_integration import get_gemini_response

def main():
    st.set_page_config(page_title="Codeforces AI Analyst", layout="wide", initial_sidebar_state="expanded")
    load_dotenv()
    apply_styling()

    if 'analysis_complete' not in st.session_state: st.session_state.analysis_complete = False
    if 'results' not in st.session_state: st.session_state.results = {}
    if 'error_message' not in st.session_state: st.session_state.error_message = None
    if 'run_collapse_script' not in st.session_state: st.session_state.run_collapse_script = False

    configs = render_sidebar()
    analysis_mode, contest_id, problem_index, language_name, n, sleep_time, max_chars, single_prompt, comp_prompt, all_together_prompt = configs

    if st.sidebar.button("Analyze Solutions", use_container_width=True):
        st.session_state.analysis_complete = False
        st.session_state.results = {}
        st.session_state.error_message = None
        st.session_state.run_collapse_script = False
        gemini_api_key = os.getenv("GEMINI_API_KEY")

        if not all([contest_id, problem_index]):
            st.session_state.error_message = "Please provide a Contest ID and Problem Index."
        elif not gemini_api_key:
            st.session_state.error_message = "GEMINI_API_KEY not found in .env file."
        else:
            try:
                genai.configure(api_key=gemini_api_key)
                with st.spinner("Phase 1/3: Fetching Problem & Submissions..."):
                    ps = fetch_problem_statement(contest_id, problem_index, sleep_time)
                    if not ps:
                        st.session_state.error_message = "Could not fetch Problem Statement. Please check inputs or increase wait time."; st.rerun()
                    
                    sub_ids = extract_submission_ids(contest_id, problem_index, LANGUAGE_OPTIONS.index(language_name), sleep_time)
                    if not sub_ids:
                        st.session_state.error_message = "No submissions found for the selected criteria."; st.rerun()

                all_solutions_code = []
                with st.spinner(f"Phase 2/3: Fetching code for {len(sub_ids[:n])} solutions..."):
                    for i, sub_id in enumerate(sub_ids[:n]):
                        code = get_code_from_submission(contest_id, sub_id, sleep_time)
                        if code:
                            all_solutions_code.append({'id': sub_id, 'code': code})
                
                if not all_solutions_code:
                    st.session_state.error_message = "Successfully found submission IDs, but failed to scrape the code for any of them. This might be due to a Codeforces UI update or network issues."; st.rerun()

                st.session_state.results = {'problem_statement': ps, 'solutions': all_solutions_code, 'mode': analysis_mode, 'language': language_name}

                with st.spinner("Phase 3/3: Calling Gemini for Analysis..."):
                    if analysis_mode == "One by One":
                        for sol in st.session_state.results['solutions']:
                            prompt = single_prompt.format(problem_statement=ps, language=language_name, code=sol['code'][:max_chars])
                            sol['analysis'] = get_gemini_response(prompt)
                        if len(st.session_state.results['solutions']) > 1:
                            solutions_text = "\n".join([f"--- Solution #{i+1} (ID: {s['id']})\n```{s['code'][:max_chars]}```" for i, s in enumerate(st.session_state.results['solutions'])])
                            prompt = comp_prompt.format(problem_statement=ps, solutions=solutions_text)
                            st.session_state.results['comparison'] = get_gemini_response(prompt)
                    elif analysis_mode == "All Together":
                        solutions_text = "\n".join([f"--- Solution #{i+1} (ID: {s['id']})\n```{s['code'][:max_chars]}```" for i, s in enumerate(st.session_state.results['solutions'])])
                        prompt = all_together_prompt.format(problem_statement=ps, solutions=solutions_text)
                        st.session_state.results['combined_analysis'] = get_gemini_response(prompt)
                
                st.session_state.analysis_complete = True
                st.session_state.run_collapse_script = True
            except Exception as e:
                st.session_state.error_message = f"An unexpected error occurred: {e}"
                st.session_state.analysis_complete = False
                st.session_state.run_collapse_script = False
        st.rerun()

    st.markdown("<h1 style='text-align: center;'>Codeforces AI Analyst</h1>", unsafe_allow_html=True)
    
    if st.session_state.analysis_complete:
        render_results_area(st.session_state.results, language_name, max_chars)
    elif st.session_state.error_message:
        st.sidebar.error(st.session_state.error_message)
    else:
        st.sidebar.info("Please configure the analysis parameters and click 'Analyze Solutions'.")

    if st.session_state.run_collapse_script:
        js = """
        <script>
            setTimeout(function() {
                const collapseButton = window.parent.document.querySelector('[data-testid="stSidebarNavCollapseButton"]');
                if (collapseButton) {
                    collapseButton.click();
                }
            }, 50);
        </script>
        """
        components.html(js, height=0, width=0)
        st.session_state.run_collapse_script = False

if __name__ == "__main__":
    main()