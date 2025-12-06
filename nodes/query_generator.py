"""
Query Generator Node - Generates SQL queries from natural language questions.
This is an LLM node that uses the schema extractor tool.
"""
from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI


def query_generator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a SQL query from the user's natural language question.
    Uses the database schema to create an appropriate query.
    
    Args:
        state (Dict[str, Any]): Current state containing:
            - question: User's natural language question
            - schema: Database schema information
            - iteration: Current iteration count (for refinement)
            - feedback: Feedback from safety check (if any)
            
    Returns:
        Dict[str, Any]: Updated state with draft_sql_query
    """
    question = state.get("question", "")
    schema = state.get("schema", "")
    iteration = state.get("iteration", 0)
    feedback = state.get("feedback", "")
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    # Build the prompt
    system_prompt = """You are an expert SQL query generator. Your task is to convert natural language questions into SQL queries.

IMPORTANT RULES:
1. Generate ONLY SELECT queries (read-only operations)
2. Do NOT use DROP, DELETE, UPDATE, INSERT, ALTER, or any destructive commands
3. Use proper SQL syntax for SQLite
4. Include appropriate WHERE clauses, JOINs, and aggregations as needed
5. Return ONLY the SQL query without any explanation or markdown formatting
6. Do not include semicolons at the end

Database Schema:
{schema}

Generate a safe, read-only SQL query to answer the user's question."""

    messages = [
        SystemMessage(content=system_prompt.format(schema=schema))
    ]
    
    # Add refinement context if this is a retry
    if iteration > 0 and feedback:
        messages.append(HumanMessage(content=f"Previous attempt failed safety check. Feedback: {feedback}"))
    
    messages.append(HumanMessage(content=f"Question: {question}"))
    
    # Generate query
    response = llm.invoke(messages)
    draft_query = response.content.strip()
    
    # Clean up the query (remove markdown code blocks if present)
    if draft_query.startswith("```sql"):
        draft_query = draft_query.replace("```sql", "").replace("```", "").strip()
    elif draft_query.startswith("```"):
        draft_query = draft_query.replace("```", "").strip()
    
    # Remove trailing semicolons
    draft_query = draft_query.rstrip(";").strip()
    
    print(f"\n Generated SQL Query (Iteration {iteration + 1}):")
    print(f"   {draft_query}\n")
    
    return {
        "draft_sql_query": draft_query,
        "iteration": iteration + 1,
        "feedback": ""  # Clear feedback for next iteration
    }
