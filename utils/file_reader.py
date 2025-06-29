import os
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path
import dotenv

dotenv.load_dotenv()

# Base directory where our data lives
DATA_DIR = Path(__file__).resolve().parent.parent


def read_csv_summary(filename: str) -> str:
    """
    Read a CSV file and return a simple summary.
    Args:
        filename: Name of the CSV file (e.g. 'sample.csv')
    Returns:
        A string describing the file's contents.
    """
    file_path = DATA_DIR / filename
    df = pd.read_csv(file_path)
    result = f"CSV file '{filename}' has {len(df)} rows and {len(df.columns)} columns."
    print(result)
    return result


def read_parquet_summary(filename: str) -> str:
    """
    Read a Parquet file and return a simple summary.
    Args:
        filename: Name of the Parquet file (e.g. 'sample.parquet')
    Returns:
        A string describing the file's contents.
    """
    file_path = DATA_DIR / filename
    df = pd.read_parquet(file_path)
    result = f"Parquet file '{filename}' has {len(df)} rows and {len(df.columns)} columns."
    print(result)
    return result


def filter_csv_by_column_value(filename: str, column: str, value: str) -> str:
    """
    Filter a CSV file by a column value and return matching rows as a string.
    Args:
        filename: Name of the CSV file (e.g. 'sample.csv')
        column: Column name to filter on
        value: Value to match in the column
    Returns:
        A string with the filtered rows or a message if none found.
    """
    file_path = DATA_DIR / filename
    df = pd.read_csv(file_path)
    if column not in df.columns:
        return f"Column '{column}' not found in CSV."
    filtered = df[df[column] == value]
    if filtered.empty:
        return f"No rows found where {column} == {value}."
    return filtered.to_csv(index=False)


def extract_csv_column(filename: str, column: str) -> str:
    """
    Extract a column from a CSV file and return its values as a string.
    Args:
        filename: Name of the CSV file (e.g. 'sample.csv')
        column: Column name to extract
    Returns:
        A string with the column values or a message if not found.
    """
    file_path = DATA_DIR / filename
    df = pd.read_csv(file_path)
    if column not in df.columns:
        return f"Column '{column}' not found in CSV."
    return '\n'.join(map(str, df[column].tolist()))


def get_pg_connection():
    """
    Returns a psycopg2 connection using environment variables.
    """
    return psycopg2.connect(
        host=os.getenv('PGHOST', 'localhost'),
        port=os.getenv('PGPORT', '5432'),
        user=os.getenv('PGUSER', 'postgres'),
        password=os.getenv('PGPASSWORD', 'postgres'),
        dbname=os.getenv('PGDATABASE', 'postgres')
    )


def get_pg_engine():
    """
    Returns a SQLAlchemy engine for pandas .to_sql
    """
    user = os.getenv('PGUSER', 'postgres')
    password = os.getenv('PGPASSWORD', 'postgres')
    host = os.getenv('PGHOST', 'localhost')
    port = os.getenv('PGPORT', '5432')
    db = os.getenv('PGDATABASE', 'postgres')
    return create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')


def load_csv_to_postgres(filename: str, table_name: str = "csv_table") -> str:
    """
    Load a CSV file into a PostgreSQL table.
    """
    file_path = DATA_DIR / filename
    df = pd.read_csv(file_path)
    engine = get_pg_engine()
    try:
        df.to_sql(table_name, engine, index=False, if_exists='replace')
        return f"Loaded {filename} into PostgreSQL table '{table_name}'."
    except Exception as e:
        return f"Error loading CSV to PostgreSQL: {e}"


def load_parquet_to_postgres(filename: str, table_name: str = "parquet_table") -> str:
    """
    Load a Parquet file into a PostgreSQL table.
    """
    file_path = DATA_DIR / filename
    df = pd.read_parquet(file_path)
    engine = get_pg_engine()
    try:
        df.to_sql(table_name, engine, index=False, if_exists='replace')
        return f"Loaded {filename} into PostgreSQL table '{table_name}'."
    except Exception as e:
        return f"Error loading Parquet to PostgreSQL: {e}"


# Simple CRUD functions for PostgreSQL
def postgres_crud(operation: str, table_name: str, data: dict = None, filters: dict = None) -> str:
    """
    Perform CRUD operations on a PostgreSQL table.
    Args:
        operation: 'create', 'read', 'update', 'delete'
        table_name: Name of the table
        data: Data for create/update (dict)
        filters: Filters for read/update/delete (dict)
    Returns:
        Query result or status message.
    """
    conn = get_pg_connection()
    cur = conn.cursor()
    try:
        if operation == 'create':
            # Insert a row
            keys = ', '.join(data.keys())
            qmarks = ', '.join(['%s'] * len(data))
            sql = f"INSERT INTO {table_name} ({keys}) VALUES ({qmarks})"
            cur.execute(sql, tuple(data.values()))
            conn.commit()
            return "Row inserted."
        elif operation == 'read':
            sql = f"SELECT * FROM {table_name}"
            vals = []
            if filters:
                where = ' AND '.join([f"{k}=%s" for k in filters.keys()])
                sql += f" WHERE {where}"
                vals = list(filters.values())
            cur.execute(sql, vals)
            rows = cur.fetchall()
            return str(rows)
        elif operation == 'update':
            set_clause = ', '.join([f"{k}=%s" for k in data.keys()])
            sql = f"UPDATE {table_name} SET {set_clause}"
            vals = list(data.values())
            if filters:
                where = ' AND '.join([f"{k}=%s" for k in filters.keys()])
                sql += f" WHERE {where}"
                vals += list(filters.values())
            cur.execute(sql, vals)
            conn.commit()
            return f"{cur.rowcount} row(s) updated."
        elif operation == 'delete':
            sql = f"DELETE FROM {table_name}"
            vals = []
            if filters:
                where = ' AND '.join([f"{k}=%s" for k in filters.keys()])
                sql += f" WHERE {where}"
                vals = list(filters.values())
            cur.execute(sql, vals)
            conn.commit()
            return f"{cur.rowcount} row(s) deleted."
        else:
            return "Invalid operation."
    except Exception as e:
        return f"PostgreSQL error: {e}"
    finally:
        cur.close()
        conn.close()
