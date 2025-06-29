from server import mcp
from utils.file_reader import read_parquet_summary


@mcp.tool()
def summarize_parquet_file(filename: str) -> str:
    """
    Summarizes the contents of a Parquet file.

    Args:
        filename (str): The path to the Parquet file.

    Returns:
        str: A summary of the Parquet file.
    """
    try:
        summary = read_parquet_summary(filename)
        return summary
    except Exception as e:
        return f"Error reading Parquet file: {e}"
