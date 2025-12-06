"""
Summary Node - Converts query results into human-readable answers.
This is an LLM node that interprets results for the user.
"""
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import pandas as pd


def summary_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert query results into a human-readable answer.
    
    Args:
        state (Dict[str, Any]): Current state containing:
            - question: Original user question
            - draft_sql_query: The executed SQL query
            - query_result: Results from query execution
            
    Returns:
        Dict[str, Any]: Updated state with final_answer
    """
    question = state.get("question", "")
    query = state.get("draft_sql_query", "")
    result = state.get("query_result", {})
    
    print(" Generating summary...")
    
    # Handle error cases
    if state.get("error"):
        return {
            "final_answer": f"I apologize, but I encountered an error: {state['error']}"
        }
    
    if not result.get("success", False):
        return {
            "final_answer": f"I apologize, but the query failed: {result.get('error', 'Unknown error')}"
        }
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    # Format the results for the LLM
    if result.get("data") is not None:
        df = result["data"]
        data_summary = df.to_string(index=False, max_rows=20)
        
        if len(df) > 20:
            data_summary += f"\n... (showing first 20 of {len(df)} rows)"
    else:
        data_summary = "No data returned."
    
    system_prompt = """You are a helpful assistant that explains SQL query results in plain English.

Your task is to:
1. Provide a clear, conversational answer to the user's question
2. Highlight key insights from the data
3. Use natural language, not technical jargon
4. Be concise but informative
5. If the data shows interesting patterns or notable values, mention them

Do not:
- Simply list all the data
- Use overly technical SQL terminology
- Repeat the query unless relevant to the explanation"""

    user_prompt = f"""User's Question: {question}

SQL Query Executed: {query}

Query Results:
{data_summary}

Please provide a clear, helpful answer to the user's question based on these results."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = llm.invoke(messages)
    final_answer = response.content.strip()
    
    print(f" Summary generated\n")
    
    return {
        "final_answer": final_answer
    }