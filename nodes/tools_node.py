"""
Tools Node - Provides utility tools for the SQL agent.
Contains Schema Extractor Tool and Query Execution Tool.
"""
import sqlite3
import pandas as pd
from typing import Dict, Any, List


class DatabaseTools:
    """Database utility tools for schema extraction and query execution."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_schema(self) -> str:
        """
        Extract and return the database schema including table names, columns, and types.
        This tool helps understand the structure of the database.
        
        Returns:
            str: Formatted schema information with tables, columns, and data types.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            schema_info = "DATABASE SCHEMA:\n" + "="*60 + "\n\n"
            
            for table in tables:
                table_name = table[0]
                schema_info += f"Table: {table_name}\n"
                schema_info += "-" * 40 + "\n"
                
                # Get column information
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                
                for col in columns:
                    col_id, col_name, col_type, not_null, default_val, pk = col
                    schema_info += f"  - {col_name} ({col_type})"
                    if pk:
                        schema_info += " [PRIMARY KEY]"
                    if not_null:
                        schema_info += " [NOT NULL]"
                    schema_info += "\n"
                
                # Get sample row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                schema_info += f"  Total rows: {count}\n\n"
            
            conn.close()
            return schema_info
            
        except Exception as e:
            return f"Error extracting schema: {str(e)}"
    
    def execute_query(self, query: str) -> str:
        """
        Execute a SQL query and return the results.
        This tool should only be called after the query has been verified as safe.
        
        Args:
            query (str): The SQL query to execute.
            
        Returns:
            str: Query results formatted as a string, or error message.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Execute query and get results as DataFrame
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if df.empty:
                return "Query executed successfully. No results returned."
            
            # Format results
            result = f"Query returned {len(df)} row(s):\n\n"
            result += df.to_string(index=False)
            
            return result
            
        except Exception as e:
            return f"Error executing query: {str(e)}"
