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

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT
