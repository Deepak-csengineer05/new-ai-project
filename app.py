import streamlit as st
import networkx as nx
from core.llm_client import LLMClient
from core.graph_manager import SkillGraph
from core.agents import Cartographer, Assessor
from ui.components import render_graph, render_quiz, render_skill_details

# Page Config
st.set_page_config(
    page_title="SkillGenome",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
with open('ui/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Session State Initialization
if 'graph' not in st.session_state:
    st.session_state.graph = SkillGraph()
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = None
if 'quiz_skill' not in st.session_state:
    st.session_state.quiz_skill = None

# Sidebar
with st.sidebar:
    st.title("🧬 SkillGenome")
    st.markdown("### The AI Competency Graph")
    
    api_key_input = st.text_input("Enter Gemini API Key", type="password")
    if api_key_input:
        st.session_state.api_key = api_key_input
    
    st.markdown("---")
    
    target_role = st.text_input("Target Role", placeholder="e.g. Full Stack Developer")
    generate_btn = st.button("Generate Graph")
    
    st.markdown("---")
    st.markdown("### Legend")
    st.markdown("🟢 Completed")
    st.markdown("🔵 Current Focus")
    st.markdown("🔴 Blocked")
    st.markdown("⚫ Pending")

# Main Logic
if not st.session_state.api_key:
    st.warning("Please enter your Gemini API Key in the sidebar to start.")
    st.stop()

llm_client = LLMClient(st.session_state.api_key)
# Show connected model in sidebar
if hasattr(llm_client, 'model') and hasattr(llm_client.model, 'model_name'):
     st.sidebar.success(f"Connected: `{llm_client.model.model_name}`")

cartographer = Cartographer(llm_client)
assessor = Assessor(llm_client)

# Generate Graph Flow
if generate_btn and target_role:
    with st.spinner(f"Cartographer is mapping the known universe of '{target_role}'..."):
        try:
            graph_data = cartographer.map_role(target_role)
            
            if "error" in graph_data:
                st.error(f"AI Error: {graph_data['error']}")
                if "raw" in graph_data:
                    with st.expander("View Raw Output"):
                        st.code(graph_data['raw'])
            else:
                st.session_state.graph.build_from_json(graph_data)
                st.success("Graph generated successfully!")
                st.rerun() # Force rerun to update the graph view immediately
        except Exception as e:
            st.error(f"Failed to generate graph: {e}")

# Main Content Area
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f"## Learning Path: {target_role if target_role else 'Not Set'}")
    
    # Graph Visualization
    graph_dict = st.session_state.graph.to_dict()
    if graph_dict['nodes']:
        # The agraph component returns the ID of the clicked node
        selected_node_id = render_graph(graph_dict)
        
        if selected_node_id:
            st.session_state.selected_node = selected_node_id
    else:
        st.info("Enter a role and click 'Generate Graph' to begin.")

with col2:
    if 'selected_node' in st.session_state and st.session_state.selected_node:
        # Find node data
        node_data = next((n for n in graph_dict['nodes'] if n['id'] == st.session_state.selected_node), None)
        
        if node_data:
            render_skill_details(node_data)
            
            # Action Buttons
            if st.button("Take Quiz"):
                st.session_state.quiz_skill = node_data['id']
                # Generate quiz
                with st.spinner("Assessor is preparing your exam..."):
                    quiz = assessor.generate_quiz(node_data['id'], node_data.get('desc', ''))
                    st.session_state.current_quiz = quiz

# Quiz Modal / Section
if st.session_state.current_quiz:
    st.markdown("---")
    st.markdown(f"## 📝 Assessment: {st.session_state.quiz_skill}")
    
    answers = render_quiz(st.session_state.current_quiz, st.session_state.quiz_skill)
    
    if answers:
        # Evaluate
        results = []
        for i, q in enumerate(st.session_state.current_quiz):
            results.append({
                "question": q['question'],
                "user_answer": answers[i],
                "correct_answer": q['correct_answer']
            })
            
        evaluation = assessor.evaluate_quiz(results)
        
        if evaluation['passed']:
            st.balloons()
            st.success(f"Passed! Score: {evaluation['score']}/{evaluation['total']}")
            st.session_state.graph.mark_completed(st.session_state.quiz_skill)
            st.session_state.current_quiz = None # Close quiz
            st.rerun()
        else:
            st.error(f"Failed. Score: {evaluation['score']}/{evaluation['total']}")
            st.markdown(f"**Feedback:** {evaluation['feedback']}")
            st.markdown("**Failed Concepts:**")
            for fc in evaluation['failed_concepts']:
                st.markdown(f"- {fc}")
            
            # Logic to flag blockers could go here
            # For now, just reset quiz to allow retry
            if st.button("Close Quiz"):
                st.session_state.current_quiz = None
                st.rerun()
