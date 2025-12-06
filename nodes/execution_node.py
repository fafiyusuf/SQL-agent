"""
Execution Node - Executes safe SQL queries using the Query Tool.
"""
from typing import Dict, Any
import sqlite3
import pandas as pd


def execution_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute the safe SQL query and return results.
    
    Args:
        state (Dict[str, Any]): Current state containing:
            - draft_sql_query: The safe SQL query to execute
            - db_path: Path to the database
            
    Returns:
        Dict[str, Any]: Updated state with query_result
    """
    query = state.get("draft_sql_query", "")
    db_path = state.get("db_path", "")
    
    print(" Executing query...")
    
    try:
        conn = sqlite3.connect(db_path)
        
        # Execute query and get results as DataFrame
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            result = {
                "success": True,
                "row_count": 0,
                "data": None,
                "message": "Query executed successfully. No results returned."
            }
        else:
            result = {
                "success": True,
                "row_count": len(df),
                "data": df,
                "columns": df.columns.tolist(),
                "message": f"Query returned {len(df)} row(s)"
            }
        
        print(f"   {result['message']}\n")
        
        return {
            "query_result": result,
            "error": None
        }
        
    except Exception as e:
        error_msg = f"Error executing query: {str(e)}"
        print(f"   {error_msg}\n")
        
        return {
            "query_result": {
                "success": False,
                "error": str(e)
            },
            "error": error_msg
        }
