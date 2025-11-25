# Technology Stack

## Core Technologies

### 1. Python
The primary programming language used for all backend logic and application control.

### 2. Streamlit
**Why?** Rapid UI development for data/AI apps.
**Usage**: Handles the web server, session state, and UI widgets.

### 3. Google Gemini Pro (via `google-generativeai`)
**Why?** High-quality reasoning for complex tasks like curriculum design and quiz generation.
**Usage**:
- `Cartographer`: Generates the skill graph structure.
- `Assessor`: Generates and evaluates quizzes.

### 4. NetworkX
**Why?** Standard library for graph theory in Python.
**Usage**:
- Manages the DAG (Directed Acyclic Graph).
- Handles topological sorting and predecessor lookups.

### 5. Streamlit Agraph
**Why?** Interactive graph visualization within Streamlit.
**Usage**: Renders the visual representation of skills and dependencies.

## Dependencies
- `streamlit`
- `networkx`
- `google-generativeai`
- `streamlit-agraph`
- `pandas` (Internal dependency for some data ops)
- `plotly` (Optional, for advanced charts)
