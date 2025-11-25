from typing import Dict, List, Any
from .llm_client import LLMClient
from .graph_manager import SkillGraph

class Cartographer:
    """
    Agent 1: The Cartographer
    Responsible for decomposing a role into a graph of skills.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def map_role(self, role: str) -> Dict[str, Any]:
        """
        Generates a skill graph for a given role.
        Returns a dictionary compatible with SkillGraph.build_from_json.
        """
        prompt = f"""
        Act as an expert curriculum designer and graph theorist.
        I need to learn the role: "{role}".
        
        Create a detailed dependency graph of skills required for this role.
        Decompose the role into granular skills (nodes) and their prerequisites (edges).
        
        Output a JSON object with two keys: "nodes" and "edges".
        
        "nodes": A list of objects, each with:
          - "id": Unique string name of the skill (e.g., "Python Basics").
          - "desc": Brief description of why this skill is needed.
          - "resources": A list of 2-3 high-quality learning resource URLs (documentation, tutorials).
          
        "edges": A list of objects, each with:
          - "source": The prerequisite skill ID.
          - "target": The dependent skill ID.
          - "reason": Brief explanation of the dependency (e.g., "Need to know variables before loops").
          
        Ensure the graph is a Directed Acyclic Graph (DAG). 
        Include at least 10-15 nodes to make it comprehensive but manageable.
        Start from foundational concepts up to advanced topics.
        """
        
        return self.llm.generate_json(prompt)

class Assessor:
    """
    Agent 2: The Assessor
    Responsible for generating quizzes and evaluating understanding.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def generate_quiz(self, skill_name: str, context_desc: str) -> List[Dict[str, Any]]:
        """
        Generates a mini-quiz for a specific skill.
        """
        prompt = f"""
        Act as a strict technical interviewer.
        Create a mini-quiz to test a student's understanding of the skill: "{skill_name}".
        Context: {context_desc}
        
        Generate 3 multiple-choice questions.
        
        Output a JSON list of objects, each with:
          - "question": The question text.
          - "options": A list of 4 possible answers.
          - "correct_answer": The exact string of the correct option.
          - "explanation": Why the answer is correct.
        """
        
        response = self.llm.generate_json(prompt)
        if isinstance(response, list):
            return response
        # Handle case where LLM wraps list in a dict key like "questions"
        if isinstance(response, dict):
            for key in response:
                if isinstance(response[key], list):
                    return response[key]
        return []

    def evaluate_quiz(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluates the quiz results.
        Input: List of {question, user_answer, correct_answer}
        Output: Analysis of gaps.
        """
        # Simple pass/fail logic for now, could be enhanced with LLM analysis
        score = 0
        total = len(results)
        failed_concepts = []
        
        for item in results:
            if item['user_answer'] == item['correct_answer']:
                score += 1
            else:
                failed_concepts.append(item.get('question', 'Unknown Question'))
                
        passed = (score / total) >= 0.7 if total > 0 else False
        
        return {
            "score": score,
            "total": total,
            "passed": passed,
            "failed_concepts": failed_concepts,
            "feedback": "Great job!" if passed else "You need to review these concepts."
        }
