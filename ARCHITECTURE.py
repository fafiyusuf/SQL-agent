"""
Workflow visualization and state diagram for the SQL Agent.
This module documents the agent's flow and decision points.
"""

# ASCII Art Workflow Diagram
WORKFLOW_DIAGRAM = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         SQL AGENT WORKFLOW                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│  USER INPUT: "How many employees are in Engineering?"                       │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
         ╔═══════════════════════════════════════╗
         ║  NODE 1: SCHEMA EXTRACTOR             ║
         ║  ────────────────────────────────     ║
         ║  • Connects to database               ║
         ║  • Extracts table structures          ║
         ║  • Gets column types & constraints    ║
         ║  • Returns formatted schema           ║
         ╚═══════════════════════════════════════╝
                                 │
                                 ▼
         ╔═══════════════════════════════════════╗
         ║  NODE 2: QUERY GENERATOR (LLM)        ║◄──────────┐
         ║  ────────────────────────────────     ║           │
         ║  • Receives question + schema         ║           │
         ║  • Uses GPT-4 to generate SQL         ║           │
         ║  • Cleans and formats query           ║           │
         ║  • Returns draft_sql_query            ║           │
         ╚═══════════════════════════════════════╝           │
                                 │                           │
                                 ▼                           │
         ╔═══════════════════════════════════════╗           │
         ║  NODE 3: SAFETY CHECK                 ║           │
         ║  ────────────────────────────────     ║           │
         ║  STEP 1: Code-Based Checks            ║           │
         ║    • Regex pattern matching           ║           │
         ║    • Block: DROP, DELETE, UPDATE...   ║           │
         ║    • Verify starts with SELECT        ║           │
         ║                                       ║           │
         ║  STEP 2: LLM Verification             ║           │
         ║    • Semantic safety analysis         ║           │
         ║    • Intent validation                ║           │
         ║    • Exploit detection                ║           │
         ╚═══════════════════════════════════════╝           │
                    │                  │                     │
           ┌────────┴────────┐         │                     │
           ▼                 ▼                     │
       [SAFE]           [UNSAFE]                  │
           │                 │                     │
           │                 ├─────────────────────┘
           │                 │  (iteration < max)
           │                 │
           │                 └─────> [STOP]
           │                        (iteration >= max)
           │
           ▼
╔═══════════════════════════════════════╗
║  NODE 4: EXECUTION                    ║
║  ────────────────────────────────     ║
║  • Execute approved SQL query         ║
║  • Fetch results with pandas          ║
║  • Format as structured data          ║
║  • Handle errors gracefully           ║
╚═══════════════════════════════════════╝
           │
           ▼
╔═══════════════════════════════════════╗
║  NODE 5: SUMMARY GENERATOR (LLM)      ║
║  ────────────────────────────────     ║
║  • Receives query results             ║
║  • Uses GPT-4 to explain data         ║
║  • Highlights key insights            ║
║  • Returns natural language answer    ║
╚═══════════════════════════════════════╝
           │
           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  OUTPUT: "The Engineering department has 4 employees. They are..."          │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# State Schema Documentation
STATE_SCHEMA = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         AGENT STATE SCHEMA                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

class AgentState(TypedDict):
    # Input
    question: str              # User's natural language question
    db_path: str              # Path to SQLite database
    
    # Schema Information
    schema: str               # Database schema (tables, columns, types)
    
    # Query Generation
    draft_sql_query: str      # Generated SQL query
    iteration: int            # Current refinement iteration (0-based)
    max_iterations: int       # Maximum allowed refinements (default: 3)
    
    # Safety Check
    is_safe: bool            # Whether query passed safety checks
    feedback: str            # Feedback for refinement (if unsafe)
    next_action: str         # Routing decision: "execute", "refine", "stop"
    
    # Execution
    query_result: dict       # Query execution results
    error: str              # Error message (if any)
    
    # Output
    final_answer: str        # Human-readable answer

Query Result Structure:
{
    "success": bool,
    "row_count": int,
    "data": pandas.DataFrame,
    "columns": List[str],
    "message": str,
    "error": str  # Only if success=False
}
"""

# Decision Points
DECISION_LOGIC = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         ROUTING LOGIC                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

After SAFETY CHECK node, the workflow decides next step:

┌─────────────────────────────────────┐
│ IF query is SAFE:                   │
│   next_action = "execute"           │
│   → Proceed to EXECUTION node       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ IF query is UNSAFE:                 │
│   IF iteration < max_iterations:    │
│     next_action = "refine"          │
│     → Return to QUERY GENERATOR     │
│   ELSE:                             │
│     next_action = "stop"            │
│     → Proceed to SUMMARY (error)    │
└─────────────────────────────────────┘

Safety Check Returns:
  • is_safe: Boolean
  • feedback: String (empty if safe, error message if unsafe)
  • next_action: "execute" | "refine" | "stop"
"""

# Node Responsibilities
NODE_DETAILS = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         NODE DETAILS                                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 SCHEMA EXTRACTOR NODE
────────────────────────
Type: Pure Function (No LLM)
File: nodes/tools_node.py

Inputs:
  • db_path: str

Process:
  1. Connect to SQLite database
  2. Query sqlite_master for table list
  3. For each table:
     - Get column info via PRAGMA table_info
     - Count total rows
  4. Format as readable schema

Outputs:
  • schema: str (formatted schema information)

Example Output:
  ```
  DATABASE SCHEMA:
  ============================================================
  
  Table: employees
  ----------------------------------------
    - id (INTEGER) [PRIMARY KEY]
    - name (TEXT) [NOT NULL]
    - department (TEXT) [NOT NULL]
    ...
  ```

────────────────────────────────────────────────────────────

🤖 QUERY GENERATOR NODE
────────────────────────
Type: LLM Node (GPT-4)
File: nodes/query_generator.py

Inputs:
  • question: str
  • schema: str
  • iteration: int (for refinement context)
  • feedback: str (if refining)

Process:
  1. Build system prompt with schema
  2. Add user question
  3. If refining, include feedback
  4. Call GPT-4 to generate SQL
  5. Clean output (remove markdown, semicolons)

Outputs:
  • draft_sql_query: str
  • iteration: int (incremented)

Example:
  Input:  "How many engineers do we have?"
  Output: "SELECT COUNT(*) FROM employees WHERE department = 'Engineering'"

────────────────────────────────────────────────────────────

🛡️ SAFETY CHECK NODE
────────────────────────
Type: Hybrid (Code + LLM)
File: nodes/safety_check.py

Inputs:
  • draft_sql_query: str
  • iteration: int
  • max_iterations: int

Process:
  PHASE 1: Code-Based Checks
    • Regex search for destructive commands
    • Verify query starts with SELECT
    • Fast, deterministic validation
  
  PHASE 2: LLM Verification (if Phase 1 passes)
    • Semantic analysis with GPT-4
    • Intent validation
    • Exploit detection
  
  PHASE 3: Decision
    • If safe: next_action = "execute"
    • If unsafe and iteration < max: next_action = "refine"
    • If unsafe and iteration >= max: next_action = "stop"

Outputs:
  • is_safe: bool
  • feedback: str
  • next_action: str

Blocked Commands:
  DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE, 
  REPLACE, CREATE, GRANT, REVOKE

────────────────────────────────────────────────────────────

⚡ EXECUTION NODE
────────────────────────
Type: Pure Function (No LLM)
File: nodes/execution_node.py

Inputs:
  • draft_sql_query: str
  • db_path: str

Process:
  1. Connect to database
  2. Execute query via pandas.read_sql_query
  3. Format results as DataFrame
  4. Handle errors with try/except

Outputs:
  • query_result: dict
    - success: bool
    - row_count: int
    - data: DataFrame
    - columns: List[str]
    - message: str
  • error: str (if failed)

Error Handling:
  • Syntax errors
  • Missing tables/columns
  • Database connection issues
  • Query timeout (if implemented)

────────────────────────────────────────────────────────────

📝 SUMMARY GENERATOR NODE
────────────────────────
Type: LLM Node (GPT-4)
File: nodes/summary_node.py

Inputs:
  • question: str (original question)
  • draft_sql_query: str
  • query_result: dict

Process:
  1. Format query results as text (max 20 rows)
  2. Build context with question + query + results
  3. Call GPT-4 to generate natural language answer
  4. Focus on insights and key findings

Outputs:
  • final_answer: str

Example:
  Input:  
    Question: "How many engineers?"
    Results: COUNT(*) = 4
  
  Output: 
    "The Engineering department currently has 4 employees. They make up 
     50% of the total workforce and have an average salary of $89,500."

────────────────────────────────────────────────────────────
"""

def print_all_diagrams():
    """Print all workflow diagrams and documentation."""
    print(WORKFLOW_DIAGRAM)
    print("\n" + "="*80 + "\n")
    print(STATE_SCHEMA)
    print("\n" + "="*80 + "\n")
    print(DECISION_LOGIC)
    print("\n" + "="*80 + "\n")
    print(NODE_DETAILS)


if __name__ == "__main__":
    print_all_diagrams()
