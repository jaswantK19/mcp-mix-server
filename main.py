from server import mcp
import dotenv

dotenv.load_dotenv()

import tools.csv_tools
import tools.parquet_tools


if __name__ == "__main__":
    mcp.run()
