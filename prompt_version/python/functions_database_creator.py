import duckdb
import time as tm
from functions_basics import get_time
import pandas as pd
import re
import os

#---###---#

def sanitize_database_name(name):
    # Permite apenas letras, números e underlines
    sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    return sanitized_name

#---###---#

def create_database():
    # Define o caminho absoluto para a pasta 'EmiCore/database'
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database/local_databases'))
    os.makedirs(base_dir, exist_ok=True)

    database_name_input = input('Please, enter a name to your database: ').strip()
    database_name_input = sanitize_database_name(database_name_input)

    proceed_database_creation = input(f'The name set for your database is: {database_name_input}. Do you want to proceed? (Y/N)')

    if proceed_database_creation.strip().upper() == 'Y':
        try:
            tm.sleep(1)
            db_path = os.path.join(base_dir, f"{database_name_input}.db")
            conn = duckdb.connect(db_path, read_only=False)

            print(f"({get_time()}) | The database named {database_name_input} was created successfully at {db_path}")
            tm.sleep(1)
            print("")
            return conn

        except Exception as error:
            print(f"({get_time()}) | The function 'create_database' has returned an error: {error}")
            tm.sleep(1)
            print("")
            return None

    else:
        print(f"({get_time()}) #-# The creation of the database has been aborted.")
        print("")

#---###---#    

def create_table_from_sql_script(file_path_collected, conn_collected):
    """
    Function to execute an SQL script and create tables in the DuckDB database.
    """
    sql_script_path = file_path_collected

    try:
        # Open and read the SQL file
        with open(sql_script_path, "r", encoding="utf-8") as file:
            sql_script = file.read().strip()  # Removing extra spaces

        # Extract table name from CREATE TABLE statement
        match = re.search(r"^\s*CREATE\s+TABLE\s+([a-zA-Z0-9_]+)", sql_script, re.IGNORECASE)
        
        if match:
            table_name = match.group(1)  # Extracting table name
            print(f"\nScript content:\n{sql_script}\n")

            proceed_sql_script_execution = input("This SQL script will be executed. Do you want to proceed? (Y/N): ")

            if proceed_sql_script_execution.strip().upper() == "Y":
                conn_collected.execute(sql_script)

                # Verify if the table was created using DuckDB-specific metadata query
                result = conn_collected.execute(f"SELECT COUNT(*) FROM duckdb_tables() WHERE table_name = '{table_name}'").fetchone()

                if result and result[0] > 0:
                    print(f"({get_time()}) | Table '{table_name}' created successfully!")
                else:
                    print(f"({get_time()}) | Table '{table_name}' was not found in the database!")

                tm.sleep(1)
            else:
                print(f"({get_time()}) | Process aborted by the user.")
                tm.sleep(1)
        else:
            print(f"({get_time()}) | The SQL script must contain CREATE TABLE statements.")
            tm.sleep(1)

    except FileNotFoundError:
        print(f"({get_time()}) | Error: File '{sql_script_path}' not found.")
        tm.sleep(1)

    except Exception as error:
        print(f"({get_time()}) | Error executing SQL script: {error}")
        tm.sleep(1)
            
#---###---#            

def create_table_from_csv_file(file_path_collected, conn_collected):
    """
    Function to load a CSV file into a DuckDB table and verify its creation.
    """
    csv_file_path = file_path_collected

    try:
        # Load the CSV into a Pandas DataFrame
        df_csv_file = pd.read_csv(csv_file_path, sep=';')
        print(df_csv_file.head(5))  # Display the first five rows of the CSV file
        
        proceed_csv_file_execution = input("This CSV file converted to a pandas DataFrame will be created as a SQL table. Do you want to proceed? (Y/N): ")

        if proceed_csv_file_execution.strip().upper() == "Y":
            table_name = csv_file_path.replace(".csv", "").replace("-", "_").replace(" ", "_")  # Clean table name

            # Execute table creation from Pandas DataFrame
            conn_collected.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df_csv_file", df_csv_file)

            # Verify if the table was created in DuckDB
            result = conn_collected.execute(f"SELECT COUNT(*) FROM duckdb_tables() WHERE table_name = '{table_name}'").fetchone()

            if result and result[0] > 0:
                print(f"({get_time()}) | Table '{table_name}' created successfully from CSV!")
            else:
                print(f"({get_time()}) | Table '{table_name}' was not found in the database!")

            tm.sleep(1)
        else:
            print(f"({get_time()}) | Process aborted by the user.")
            tm.sleep(1)

    except FileNotFoundError:
        print(f"({get_time()}) | Error: File '{csv_file_path}' not found.")
        tm.sleep(1)

    except Exception as error:
        print(f"({get_time()}) | Error executing function 'create_table_from_csv_file': {error}")
        tm.sleep(1)
        
#---###---#

def read_sql_scripts():

    # Definir a pasta onde estão os arquivos SQL
    folder = "./database/sql_scripts/"

    # Obter lista de arquivos .sql
    sql_files = [f for f in os.listdir(folder) if f.endswith('.sql')]

    # Listar arquivos para o usuário
    print("Files Avalible:")
    for i, file in enumerate(sql_files, start=1):
        print(f"{i} - {file}")

    # Solicitar escolha do usuário
    selection = int(input("\nSelect the number from the file: "))

    while True:
        print("If you want exit from this step, press 0 \n")
        if 1 <= selection <= len(sql_files):
            file_path_selected = os.path.join(folder, sql_files[selection - 1])
            print(f"\nYou select: {file_path_selected}")
            return file_path_selected
        if selection == "0":
            print("Exiting from this step...")
            tm.sleep(1)
            break
        else:
            print("\nInvalid number, please, try again.")
        
#---###---#
        
def read_csv_files():
    
    folder = "./database/csv_files/"
    
    csv_files = [f for f in os.listdir(folder) if f.endswith('.csv')]
    
    print("Files Avalible:")
    for i, file in enumerate(csv_files, start=1):
        print(f"{i} - {file}")
        
    selection = int(input("\nSelect the number from the file: "))
    
    while True:
        print("If you want exit from this step, press 0 \n")
        if 1 <= selection <= len(csv_files):
            file_path_selected = os.path.join(folder, csv_files[selection - 1])
            print(f"\nYou select: {file_path_selected}")
            return file_path_selected
        if selection == "0":
            print("Exiting from this step...")
            tm.sleep(1)
            break
        else:
            print("\nInvalid number, please, try again.")
        
#---###---#

def create_custom_table(conn_collected):
    """
    Function to allow the user to create a table in DuckDB by typing the schema in the prompt.
    """
    print("\n=== CREATE YOUR TABLE ===")
    table_name = input("Enter the table name: ").strip().replace(" ", "_")  # Sanitize table name

    print("\nDefine your table columns (example: id INT PRIMARY KEY, name TEXT NOT NULL):")
    columns_structure = input("Enter column definitions: ").strip()

    if not table_name or not columns_structure:
        print("Invalid input! Table name and columns cannot be empty.")
        return

    # Constructing the SQL command
    sql_command = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_structure})"

    try:
        conn_collected.execute(sql_command)
        
        # Verify if the table was created in DuckDB
        result = conn_collected.execute(f"SELECT COUNT(*) FROM duckdb_tables() WHERE table_name = '{table_name}'").fetchone()

        if result and result[0] > 0:
            print(f"({get_time()}) | Table '{table_name}' created successfully!")
        else:
            print(f"({get_time()}) | Table '{table_name}' was not found in the database!")

        tm.sleep(1)

    except Exception as error:
        print(f"({get_time()}) | Error creating table: {error}")
        tm.sleep(1)
        
#---###---#

def create_table_from_console(conn_collected):
    """
    Provides an interactive SQL console for users to create tables easily.
    Default input starts with 'CREATE TABLE IF NOT EXISTS '.
    """
    default_command = "CREATE TABLE IF NOT EXISTS "
    user_input = input(default_command)

    full_sql = default_command + user_input

    # Check if user ended input correctly
    if full_sql.strip().endswith(";"):
        try:
            conn_collected.execute(full_sql)  # Usar a conexão passada, sem criar uma nova
            print(f"({get_time()}) | Table created successfully!")
        except Exception as e:
            print(f"({get_time()}) | Error executing SQL: {e}")
    else:
        print(f"({get_time()}) | Your SQL command must end with ';' to execute.")
        
#---###---#

def create_new_database_menu():
    
    try:
        conn_obtained = create_database()
        
    except ValueError as error:
        print(f"({get_time()}) | A database connection was not established: {error} | Exiting...")
        tm.sleep(1)
        return
    
    continue_input = input("Do you want to create tables in this new database? (Y/N): ")
    tm.sleep(1)
    
    if continue_input.strip().upper() == "Y":
        while True:
            type_of_create_tables_menu_input = input(
                "What you want to do about your new tables? \n" 
                "1 - Create my own table using console interaction; \n"
                "2 - Import Schema construction from a SQL Script (The script need to exist in the '/database/sql_scripts' folder); \n"
                "3 - Import Schema construction and data from a CSV File (The '.csv' file need to exist in the '/database/csv_files' folder); \n"
                "4 - Create my own table using format schema of 'CREATE TABLE' \n"
                "0 - Exit from this step \n\n"
                "-> "
            )
            
            if type_of_create_tables_menu_input == "1":
                create_custom_table(conn_collected=conn_obtained)
                
            if type_of_create_tables_menu_input == "2":
                sql_script_file_path_obtained = read_sql_scripts()
                create_table_from_sql_script(
                    file_path_collected=sql_script_file_path_obtained,
                    conn_collected=conn_obtained
                )
                
            if type_of_create_tables_menu_input == "3":
                csv_file_path_obtained = read_csv_files()
                create_table_from_csv_file(
                    file_path_collected=csv_file_path_obtained,
                    conn_collected=conn_obtained
                )

            if type_of_create_tables_menu_input == "4":
                create_table_from_console(conn_collected=conn_obtained)
            
            if type_of_create_tables_menu_input == "0":
                print("Exiting from this step...\n")
                tm.sleep(1)
                break