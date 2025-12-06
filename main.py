"""
SQL Agent - Natural Language to SQL Query System
Uses LangGraph to orchestrate a multi-node workflow for safe SQL query execution.
"""
import os
import sys
import sqlite3
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# Import node functions
from nodes.query_generator import query_generator_node
from nodes.safety_check import safety_check_node
from nodes.execution_node import execution_node
from nodes.summary_node import summary_node
from nodes.tools_node import DatabaseTools


# Define the state schema
class AgentState(TypedDict):
    """State object that flows through the graph."""
    question: str
    schema: str
    draft_sql_query: str
    is_safe: bool
    feedback: str
    query_result: dict
    final_answer: str
    iteration: int
    max_iterations: int
    next_action: str
    error: str
    db_path: str


def get_schema_node(state: AgentState) -> AgentState:
    """
    Node to extract database schema.
    This runs once at the beginning to get schema information.
    """
    db_path = state.get("db_path", "")
    print("📊 Extracting database schema...\n")
    
    db_tools = DatabaseTools(db_path)
    schema = db_tools.get_schema()
    
    return {"schema": schema}


def route_after_safety_check(state: AgentState) -> str:
    """
    Routing function to determine next step after safety check.
    
    Returns:
        str: Name of the next node ("query_generator", "execution", or "end")
    """
    next_action = state.get("next_action", "")
    
    if next_action == "execute":
        return "execution"
    elif next_action == "refine":
        return "query_generator"
    else:  # stop or error
        return "end"


def create_workflow(db_path: str, max_iterations: int = 3) -> StateGraph:
    """
    Create the LangGraph workflow for the SQL agent.
    
    Args:
        db_path (str): Path to the SQLite database
        max_iterations (int): Maximum number of query refinement attempts
        
    Returns:
        StateGraph: Compiled workflow graph
    """
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("get_schema", get_schema_node)
    workflow.add_node("query_generator", query_generator_node)
    workflow.add_node("safety_check", safety_check_node)
    workflow.add_node("execution", execution_node)
    workflow.add_node("summary", summary_node)
    
    # Define the flow
    workflow.set_entry_point("get_schema")
    workflow.add_edge("get_schema", "query_generator")
    workflow.add_edge("query_generator", "safety_check")
    
    # Conditional routing after safety check
    workflow.add_conditional_edges(
        "safety_check",
        route_after_safety_check,
        {
            "query_generator": "query_generator",
            "execution": "execution",
            "end": "summary"
        }
    )
    
    workflow.add_edge("execution", "summary")
    workflow.add_edge("summary", END)
    
    return workflow.compile()


def run_sql_agent(question: str, db_path: str = "database/test_db.sqlite", max_iterations: int = 3):
    """
    Run the SQL agent with a natural language question.
    
    Args:
        question (str): Natural language question to answer
        db_path (str): Path to the SQLite database
        max_iterations (int): Maximum number of query refinement attempts
        
    Returns:
        dict: Final state with the answer
    """
    print("\n" + "="*70)
    print("🤖 SQL AGENT - Natural Language to SQL")
    print("="*70)
    print(f"\n❓ Question: {question}\n")
    
    # Create the workflow
    app = create_workflow(db_path, max_iterations)
    
    # Initial state
    initial_state = {
        "question": question,
        "schema": "",
        "draft_sql_query": "",
        "is_safe": False,
        "feedback": "",
        "query_result": {},
        "final_answer": "",
        "iteration": 0,
        "max_iterations": max_iterations,
        "next_action": "",
        "error": "",
        "db_path": db_path
    }
    
    # Run the workflow
    final_state = app.invoke(initial_state)
    
    print("="*70)
    print("✨ FINAL ANSWER:")
    print("="*70)
    print(f"\n{final_state.get('final_answer', 'No answer generated.')}\n")
    
    # Show the executed query
    if final_state.get("draft_sql_query"):
        print("\n" + "-"*70)
        print("📋 Executed SQL Query:")
        print("-"*70)
        print(f"{final_state['draft_sql_query']}\n")
    
    return final_state


def initialize_sample_database(db_path: str = "database/test_db.sqlite"):
    """
    Initialize a comprehensive database with realistic business data.
    Runs create_database.py if database doesn't exist or is empty.
    
    Args:
        db_path (str): Path to the SQLite database
    """
    import os
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    conn.close()
    
    if not tables:
        print("Initializing comprehensive database...")
        print("Running create_database.py...\n")
        os.system(f"{sys.executable} create_database.py")
    else:
        # Check if we have the new schema (8 tables)
        if len(tables) < 8:
            print("Updating to comprehensive database schema...")
            print("Running create_database.py...\n")
            os.system(f"{sys.executable} create_database.py")


def main():
    """Main function to run the SQL agent."""
    # Load environment variables
    load_dotenv()
    
    # Check for Google API key (Gemini)
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please create a .env file with your Google Gemini API key:")
        print("GOOGLE_API_KEY=your-google-api-key-here")
        print("\nGet your API key from: https://aistudio.google.com/app/apikey")
        return
    
    # Database path
    db_path = "database/test_db.sqlite"
    
    # Initialize sample database if needed
    initialize_sample_database(db_path)
    
    # Example questions to demonstrate the agent
    example_questions = [
        "How many employees work in the Engineering department?",
        "What is the average salary by department?",
        "Who are the top 3 highest paid employees?",
        "Show me all employees hired after 2020",
        "What is the total budget across all departments?",
        "Which products are in the Electronics category?",
        "Who are the top 5 customers by total spent?",
        "How many orders were placed in November 2024?",
        "What's the average order value?",
        "Show me all unresolved customer support tickets",
        "Which products have low stock (under 100 units)?",
        "What are the most popular products by order count?",
    ]
    
    print("\n" + "="*70)
    print("🎯 EXAMPLE QUESTIONS YOU CAN ASK:")
    print("="*70)
    for i, q in enumerate(example_questions, 1):
        print(f"{i}. {q}")
    print("="*70 + "\n")
    
    # Interactive mode
    while True:
        question = input("\n💬 Enter your question (or 'quit' to exit): ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!\n")
            break
        
        if not question:
            print("Please enter a valid question.")
            continue
        
        try:
            run_sql_agent(question, db_path)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


if __name__ == "__main__":
    main()
