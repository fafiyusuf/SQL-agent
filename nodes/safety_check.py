"""
Safety Check Node - Analyzes SQL queries for safety before execution.
Uses both code-based checks and optional LLM verification.
"""
from typing import Dict, Any, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import re


def check_destructive_commands(query: str) -> Tuple[bool, str]:
    """
    Check if the query contains any destructive SQL commands.
    
    Args:
        query (str): The SQL query to check.
        
    Returns:
        Tuple[bool, str]: (is_safe, feedback_message)
    """
    # Convert to uppercase for checking
    query_upper = query.upper()
    
    # List of prohibited commands
    destructive_commands = [
        "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", 
        "TRUNCATE", "REPLACE", "CREATE", "GRANT", "REVOKE"
    ]
    
    for command in destructive_commands:
        # Use word boundary regex to avoid false positives
        pattern = r'\b' + command + r'\b'
        if re.search(pattern, query_upper):
            return False, f"Query contains prohibited command: {command}. Only SELECT queries are allowed."
    
    # Check if query starts with SELECT (allowing for whitespace and comments)
    query_stripped = query.strip()
    if not query_stripped.upper().startswith("SELECT"):
        return False, "Query must be a SELECT statement. Only read-only queries are allowed."
    
    return True, ""


def llm_safety_check(query: str) -> Tuple[bool, str]:
    """
    Use LLM to perform additional safety verification.
    
    Args:
        query (str): The SQL query to check.
        
    Returns:
        Tuple[bool, str]: (is_safe, feedback_message)
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    system_prompt = """You are a SQL security expert. Analyze the given SQL query for safety.

A query is SAFE if:
1. It is a SELECT statement (read-only)
2. It does not contain any destructive commands (DROP, DELETE, UPDATE, INSERT, ALTER, etc.)
3. It does not attempt to bypass restrictions or exploit vulnerabilities
4. It follows standard SQL best practices

Respond with EXACTLY one of these formats:
SAFE
or
UNSAFE: [brief reason]

Do not provide any other explanation."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Query to analyze:\n{query}")
    ]
    
    response = llm.invoke(messages)
    result = response.content.strip()
    
    if result.upper().startswith("SAFE"):
        return True, ""
    else:
        feedback = result.replace("UNSAFE:", "").strip() if "UNSAFE:" in result else result
        return False, feedback


def safety_check_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the draft SQL query for safety.
    Performs both code-based and LLM-based safety checks.
    
    Args:
        state (Dict[str, Any]): Current state containing:
            - draft_sql_query: The SQL query to check
            - iteration: Current iteration count
            
    Returns:
        Dict[str, Any]: Updated state with:
            - is_safe: Boolean indicating if query is safe
            - feedback: Feedback message if unsafe
            - next_action: "execute" or "refine"
    """
    query = state.get("draft_sql_query", "")
    iteration = state.get("iteration", 0)
    max_iterations = state.get("max_iterations", 3)
    
    print("🛡️  Running safety checks...")
    
    # First, run code-based checks
    is_safe, feedback = check_destructive_commands(query)
    
    if not is_safe:
        print(f"   ❌ Code-based check FAILED: {feedback}")
        
        # Check if we've exceeded max iterations
        if iteration >= max_iterations:
            return {
                "is_safe": False,
                "feedback": f"Maximum refinement attempts ({max_iterations}) reached. {feedback}",
                "next_action": "stop",
                "error": "Safety check failed after maximum iterations"
            }
        
        return {
            "is_safe": False,
            "feedback": feedback,
            "next_action": "refine"
        }
    
    # If code-based checks pass, run LLM safety check
    is_safe, llm_feedback = llm_safety_check(query)
    
    if not is_safe:
        print(f"   LLM safety check FAILED: {llm_feedback}")
        
        if iteration >= max_iterations:
            return {
                "is_safe": False,
                "feedback": f"Maximum refinement attempts ({max_iterations}) reached. {llm_feedback}",
                "next_action": "stop",
                "error": "Safety check failed after maximum iterations"
            }
        
        return {
            "is_safe": False,
            "feedback": llm_feedback,
            "next_action": "refine"
        }
    
    print("   Safety checks PASSED\n")
    
    return {
        "is_safe": True,
        "feedback": "",
        "next_action": "execute"
    }
