import sqlite3

from crewai.tools import tool


# Connect to or create a local database file


# # Create the table if it doesn't exist
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS transactions (
#     transaction_id TEXT PRIMARY KEY,
#     account_id TEXT,
#     timestamp DATETIME,
#     amount REAL,
#     transaction_type TEXT,
#     status TEXT
# )
# ''')

# # Insert sample data
# cursor.execute('''
# INSERT INTO transactions (transaction_id, account_id, timestamp, amount, transaction_type, status)
# VALUES ('TXN1001', 'ACC5001', '2025-10-11 10:30:00', 250.75, 'debit', 'success')
# ''')

# cursor.execute('''
# INSERT INTO transactions (transaction_id, account_id, timestamp, amount, transaction_type, status)
# VALUES ('TXN1002', 'ACC5002', '2025-10-11 11:00:00', 1200.00, 'credit', 'pending')
# ''')

# # Commit changes
# 

# Fetch and print all transactions


# Close connection


@tool("sql_tool")
def sql_tool(sql_query: str) -> str:
    """Helper tool that will run the required sql query on the transaction database
    Args:
        sql_query (str): SQL query that needs to be run on the database.
    
    Returns:
        A dict that includes the results from the database
    """
    try:
        conn = sqlite3.connect('transactions.db')
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        return f"The database did not return results due to the following error: {e}"






