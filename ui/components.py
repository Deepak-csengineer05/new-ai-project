import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from typing import List, Dict, Any

def render_graph(graph_data: Dict[str, Any]):
    """
    Renders the interactive skill graph using streamlit-agraph.
    """
    nodes = []
    edges = []
    
    # Define colors based on status
    colors = {
        "pending": "#424242",   # Dark Grey
        "completed": "#00e676", # Green
        "blocked": "#ff1744",   # Red
        "current": "#2979ff"    # Blue
    }

    # Convert NetworkX/Dict data to agraph Nodes
    for node_id in graph_data['nodes']:
        # We need to access the node attributes from the graph dictionary
        # The graph_data from nx.node_link_data has 'nodes' as a list of dicts
        # and 'links' as a list of dicts.
        
        # However, nx.node_link_data structure depends on the format. 
        # Let's assume standard node-link format:
        # nodes: [{'id': 'A', 'status': 'pending', ...}, ...]
        
        status = node_id.get('status', 'pending')
        color = colors.get(status, colors['pending'])
        
        nodes.append(Node(
            id=node_id['id'],
            label=node_id['id'],
            size=25,
            color=color,
            # shape="circularImage" if we had images, else "dot"
            font={'color': 'white'}
        ))

    # NetworkX node_link_data can return 'links' or 'edges' depending on version/config
    links = graph_data.get('links', graph_data.get('edges', []))
    for link in links:
        edges.append(Edge(
            source=link['source'],
            target=link['target'],
            color="#bdbdbd",
            type="CURVE_SMOOTH"
        ))

    config = Config(
        width=800,
        height=600,
        directed=True, 
        physics=True, 
        hierarchical=True, # Good for DAGs
        # hierarchical options
        sortMethod="directed"
    )

    return agraph(nodes=nodes, edges=edges, config=config)

def render_quiz(quiz_data: List[Dict[str, Any]], skill_name: str):
    """
    Renders the quiz interface.
    """
    st.markdown(f"### 📝 Quiz: {skill_name}")
    
    answers = {}
    
    with st.form(key=f"quiz_{skill_name}"):
        for i, q in enumerate(quiz_data):
            st.markdown(f"**Q{i+1}: {q['question']}**")
            answers[i] = st.radio(
                "Select an answer:",
                q['options'],
                key=f"q_{i}_{skill_name}",
                label_visibility="collapsed"
            )
            st.markdown("---")
            
        submit_button = st.form_submit_button(label="Submit Quiz")
        
    if submit_button:
        return answers
    return None

def render_skill_details(skill_data: Dict[str, Any]):
    """
    Renders details for a selected skill in the sidebar or modal.
    """
    st.markdown(f"## {skill_data['id']}")
    st.markdown(f"**Status:** {skill_data.get('status', 'pending').title()}")
    st.markdown(f"_{skill_data.get('description', 'No description available.')}_")
    
    st.markdown("### 📚 Resources")
    for res in skill_data.get('resources', []):
        st.markdown(f"- [{res}]({res})")
