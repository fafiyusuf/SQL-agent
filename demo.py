"""
Demo script to test the SQL Agent with example queries.
Run this to see the agent in action!
"""
from main import run_sql_agent, initialize_sample_database
import os
from dotenv import load_dotenv


def run_demo():
    """Run a demonstration of the SQL agent with various questions."""
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found.")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your-api-key-here")
        return
    
    # Database path
    db_path = "database/test_db.sqlite"
    
    # Initialize sample database
    initialize_sample_database(db_path)
    
    # Demo questions - covering different tables
    demo_questions = [
        "How many employees work in the Engineering department?",
        "What are the top 5 best-selling products by order count?",
        "Which customers have spent more than $1500 total?",
        "Show me all unresolved customer support tickets",
        "What's the total revenue from completed orders in November 2024?",
    ]
    
    print("\n" + "="*70)
    print("🚀 SQL AGENT DEMO")
    print("="*70)
    print("\nRunning through example questions...\n")
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n{'='*70}")
        print(f"Demo Question {i}/{len(demo_questions)}")
        print('='*70)
        
        try:
            run_sql_agent(question, db_path)
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        if i < len(demo_questions):
            input("\n⏸️  Press Enter to continue to next question...")
    
    print("\n" + "="*70)
    print("✅ DEMO COMPLETE!")
    print("="*70)
    print("\nYou can now run 'python main.py' for interactive mode.\n")


if __name__ == "__main__":
    run_demo()
