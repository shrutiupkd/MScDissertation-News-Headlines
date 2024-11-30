import pandas as pd
import sqlite3

file_path = 'monthlyvaccinationrates202106.xlsx'  # Excel file path
df = pd.read_excel(file_path)  # Use read_excel to read Excel file

conn = sqlite3.connect('vaccine.db')  # Create a database connection
cursor = conn.cursor()

table_name = 'vaccines'  # Define the table name
df.to_sql(table_name, conn, if_exists='replace', index=False)  # Store DataFrame in the database

conn.commit()
conn.close()

print(f"Data from {file_path} has been stored in {table_name} table of vaccine.db")
