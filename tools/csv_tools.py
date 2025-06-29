from server import mcp
from utils.file_reader import (
    read_csv_summary,
    filter_csv_by_column_value,
    extract_csv_column,
    load_csv_to_postgres,
    postgres_crud,
)


@mcp.tool()
def summarize_csv_file(filename: str) -> str:
    """
    Summarizes the contents of a CSV file.

    Args:
        filename (str): The path to the CSV file.

    Returns:
        str: A summary of the CSV file.
    """
    try:
        summary = read_csv_summary(filename)
        return summary
    except Exception as e:
        return f"Error reading CSV file: {e}"


@mcp.tool()
def filter_csv_by_column_value_tool(filename: str, column: str, value: str) -> str:
    """
    Filters a CSV file by a column value and returns matching rows as CSV string.

    Args:
        filename (str): The path to the CSV file.
        column (str): The column name to filter on.
        value (str): The value to match in the column.

    Returns:
        str: Filtered rows as CSV or a message if none found.
    """
    try:
        return filter_csv_by_column_value(filename, column, value)
    except Exception as e:
        return f"Error filtering CSV file: {e}"


@mcp.tool()
def extract_csv_column_tool(filename: str, column: str) -> str:
    """
    Extracts a column from a CSV file and returns its values as a string.

    Args:
        filename (str): The path to the CSV file.
        column (str): The column name to extract.

    Returns:
        str: The column values or a message if not found.
    """
    try:
        return extract_csv_column(filename, column)
    except Exception as e:
        return f"Error extracting column from CSV file: {e}"


@mcp.tool()
def load_csv_to_postgres_tool(filename: str, table_name: str = "csv_table") -> str:
    """
    Loads a CSV file into a PostgreSQL table.

    Args:
        filename (str): The path to the CSV file.
        table_name (str): The name of the table to create.

    Returns:
        str: Success message or error.
    """
    try:
        return load_csv_to_postgres(filename, table_name)
    except Exception as e:
        return f"Error loading CSV to PostgreSQL: {e}"


@mcp.tool()
def postgres_crud_tool(operation: str, table_name: str, data: dict = None, filters: dict = None) -> str:
    """
    Perform CRUD operations on a PostgreSQL table.

    Args:
        operation (str): 'create', 'read', 'update', 'delete'
        table_name (str): Name of the table
        data (dict): Data for create/update
        filters (dict): Filters for read/update/delete

    Returns:
        str: Query result or status message.
    """
    try:
        return postgres_crud(operation, table_name, data, filters)
    except Exception as e:
        return f"Error in PostgreSQL CRUD: {e}"
