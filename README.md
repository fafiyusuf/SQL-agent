# SQL Agent - Natural Language to SQL Query System

A sophisticated SQL agent that converts natural language questions into SQL queries with safety checks and human-readable results. Built with LangGraph and Google Gemini (or OpenAI).

## 🎯 Features

- **Natural Language Understanding**: Ask questions in plain English
- **Schema-Aware Query Generation**: Automatically learns your database structure
- **Multi-Layer Safety Checks**: Code-based + LLM-based verification
- **Query Refinement Loop**: Automatically refines unsafe queries
- **Human-Readable Results**: Converts data into conversational answers
- **Interactive Mode**: Chat-like interface for database exploration
- **Flexible LLM Support**: Works with Google Gemini 2.5 Flash or OpenAI GPT-4

## 🏗️ Architecture

The system uses a LangGraph workflow with the following nodes:

### 1. **Schema Extractor Node**
- Extracts database schema (tables, columns, types)
- Provides context for query generation

### 2. **Query Generator Node** (LLM)
- Converts natural language to SQL
- Uses Google Gemini 2.5 Flash (or GPT-4) to understand intent
- Schema-aware query construction

### 3. **Safety Check Node** (LLM + Code)
- **Code-based checks**: Blocks DROP, DELETE, UPDATE, etc.
- **LLM verification**: Semantic safety analysis
- **Refinement loop**: Up to 3 attempts to generate safe queries

### 4. **Execution Node**
- Executes approved SQL queries
- Returns structured results with pandas
- Error handling and reporting

### 5. **Summary Node** (LLM)
- Converts query results to natural language
- Highlights key insights
- Provides conversational answers

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. **Clone or navigate to the project directory**:
```bash
cd sql_agent_project
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up your OpenAI API key**:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Running the Agent

**Interactive Mode** (recommended):
```bash
python main.py
```

**Programmatic Usage**:
```python
from main import run_sql_agent

# Ask a question
result = run_sql_agent(
    question="How many employees are in Engineering?",
    db_path="database/test_db.sqlite"
)

print(result['final_answer'])
```

## 📊 Example Database

The project includes a sample SQLite database with:

### Tables

**employees**
- id (INTEGER PRIMARY KEY)
- name (TEXT)
- department (TEXT)
- salary (REAL)
- hire_date (TEXT)

**departments**
- id (INTEGER PRIMARY KEY)
- name (TEXT)
- budget (REAL)
- manager_id (INTEGER)

### Sample Questions

1. "How many employees work in the Engineering department?"
2. "What is the average salary by department?"
3. "Who are the top 3 highest paid employees?"
4. "Show me all employees hired after 2020"
5. "What is the total budget across all departments?"

## 🔒 Safety Features

### Code-Based Safety Checks
- Blocks all destructive operations (DROP, DELETE, UPDATE, INSERT, ALTER, etc.)
- Ensures queries start with SELECT
- Regex-based pattern matching with word boundaries

### LLM-Based Safety Verification
- Semantic analysis of query intent
- Detects potential exploits or unusual patterns
- Provides feedback for refinement

### Refinement Loop
- Maximum 3 attempts to generate a safe query
- Provides specific feedback for each failure
- Prevents infinite loops with iteration limits

## 🛠️ Configuration

### Environment Variables

Create a `.env` file with your API key:

**Using Google Gemini (Recommended - Free tier available)**:
```env
GOOGLE_API_KEY=your-google-api-key-here
```
Get your key from: https://aistudio.google.com/app/apikey

**Or using OpenAI**:
```env
OPENAI_API_KEY=your-openai-api-key-here
```
Get your key from: https://platform.openai.com/api-keys

**Need to switch providers?** See [MIGRATION_GEMINI.md](MIGRATION_GEMINI.md) for migration guide.

### Workflow Parameters

Adjust in `main.py`:
```python
run_sql_agent(
    question="Your question here",
    db_path="path/to/database.sqlite",
    max_iterations=3  # Maximum refinement attempts
)
```

## 📁 Project Structure

```
sql_agent_project/
├── main.py                    # Main application and workflow
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variable template
├── README.md                 # This file
├── database/
│   └── test_db.sqlite        # Sample database
└── nodes/
    ├── query_generator.py    # LLM-based query generation
    ├── safety_check.py       # Safety verification
    ├── execution_node.py     # Query execution
    ├── summary_node.py       # Result summarization
    └── tools_node.py         # Database utility tools
```

## 🔄 Workflow Diagram

```
┌─────────────────┐
│  User Question  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Get Schema     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Query Generator │◄────┐
└────────┬────────┘     │
         │              │
         ▼              │
┌─────────────────┐     │
│  Safety Check   │     │
└────────┬────────┘     │
         │              │
    Safe │ Unsafe       │
         ▼              │
┌─────────────────┐     │
│   Execution     │     │ Refine
└────────┬────────┘     │
         │              │
         ▼              │
┌─────────────────┐     │
│    Summary      │─────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Final Answer   │
└─────────────────┘
```

## 🧪 Testing with Custom Databases

To use your own database:

1. Place your `.sqlite` file in the `database/` directory
2. Update the `db_path` parameter:
```python
run_sql_agent(
    question="Your question",
    db_path="database/your_database.sqlite"
)
```

## 📝 Notes

- **Read-Only**: The system only allows SELECT queries for safety
- **SQLite**: Currently supports SQLite databases
- **LLM Model**: Uses Google Gemini 2.5 Flash (or GPT-4o-mini) for cost efficiency
- **Iteration Limit**: Maximum 3 refinement attempts to prevent loops

## 🚨 Troubleshooting

### "API key not found" / "GOOGLE_API_KEY not found"
Create a `.env` file with your API key:
```bash
# For Gemini (recommended)
echo "GOOGLE_API_KEY=your-key-here" > .env

# For OpenAI (alternative)
echo "OPENAI_API_KEY=your-key-here" > .env
```

### Rate Limit Errors
If you're hitting OpenAI rate limits:
1. Consider switching to Google Gemini (better free tier)
2. See [MIGRATION_GEMINI.md](MIGRATION_GEMINI.md) for migration guide
3. Or run: `./setup_gemini.sh` for automated setup

### "No such table" errors
Ensure your database path is correct and tables exist:
```python
import sqlite3
conn = sqlite3.connect("database/test_db.sqlite")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
```

### Safety check failures
The system may take 2-3 iterations to generate a safe query. This is normal behavior.

## 🤝 Contributing

Feel free to extend the system:
- Add support for other databases (PostgreSQL, MySQL)
- Implement query caching
- Add visualization capabilities
- Extend safety rules

## 📄 License

MIT License - Feel free to use this project for learning and development!

## 🙏 Acknowledgments

Built with:
- [LangGraph](https://github.com/langchain-ai/langgraph) - Workflow orchestration
- [LangChain](https://github.com/langchain-ai/langchain) - LLM framework
- [OpenAI](https://openai.com/) - Language models
- [pandas](https://pandas.pydata.org/) - Data manipulation
