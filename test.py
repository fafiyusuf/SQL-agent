"""
Test script for the SQL Agent - No API key required!
Tests the workflow with mock responses.
"""
import sqlite3
from nodes.tools_node import DatabaseTools
from nodes.safety_check import check_destructive_commands


def test_database_setup():
    """Test that the database is set up correctly."""
    print("\n" + "="*70)
    print("🧪 TEST 1: Database Setup")
    print("="*70)
    
    db_path = "database/test_db.sqlite"
    db_tools = DatabaseTools(db_path)
    
    # Test schema extraction
    schema = db_tools.get_schema()
    print("\n✅ Schema extracted successfully!")
    print(schema)
    
    return db_path


def test_safety_checks():
    """Test the safety check functionality."""
    print("\n" + "="*70)
    print("🧪 TEST 2: Safety Checks")
    print("="*70)
    
    test_queries = [
        ("SELECT * FROM employees", True, "Safe SELECT query"),
        ("DELETE FROM employees WHERE id = 1", False, "Destructive DELETE"),
        ("DROP TABLE employees", False, "Destructive DROP"),
        ("UPDATE employees SET salary = 100000", False, "Destructive UPDATE"),
        ("SELECT name, salary FROM employees WHERE department = 'Engineering'", True, "Safe filtered SELECT"),
    ]
    
    print("\nTesting various SQL queries:\n")
    
    for query, expected_safe, description in test_queries:
        is_safe, feedback = check_destructive_commands(query)
        status = "✅ PASS" if is_safe == expected_safe else "❌ FAIL"
        
        print(f"{status} - {description}")
        print(f"   Query: {query}")
        print(f"   Safe: {is_safe}, Expected: {expected_safe}")
        if feedback:
            print(f"   Feedback: {feedback}")
        print()


def test_query_execution():
    """Test query execution without LLM."""
    print("\n" + "="*70)
    print("🧪 TEST 3: Query Execution")
    print("="*70)
    
    db_path = "database/test_db.sqlite"
    db_tools = DatabaseTools(db_path)
    
    test_queries = [
        "SELECT COUNT(*) as total_employees FROM employees",
        "SELECT department, COUNT(*) as count FROM employees GROUP BY department",
        "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3",
    ]
    
    print("\nExecuting test queries:\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: {query}")
        result = db_tools.execute_query(query)
        print(f"Result:\n{result}\n")
        print("-" * 70 + "\n")


def test_workflow_logic():
    """Test the workflow routing logic."""
    print("\n" + "="*70)
    print("🧪 TEST 4: Workflow Logic")
    print("="*70)
    
    print("\nTesting state transitions:\n")
    
    # Test safe query flow
    state = {
        "draft_sql_query": "SELECT * FROM employees",
        "iteration": 0,
        "max_iterations": 3
    }
    
    is_safe, feedback = check_destructive_commands(state["draft_sql_query"])
    
    if is_safe:
        print("✅ Safe query would proceed to execution")
        print(f"   Query: {state['draft_sql_query']}")
    
    # Test unsafe query flow
    state = {
        "draft_sql_query": "DELETE FROM employees",
        "iteration": 0,
        "max_iterations": 3
    }
    
    is_safe, feedback = check_destructive_commands(state["draft_sql_query"])
    
    if not is_safe:
        print("\n✅ Unsafe query would trigger refinement")
        print(f"   Query: {state['draft_sql_query']}")
        print(f"   Feedback: {feedback}")
        print(f"   Would return to Query Generator (iteration {state['iteration'] + 1})")
    
    # Test max iterations
    state["iteration"] = 3
    if state["iteration"] >= state["max_iterations"]:
        print("\n✅ Max iterations reached - workflow would stop")
        print(f"   Final iteration: {state['iteration']}")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("🧪 SQL AGENT - UNIT TESTS")
    print("="*70)
    print("\nThese tests don't require an OpenAI API key.\n")
    
    # Initialize database
    from main import initialize_sample_database
    initialize_sample_database()
    
    # Run tests
    test_database_setup()
    test_safety_checks()
    test_query_execution()
    test_workflow_logic()
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("1. Add your OpenAI API key to .env file")
    print("2. Run 'python demo.py' to see the full agent in action")
    print("3. Run 'python main.py' for interactive mode\n")


if __name__ == "__main__":
    run_all_tests()
