# SkillGenome Architecture

## Overview
SkillGenome is a modular application designed to build dynamic competency graphs using Generative AI. It follows a clean separation of concerns between the backend logic (`core/`) and the frontend UI (`ui/`).

## Directory Structure
```
SkillGenome/
├── app.py                 # Main Entry Point (Streamlit)
├── core/                  # Backend Logic
│   ├── llm_client.py      # Gemini API Wrapper
│   ├── graph_manager.py   # Graph Data Structure (NetworkX)
│   └── agents.py          # AI Agents (Cartographer, Assessor)
├── ui/                    # Frontend Components
│   ├── components.py      # Reusable UI widgets (Graph, Quiz)
│   └── styles.css         # Custom Styling
└── docs/                  # Documentation
```

## Core Components

### 1. The Cartographer (Agent)
- **Role**: Decomposes a high-level job role into a dependency graph.
- **Mechanism**: Uses Gemini Pro to generate a JSON structure of Nodes (Skills) and Edges (Dependencies).
- **Output**: A Directed Acyclic Graph (DAG) where edges represent prerequisites.

### 2. The Assessor (Agent)
- **Role**: Validates user knowledge.
- **Mechanism**: Generates context-aware multiple-choice quizzes for specific skills.
- **Evaluation**: Checks answers and provides feedback.

### 3. SkillGraph (Data Structure)
- **Library**: `networkx`
- **Function**: Manages the graph state, topological sorting, and dependency tracking.
- **Serialization**: Converts graph data to/from JSON for Streamlit session state storage.

### 4. User Interface
- **Framework**: `streamlit`
- **Visualization**: `streamlit-agraph` for interactive graph rendering.
- **Styling**: Custom CSS for a dark, glassmorphism-inspired aesthetic.

## Data Flow
1.  **User Input** -> `app.py` captures Role.
2.  **Generation** -> `Cartographer` calls LLM -> Returns JSON.
3.  **Build** -> `SkillGraph` parses JSON -> Builds NetworkX graph.
4.  **Render** -> `ui/components.py` visualizes the graph.
5.  **Interaction** -> User clicks Node -> `Assessor` generates Quiz.
6.  **Update** -> Quiz Passed -> `SkillGraph` updates Node status -> Graph re-renders.
