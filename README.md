# Mix Server

A Python-based data server for working with CSV and Parquet files, featuring:
- Data summarization
- Column extraction
- Row filtering
- Loading data into PostgreSQL
- Full CRUD operations via API/tools

## Features
- Summarize CSV and Parquet files
- Extract columns or filter rows by value
- Load data into a PostgreSQL database (Dockerized)
- Perform CRUD operations on database tables
- Easily extensible with new tools

## Getting Started

### Prerequisites
- Python 3.11+
- Docker (for PostgreSQL)
- [uv](https://github.com/astral-sh/uv) (for dependency management)
- [GitHub CLI](https://cli.github.com/) (optional, for repo management)

### Setup
1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd mix-server
   ```
2. **Install dependencies:**
   ```sh
   uv pip compile pyproject.toml > requirements.txt
   pip install -r requirements.txt
   ```
3. **Start PostgreSQL (Docker):**
   ```sh
   make start-postgres
   ```
4. **Configure environment:**
   - Edit `.env` if needed (default credentials are set for local Docker Postgres)

5. **Run the server:**
   ```sh
   python main.py
   ```

### Docker
To build and run the server in Docker:
```sh
docker build -t mix-server .
docker run --env-file .env -p 8000:8000 mix-server
```

## Project Structure
```
.
├── data/                # Sample data files (CSV, Parquet)
├── tools/               # Tool modules for CSV/Parquet/DB
├── utils/               # Utility functions (file reading, DB, etc.)
├── main.py              # Entry point
├── server.py            # MCP server setup
├── pyproject.toml       # Python project config
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker build file
├── Makefile             # Automation commands
├── .env                 # Environment variables
└── .gitignore           # Git ignore rules
```

## Usage Examples
- Summarize a CSV file:
  ```python
  summarize_csv_file('data/sample.csv')
  ```
- Load CSV to PostgreSQL:
  ```python
  load_csv_to_postgres('data/sample.csv', 'sample_table')
  ```
- CRUD on DB:
  ```python
  postgres_crud('read', 'sample_table')
  ```

## Using MCP Servers with Clients (VS Code, Claude Desktop, etc.)

### VS Code
To connect your MCP server to VS Code:
1. Open VS Code.
2. Press `Cmd+,` (or go to Settings).
3. Search for `mcp` in the settings search bar.
4. Edit the settings to add the following snippet:

```json
"mcp": {
    "servers":{
        "mix_server": {
        "command": "uv",
        "args": [
            "--directory",
            "<ABSOLUTE PATH TO THE MCP SERVER DIR>/mix-server",
            "run",
            "main.py"
            ]
        }
    }
},

```

This will allow you to launch and connect to your local Mix Server MCP instance directly from VS Code.

### Claude Desktop or Other MCP Clients
- Add your MCP server endpoint or command in the client’s settings as per their documentation.
- Make sure your server is running and accessible (locally or via network).

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT
