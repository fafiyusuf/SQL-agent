# SQL Agent - Quick Start Guide

## 🎯 What You've Built

A complete SQL agent that:
- ✅ Converts natural language to SQL queries
- ✅ Validates query safety with multi-layer checks
- ✅ Executes approved queries on SQLite databases
- ✅ Returns human-readable answers
- ✅ Automatically refines unsafe queries

## 📊 Architecture Overview

```
User Question → Schema Extractor → Query Generator (GPT-4) 
                                          ↓
                                    Safety Check
                                    ↙        ↘
                            [Safe]              [Unsafe]
                             ↓                     ↓
                        Execution           ← Refine Query
                             ↓
                        Summary (GPT-4)
                             ↓
                     Human Answer
```

## 🚀 Getting Started

### 1. Install Dependencies (Already Done!)

```bash
cd /home/newuser/codingFolders/sql_agent_project
source env/bin/activate  # or: . env/bin/activate
pip install -r requirements.txt
```

### 2. Set Up Your OpenAI API Key

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your key
nano .env  # or use your preferred editor
```

Your `.env` should look like:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### 3. Run Tests (No API Key Needed!)

```bash
python test.py
```

This verifies:
- Database connection works
- Safety checks function correctly
- Query execution works
- Workflow logic is sound

### 4. Run Demo (Requires API Key)

```bash
python demo.py
```

Runs through 3 example questions to show the full agent in action.

### 5. Interactive Mode (Requires API Key)

```bash
python main.py
```

Ask your own questions in a chat-like interface!

## 💡 Example Questions to Try

### Employee Analysis
- "How many employees work in each department?"
- "Who are the top 5 highest paid employees?"
- "What's the average salary in the Engineering department?"
- "Show me all employees hired after 2020"

### Department Insights
- "Which department has the largest budget?"
- "What is the total budget across all departments?"
- "List all departments with their manager IDs"

### Aggregations & Statistics
- "What's the salary range for each department?"
- "How many employees were hired in 2021?"
- "Calculate the total payroll cost"

## 🛡️ Safety Features Explained

### Code-Based Checks
The system blocks these SQL operations:
- `DROP` - Deleting tables
- `DELETE` - Removing rows
- `UPDATE` - Modifying data
- `INSERT` - Adding data
- `ALTER` - Changing structure
- `TRUNCATE` - Clearing tables
- `CREATE` - Making new objects

### LLM-Based Verification
After code checks pass, GPT-4 performs semantic analysis:
- Verifies query intent matches user question
- Detects potential SQL injection attempts
- Ensures no privilege escalation
- Validates query follows best practices

### Refinement Loop
If a query fails safety checks:
1. Feedback is sent back to Query Generator
2. LLM generates a new, safer query
3. Process repeats (max 3 attempts)
4. If still unsafe, returns error to user

## 📁 File Structure Explained

```
sql_agent_project/
├── main.py                    # Main application & workflow orchestration
├── demo.py                    # Automated demo script
├── test.py                    # Unit tests (no API key needed)
├── requirements.txt           # Python dependencies
├── .env.example              # API key template
├── .env                      # Your API key (create this!)
├── README.md                 # Full documentation
├── QUICKSTART.md             # This file
│
├── database/
│   └── test_db.sqlite        # Sample database with employees & departments
│
└── nodes/                    # LangGraph nodes
    ├── query_generator.py    # LLM: Natural language → SQL
    ├── safety_check.py       # Validates query safety
    ├── execution_node.py     # Executes approved queries
    ├── summary_node.py       # LLM: Results → Human answer
    └── tools_node.py         # Database utility functions
```

## 🔧 Using Your Own Database

### Option 1: Replace the Sample Database

```python
# In your code
from main import run_sql_agent

result = run_sql_agent(
    question="Your question here",
    db_path="path/to/your/database.sqlite"
)
```

### Option 2: Modify main.py

Change the default database path:
```python
# In main.py, line ~265
db_path = "database/your_custom_db.sqlite"
```

## 🎨 Customization Options

### Change LLM Model

In `nodes/query_generator.py`, `nodes/safety_check.py`, and `nodes/summary_node.py`:
```python
llm = ChatOpenAI(model="gpt-4", temperature=0)  # Use GPT-4 instead
# or
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)  # Cheaper option
```

### Adjust Max Iterations

```python
run_sql_agent(
    question="Your question",
    db_path="database/test_db.sqlite",
    max_iterations=5  # Default is 3
)
```

### Add Custom Safety Rules

In `nodes/safety_check.py`, add to the `destructive_commands` list:
```python
destructive_commands = [
    "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", 
    "TRUNCATE", "REPLACE", "CREATE", "GRANT", "REVOKE",
    "YOUR_CUSTOM_COMMAND"  # Add here
]
```

## 📊 Sample Database Schema

### employees table
| Column     | Type    | Description              |
|------------|---------|--------------------------|
| id         | INTEGER | Primary key              |
| name       | TEXT    | Employee name            |
| department | TEXT    | Department name          |
| salary     | REAL    | Annual salary            |
| hire_date  | TEXT    | Date hired (YYYY-MM-DD)  |

8 rows of sample data

### departments table
| Column      | Type    | Description              |
|-------------|---------|--------------------------|
| id          | INTEGER | Primary key              |
| name        | TEXT    | Department name          |
| budget      | REAL    | Annual budget            |
| manager_id  | INTEGER | Employee ID of manager   |

3 rows of sample data

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Create `.env` file in project root
- Add: `OPENAI_API_KEY=your-key-here`
- No quotes needed around the key

### "No such table" errors
- Verify database path is correct
- Run `python test.py` to check database setup
- Try reinitializing: delete `database/test_db.sqlite` and run again

### "Safety check failed after maximum iterations"
- Your question might be too vague
- Try being more specific
- Check if you're asking for destructive operations
- Increase max_iterations parameter

### Import errors
- Activate virtual environment: `source env/bin/activate`
- Reinstall packages: `pip install -r requirements.txt`

## 📈 Next Steps

### 1. Extend to Other Databases
- Add PostgreSQL support
- Add MySQL support
- Add MongoDB support (NoSQL)

### 2. Add Visualization
- Generate charts from query results
- Use matplotlib or plotly
- Return images in responses

### 3. Query Caching
- Cache frequent queries
- Speed up repeated questions
- Reduce API costs

### 4. Multi-Database Support
- Query across multiple databases
- Join data from different sources
- Aggregate cross-database insights

### 5. Advanced Features
- Query explanation mode
- Query optimization suggestions
- Database performance monitoring
- Automatic indexing recommendations

## 📚 Learning Resources

### LangGraph
- Official docs: https://langchain-ai.github.io/langgraph/
- Tutorial: Building stateful agents

### LangChain
- Official docs: https://python.langchain.com/
- LLM integration patterns

### SQL Best Practices
- SQL query optimization
- Database design principles
- Security in SQL applications

## 🤝 Contributing Ideas

Want to improve this project? Ideas:
- [ ] Add support for multiple LLM providers (Anthropic, Cohere)
- [ ] Implement query history and learning
- [ ] Add natural language query explanation
- [ ] Create web UI (Streamlit/Gradio)
- [ ] Add voice input support
- [ ] Implement query templates
- [ ] Add data export options (CSV, Excel, JSON)

## 💰 Cost Considerations

### Using GPT-4o-mini (Current Setup)
- ~$0.15 per 1M input tokens
- ~$0.60 per 1M output tokens
- Average query: ~$0.001-0.005

### Typical Usage Costs
- 100 questions: ~$0.10-0.50
- 1000 questions: ~$1-5
- Very affordable for development!

## ✨ Key Features Recap

✅ **Natural Language Interface** - Ask questions like a human
✅ **Multi-Layer Safety** - Code + LLM verification
✅ **Automatic Refinement** - Self-corrects unsafe queries
✅ **Human-Readable Answers** - No raw SQL dumps
✅ **Interactive & Programmatic** - CLI and Python API
✅ **Extensible Architecture** - Easy to customize
✅ **Production-Ready** - Error handling, logging, testing

---

**Ready to start?** Run `python test.py` to verify everything works!

**Need help?** Check the full README.md for detailed documentation.

**Have fun exploring your data! 🚀**
