"""
SQL Agent Web Interface - Streamlit UI
A modern web interface for the Natural Language to SQL Query System
"""
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv

# Import the SQL agent workflow
from main import create_workflow, AgentState

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SQL Agent - NL to SQL",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with icon support
st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .sql-query {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        font-family: 'Courier New', monospace;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    if 'current_result' not in st.session_state:
        st.session_state.current_result = None
    if 'api_key_valid' not in st.session_state:
        st.session_state.api_key_valid = bool(os.getenv("GOOGLE_API_KEY"))


def check_api_key():
    """Check if API key is configured."""
    return bool(os.getenv("GOOGLE_API_KEY"))


def run_query(question: str, db_path: str = "database/test_db.sqlite"):
    """
    Run a natural language query through the SQL agent.
    
    Args:
        question: Natural language question
        db_path: Path to SQLite database
        
    Returns:
        dict: Result containing answer, SQL query, and data
    """
    try:
        # Build the workflow
        workflow = create_workflow(db_path=db_path)
        
        # Initial state (must be a dict, not AgentState instance)
        initial_state = {
            "question": question,
            "schema": "",
            "draft_sql_query": "",
            "is_safe": False,
            "feedback": "",
            "query_result": {},
            "final_answer": "",
            "iteration": 0,
            "max_iterations": 3,
            "next_action": "",
            "error": "",
            "db_path": db_path
        }
        
        # Run the workflow
        with st.spinner('⚙️ Processing your question...'):
            final_state = workflow.invoke(initial_state)
        
        return {
            'success': True,
            'answer': final_state.get('final_answer', 'No answer generated'),
            'sql_query': final_state.get('draft_sql_query', ''),
            'data': final_state.get('query_result', {}).get('data'),
            'error': final_state.get('error', ''),
            'iterations': final_state.get('iteration', 0)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'answer': f"Error: {str(e)}"
        }


def display_result(result):
    """Display query results in a nice format."""
    if not result:
        return
    
    # Display answer
    st.markdown("### <i class='fas fa-comment-dots'></i> Answer", unsafe_allow_html=True)
    if result.get('success'):
        st.markdown(f"<div style='background-color: #28a745; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #28a745;'><i class='fas fa-check-circle' style='color: #28a745;'></i> {result['answer']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color: #f8d7da; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #dc3545;'><i class='fas fa-times-circle' style='color: #dc3545;'></i> {result['answer']}</div>", unsafe_allow_html=True)
    
    # Display SQL query
    if result.get('sql_query'):
        st.markdown("### <i class='fas fa-code'></i> Generated SQL Query", unsafe_allow_html=True)
        st.code(result['sql_query'], language='sql')
        
        # Copy button
        st.button("📋 Copy SQL", key=f"copy_{datetime.now().timestamp()}")
    
    # Display data if available
    if result.get('data') is not None and not result['data'].empty:
        st.markdown("### <i class='fas fa-chart-bar'></i> Query Results", unsafe_allow_html=True)
        
        # Show data in tabs with icons
        tab1, tab2, tab3 = st.tabs(["📋 Table View", "📈 Visualize", "� Export"])
        
        with tab1:
            st.dataframe(
                result['data'],
                use_container_width=True,
                hide_index=False
            )
            
            # Show row count
            st.markdown(f"<p style='color: #666;'><i class='fas fa-info-circle'></i> Showing {len(result['data'])} row(s)</p>", unsafe_allow_html=True)
        
        with tab2:
            # Auto-detect numeric columns for visualization
            numeric_cols = result['data'].select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            if len(numeric_cols) > 0:
                # Let user choose visualization type
                viz_type = st.selectbox(
                    "Select visualization type:",
                    ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot"]
                )
                
                if len(result['data'].columns) >= 2:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        x_axis = st.selectbox("X-axis:", result['data'].columns.tolist())
                    
                    with col2:
                        y_options = [col for col in result['data'].columns if col != x_axis]
                        if y_options:
                            y_axis = st.selectbox("Y-axis:", y_options)
                        else:
                            y_axis = result['data'].columns[0]
                    
                    # Create visualization
                    try:
                        if viz_type == "Bar Chart":
                            fig = px.bar(result['data'], x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
                        elif viz_type == "Line Chart":
                            fig = px.line(result['data'], x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
                        elif viz_type == "Pie Chart":
                            fig = px.pie(result['data'], names=x_axis, values=y_axis, title=f"{y_axis} distribution")
                        else:  # Scatter Plot
                            fig = px.scatter(result['data'], x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                        
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Could not create visualization: {str(e)}")
                else:
                    st.info("Need at least 2 columns for visualization")
            else:
                st.info("No numeric columns available for visualization")
        
        with tab3:
            # Export options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv = result['data'].to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                json_str = result['data'].to_json(orient='records', indent=2)
                st.download_button(
                    label="⬇️ Download JSON",
                    data=json_str,
                    file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col3:
                # Excel download would require openpyxl
                st.markdown("<p style='color: #0066cc;'><i class='fas fa-info-circle'></i> CSV and JSON formats available</p>", unsafe_allow_html=True)
    
    # Show metadata
    if result.get('iterations'):
        st.markdown(f"<p style='color: #666;'><i class='fas fa-sync-alt'></i> Query refined {result['iterations']} time(s)</p>", unsafe_allow_html=True)


def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Header with icon
    st.markdown('''
        <div class="main-header">
            <i class="fas fa-robot" style="color: #1f77b4;"></i> SQL Agent
        </div>
    ''', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Natural Language to SQL Query System</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('''
            <div style="text-align: center; padding: 1rem;">
                <i class="fas fa-robot" style="font-size: 64px; color: #1f77b4;"></i>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown("### <i class='fas fa-cog'></i> Settings", unsafe_allow_html=True)
        
        # API Key Status
        if check_api_key():
            st.markdown("<p style='color: green;'><i class='fas fa-check-circle'></i> API Key Configured</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: red;'><i class='fas fa-times-circle'></i> API Key Missing</p>", unsafe_allow_html=True)
            st.markdown("<p style='color: orange;'><i class='fas fa-exclamation-triangle'></i> Please add GOOGLE_API_KEY to your .env file</p>", unsafe_allow_html=True)
            st.code("GOOGLE_API_KEY=your-key-here")
            st.markdown("<p style='color: #0066cc;'><i class='fas fa-info-circle'></i> Get your key from: https://aistudio.google.com/app/apikey</p>", unsafe_allow_html=True)
        
        st.divider()
        
        # Database selection
        st.markdown("### <i class='fas fa-database'></i> Database", unsafe_allow_html=True)
        db_path = st.text_input(
            "Database Path:",
            value="database/test_db.sqlite",
            help="Path to your SQLite database file"
        )
        
        if os.path.exists(db_path):
            st.markdown("<p style='color: green;'><i class='fas fa-check-circle'></i> Database found</p>", unsafe_allow_html=True)
            
            # Show database stats
            import sqlite3
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                st.markdown(f"<p style='color: #0066cc;'><i class='fas fa-table'></i> {len(tables)} table(s) found</p>", unsafe_allow_html=True)
                
                with st.expander("🔍 View Tables"):
                    for table in tables:
                        st.markdown(f"<i class='fas fa-table'></i> {table[0]}", unsafe_allow_html=True)
                
                conn.close()
            except Exception as e:
                st.markdown(f"<p style='color: red;'><i class='fas fa-exclamation-circle'></i> Error reading database: {str(e)}</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: red;'><i class='fas fa-times-circle'></i> Database not found</p>", unsafe_allow_html=True)
        
        st.divider()
        
        # Example queries
        st.markdown("### <i class='fas fa-lightbulb'></i> Example Questions", unsafe_allow_html=True)
        example_queries = [
            "How many employees are there?",
            "What is the average salary by department?",
            "Show me the top 5 highest paid employees",
            "Which products are low in stock?",
            "What were the total sales in November 2024?",
            "List all customers who placed more than 3 orders",
            "Show me unresolved customer support tickets",
            "What is the most popular product category?"
        ]
        
        for i, query in enumerate(example_queries[:5]):
            if st.button(f"💬 {query}", key=f"example_{i}", use_container_width=True):
                st.session_state.current_question = query
                st.session_state.run_query = True
                st.rerun()
        
        st.divider()
        
        # Query history
        if st.session_state.query_history:
            st.markdown("### <i class='fas fa-history'></i> Recent Queries", unsafe_allow_html=True)
            with st.expander(f"View History ({len(st.session_state.query_history)})"):
                for i, hist in enumerate(reversed(st.session_state.query_history[-5:])):
                    status_icon = "<i class='fas fa-check-circle' style='color: green;'></i>" if hist.get('success') else "<i class='fas fa-times-circle' style='color: red;'></i>"
                    st.markdown(f"{status_icon} {i+1}. {hist['question'][:50]}...", unsafe_allow_html=True)
            
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.query_history = []
                st.rerun()
    
    # Main content area
    if not check_api_key():
        st.markdown("<p style='color: red; font-size: 1.2rem;'><i class='fas fa-exclamation-triangle'></i> Please configure your GOOGLE_API_KEY in the .env file to use the SQL Agent.</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #0066cc;'><i class='fas fa-info-circle'></i> See the sidebar for instructions.</p>", unsafe_allow_html=True)
        return
    
    # Query input
    st.markdown("### <i class='fas fa-comment-dots'></i> Ask Your Question", unsafe_allow_html=True)
    
    # Use session state for the question if set by example button
    default_question = st.session_state.get('current_question', '')
    
    question = st.text_area(
        "Enter your question in natural language:",
        value=default_question,
        height=100,
        placeholder="e.g., How many employees work in the Engineering department?",
        help="Ask anything about your database in plain English"
    )
    
    # Clear the current_question after using it
    if 'current_question' in st.session_state:
        del st.session_state.current_question
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        run_button = st.button("▶️ Run Query", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🔄 Clear", use_container_width=True)
    
    if clear_button:
        st.session_state.current_result = None
        if 'run_query' in st.session_state:
            del st.session_state.run_query
        st.rerun()
    
    # Check if we should auto-run the query (from example button)
    auto_run = st.session_state.get('run_query', False)
    if auto_run:
        st.session_state.run_query = False  # Clear the flag
    
    # Run query
    if (run_button or auto_run) and question.strip():
        result = run_query(question, db_path)
        st.session_state.current_result = result
        
        # Add to history
        st.session_state.query_history.append({
            'question': question,
            'timestamp': datetime.now().isoformat(),
            'success': result.get('success', False)
        })
    
    # Display current result
    if st.session_state.current_result:
        st.divider()
        display_result(st.session_state.current_result)
    
    # Footer
    st.divider()
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 2rem;'>
            <p>
                <i class="fas fa-robot" style="color: #1f77b4;"></i> 
                Powered by Google Gemini 2.5 Flash | 
                <i class="fas fa-code-branch"></i> Built with LangGraph & Streamlit
            </p>
            <p style='font-size: 0.8rem;'>
                <i class="fas fa-shield-alt" style="color: #28a745;"></i> 
                Safe SQL execution with multi-layer safety checks
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
