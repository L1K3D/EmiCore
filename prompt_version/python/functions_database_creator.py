"""
This module provides a set of functions to manage DuckDB databases with user interaction.

Features include:
- Creating and sanitizing database names.
- Creating new databases and managing their file locations.
- Creating tables from SQL scripts, CSV files, console input, or custom schema definitions.
- Listing and selecting SQL script or CSV files from predefined folders.
- Interactive menus guiding users through database and table creation processes.

The module relies on DuckDB for database operations, pandas for CSV handling,
and includes helpful prompts and validation to ensure smooth user experience.
"""

#---###---#

# Importing Libraries
import duckdb  # Library for executing SQL queries on DuckDB databases
import time as tm  # Standard Python time library, renamed as 'tm'
from functions_basics import get_time  # Custom function 'get_time' imported from another module
import pandas as pd  # Library for data manipulation and analysis using DataFrames
import re  # Library for working with regular expressions
import os  # Library for interacting with the operating system

#---###---#

# Function to sanitize the database name
def sanitize_database_name(name):
    # Removes unwanted characters from the database name to ensure safety and validity
    # Only allows letters (a-z, A-Z), numbers (0-9), and underscores (_)
    sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    
    # Returns the cleaned database name
    return sanitized_name

#---###---#

# Function to create the database
def create_database():
    # Defines the absolute path to the 'EmiCore/database/local_databases' folder
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database/local_databases'))
    
    # Creates the folder if it does not exist
    os.makedirs(base_dir, exist_ok=True)

    # Asks the user to input a database name and removes leading/trailing spaces
    database_name_input = input('Please, enter a name to your database: ').strip()
    
    # Sanitizes the database name to allow only letters, numbers, and underscores
    database_name_input = sanitize_database_name(database_name_input)

    # Asks the user to confirm the chosen database name
    proceed_database_creation = input(f'The name set for your database is: {database_name_input}. Do you want to proceed? (Y/N)')

    # Checks if the user confirmed database creation
    if proceed_database_creation.strip().upper() == 'Y':
        try:
            # Waits for 1 second before proceeding
            tm.sleep(1)
            
            # Defines the full path for the new database file
            db_path = os.path.join(base_dir, f"{database_name_input}.db")
            
            # Creates (or opens if already exists) the DuckDB database
            conn = duckdb.connect(db_path, read_only=False)

            # Prints a success message with timestamp
            print(f"({get_time()}) | The database named {database_name_input} was created successfully at {db_path}")
            
            # Waits for 1 second for better user experience
            tm.sleep(1)
            print("")
            return conn

        except Exception as error:
            # Prints an error message with timestamp if something goes wrong
            print(f"({get_time()}) | The function 'create_database' has returned an error: {error}")
            tm.sleep(1)
            print("")
            return None

    else:
        # Prints a message if the database creation was canceled by the user
        print(f"({get_time()}) #-# The creation of the database has been aborted.")
        print("")

#---###---#    

# Function to execute an SQL script and create tables in the DuckDB database
def create_table_from_sql_script(file_path_collected, conn_collected):
    sql_script_path = file_path_collected

    try:
        # Opens and reads the SQL script file
        with open(sql_script_path, "r", encoding="utf-8") as file:
            # Reads the file content and removes leading/trailing whitespace
            sql_script = file.read().strip()

        # Uses regex to extract the table name from the CREATE TABLE statement
        match = re.search(r"^\s*CREATE\s+TABLE\s+([a-zA-Z0-9_]+)", sql_script, re.IGNORECASE)
        
        if match:
            # Stores the extracted table name
            table_name = match.group(1)
            
            # Prints the content of the script to the console
            print(f"\nScript content:\n{sql_script}\n")

            # Asks the user if they want to proceed with executing the script
            proceed_sql_script_execution = input("This SQL script will be executed. Do you want to proceed? (Y/N): ")

            if proceed_sql_script_execution.strip().upper() == "Y":
                # Executes the SQL script in the DuckDB connection
                conn_collected.execute(sql_script)

                # Checks if the table was successfully created using DuckDB metadata
                result = conn_collected.execute(
                    f"SELECT COUNT(*) FROM duckdb_tables() WHERE table_name = '{table_name}'"
                ).fetchone()

                # If the result is greater than 0, the table exists
                if result and result[0] > 0:
                    print(f"({get_time()}) | Table '{table_name}' created successfully!")
                else:
                    print(f"({get_time()}) | Table '{table_name}' was not found in the database!")

                # Waits for 1 second before continuing
                tm.sleep(1)
            else:
                # Message when the user chooses to abort
                print(f"({get_time()}) | Process aborted by the user.")
                tm.sleep(1)
        else:
            # If no CREATE TABLE statement was found in the script
            print(f"({get_time()}) | The SQL script must contain CREATE TABLE statements.")
            tm.sleep(1)

    except FileNotFoundError:
        # Error message when the file does not exist
        print(f"({get_time()}) | Error: File '{sql_script_path}' not found.")
        tm.sleep(1)

    except Exception as error:
        # Generic error message for any unexpected exception during execution
        print(f"({get_time()}) | Error executing SQL script: {error}")
        tm.sleep(1)
            
#---###---#            

# Function to load a CSV file into a DuckDB table and verify its creation
def create_table_from_csv_file(file_path_collected, conn_collected):
    csv_file_path = file_path_collected

    try:
        # Loads the CSV file into a Pandas DataFrame using ';' as the separator
        df_csv_file = pd.read_csv(csv_file_path, sep=';')
        
        # Displays the first five rows of the DataFrame
        print(df_csv_file.head(5))
        
        # Displays information about the DataFrame (columns, data types, memory usage, etc.)
        print(df_csv_file.info())
        
        # Asks the user for confirmation before creating the table
        proceed_csv_file_execution = input(
            "This CSV file converted to a pandas DataFrame will be created as a SQL table. Do you want to proceed? (Y/N): "
        )

        if proceed_csv_file_execution.strip().upper() == "Y":
            # Generates the table name by removing '.csv' and replacing invalid characters with underscores
            table_name = csv_file_path.replace(".csv", "").replace("-", "_").replace(" ", "_")

            # Executes a SQL statement to create the table from the DataFrame (if it does not exist already)
            conn_collected.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df_csv_file", 
                df_csv_file
            )

            # Verifies if the table was successfully created using DuckDB's internal metadata
            result = conn_collected.execute(
                f"SELECT COUNT(*) FROM duckdb_tables() WHERE table_name = '{table_name}'"
            ).fetchone()

            if result and result[0] > 0:
                print(f"({get_time()}) | Table '{table_name}' created successfully from CSV!")
            else:
                print(f"({get_time()}) | Table '{table_name}' was not found in the database!")

            # Waits for 1 second for better UX
            tm.sleep(1)
        else:
            # Message when the user chooses not to proceed
            print(f"({get_time()}) | Process aborted by the user.")
            tm.sleep(1)

    except FileNotFoundError:
        # Error message when the CSV file is not found
        print(f"({get_time()}) | Error: File '{csv_file_path}' not found.")
        tm.sleep(1)

    except Exception as error:
        # Generic error message for unexpected exceptions
        print(f"({get_time()}) | Error executing function 'create_table_from_csv_file': {error}")
        tm.sleep(1)
        
#---###---#

# Function to list available SQL script files and allow the user to select one
def read_sql_scripts():
    # Defines the folder where the SQL files are stored
    folder = "./prompt_version/database/sql_scripts/"

    # Gets a list of all files in the folder that end with '.sql'
    sql_files = [f for f in os.listdir(folder) if f.endswith('.sql')]

    # Displays the available files to the user with numbering
    print("Files Available:")
    for i, file in enumerate(sql_files, start=1):
        print(f"{i} - {file}")

    while True:
        # Instruction for exiting this step
        print("\nIf you want to exit from this step, press 0")
        
        # Asks the user to select a file by its corresponding number
        try:
            selection = int(input("\nSelect the number from the file: "))
        except ValueError:
            # Handles the case where the input is not a valid integer
            print("Invalid input. Please enter a number.")
            continue

        # If the user chooses to exit
        if selection == 0:
            print("Exiting from this step...")
            tm.sleep(1)
            break

        # If the selection is within the valid range
        if 1 <= selection <= len(sql_files):
            # Gets the full path of the selected file
            file_path_selected = os.path.join(folder, sql_files[selection - 1])
            
            # Displays the selected file path
            print(f"\nYou selected: {file_path_selected}")
            return file_path_selected

        # If the entered number is invalid
        print("\nInvalid number, please, try again.")
        
#---###---#
        
# Function to list available CSV files and allow the user to select one
def read_csv_files():
    # Defines the folder where the CSV files are stored
    folder = "./prompt_version/database/csv_files/"
    
    # Gets a list of all files in the folder that end with '.csv'
    csv_files = [f for f in os.listdir(folder) if f.endswith('.csv')]
    
    # Displays the available files to the user with numbering
    print("Files Available:")
    for i, file in enumerate(csv_files, start=1):
        print(f"{i} - {file}")
    
    while True:
        # Asks the user to select a file by its corresponding number or 0 to exit
        selection = input("\nSelect the number from the file (or 0 to exit): ").strip()
        
        # If the user wants to exit
        if selection == "0":
            print("Exiting from this step...")
            tm.sleep(1)
            break
        
        # Checks if the input is a valid number
        if selection.isdigit():
            selection = int(selection)
            
            # If the selection corresponds to a valid file index
            if 1 <= selection <= len(csv_files):
                # Gets the full path of the selected file
                file_path_selected = os.path.join(folder, csv_files[selection - 1])
                
                # Displays the selected file path
                print(f"\nYou selected: {file_path_selected}")
                return file_path_selected
        
        # If the input is invalid
        print("\nInvalid number, please, try again.")
        
#---###---#

# Function to allow the user to create a table in DuckDB by typing the schema manually
def create_custom_table(conn_collected):
    # Title displayed to the user
    print("\n=== CREATE YOUR TABLE ===")
    
    # Asks for the table name, removes spaces from the start/end and replaces inner spaces with underscores
    table_name = input("Enter the table name: ").strip().replace(" ", "_")

    # Asks the user to define the table columns and their data types
    print("\nDefine your table columns (example: id INT PRIMARY KEY, name TEXT NOT NULL):")
    columns_structure = input("Enter column definitions: ").strip()

    # Validates if both the table name and column definitions are provided
    if not table_name or not columns_structure:
        print("Invalid input! Table name and columns cannot be empty.")
        return

    # Constructs the SQL CREATE TABLE command with the provided name and structure
    sql_command = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_structure})"

    try:
        # Executes the SQL command to create the table
        conn_collected.execute(sql_command)
        
        # Checks if the table was successfully created using DuckDB's internal metadata
        result = conn_collected.execute(
            f"SELECT COUNT(*) FROM duckdb_tables() WHERE table_name = '{table_name}'"
        ).fetchone()

        if result and result[0] > 0:
            print(f"({get_time()}) | Table '{table_name}' created successfully!")
        else:
            print(f"({get_time()}) | Table '{table_name}' was not found in the database!")

        # Waits for 1 second for better user experience
        tm.sleep(1)

    except Exception as error:
        # Generic error message in case of failure
        print(f"({get_time()}) | Error creating table: {error}")
        tm.sleep(1)
        
#---###---#

# Function to allow the user to create a table in DuckDB by typing the schema manually
def create_custom_table(conn_collected):
    # Title displayed to the user
    print("\n=== CREATE YOUR TABLE ===")
    
    # Asks for the table name, removes spaces from the start/end and replaces inner spaces with underscores
    table_name = input("Enter the table name: ").strip().replace(" ", "_")

    # Asks the user to define the table columns and their data types
    print("\nDefine your table columns (example: id INT PRIMARY KEY, name TEXT NOT NULL):")
    columns_structure = input("Enter column definitions: ").strip()

    # Validates if both the table name and column definitions are provided
    if not table_name or not columns_structure:
        print("Invalid input! Table name and columns cannot be empty.")
        return

    # Constructs the SQL CREATE TABLE command with the provided name and structure
    sql_command = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_structure})"

    try:
        # Executes the SQL command to create the table
        conn_collected.execute(sql_command)
        
        # Checks if the table was successfully created using DuckDB's internal metadata
        result = conn_collected.execute(
            f"SELECT COUNT(*) FROM duckdb_tables() WHERE table_name = '{table_name}'"
        ).fetchone()

        if result and result[0] > 0:
            print(f"({get_time()}) | Table '{table_name}' created successfully!")
        else:
            print(f"({get_time()}) | Table '{table_name}' was not found in the database!")

        # Waits for 1 second for better user experience
        tm.sleep(1)

    except Exception as error:
        # Generic error message in case of failure
        print(f"({get_time()}) | Error creating table: {error}")
        tm.sleep(1)
        
#---###---#

# Provides an interactive SQL console for users to create tables easily
def create_table_from_console(conn_collected):
    # The default input starts with "CREATE TABLE IF NOT EXISTS "
    default_command = "CREATE TABLE IF NOT EXISTS "
    
    # Prompts the user to complete the CREATE TABLE command
    user_input = input(default_command)
    
    # Concatenates the default part with the user input to form the full SQL statement
    full_sql = default_command + user_input
    
    # Checks if the SQL statement ends with a semicolon ';' (required for execution)
    if full_sql.strip().endswith(";"):
        try:
            # Executes the full SQL statement using the provided DuckDB connection
            conn_collected.execute(full_sql)
            
            # Success message with timestamp
            print(f"({get_time()}) | Table created successfully!")
        except Exception as e:
            # Prints any error raised during SQL execution
            print(f"({get_time()}) | Error executing SQL: {e}")
    else:
        # Message prompting user to end command properly with a semicolon
        print(f"({get_time()}) | Your SQL command must end with ';' to execute.")
        
#---###---#

# Menu to create a new database and optionally create tables within it
def create_new_database_menu():
    try:
        # Attempts to create a new database and obtain a connection
        conn_obtained = create_database()
        
    except ValueError as error:
        # Prints error if database connection could not be established and exits the function
        print(f"({get_time()}) | A database connection was not established: {error} | Exiting...")
        tm.sleep(1)
        return
    
    # Asks the user if they want to create tables in the newly created database
    continue_input = input("Do you want to create tables in this new database? (Y/N): ")
    tm.sleep(1)
    
    if continue_input.strip().upper() == "Y":
        while True:
            # Displays menu options for table creation methods
            type_of_create_tables_menu_input = input(
                "What you want to do about your new tables? \n" 
                "1 - Create my own table using console interaction; \n"
                "2 - Import Schema construction from a SQL Script (The script needs to exist in the '/database/sql_scripts' folder); \n"
                "3 - Import Schema construction and data from a CSV File (The '.csv' file needs to exist in the '/database/csv_files' folder); \n"
                "4 - Create my own table using format schema of 'CREATE TABLE'; \n"
                "0 - Exit from this step. \n\n"
                "-> "
            )
            
            if type_of_create_tables_menu_input == "1":
                # Calls the function to create a custom table interactively
                create_custom_table(conn_collected=conn_obtained)
                
            if type_of_create_tables_menu_input == "2":
                # Reads the path of a SQL script selected by the user and executes it to create tables
                sql_script_file_path_obtained = read_sql_scripts()
                create_table_from_sql_script(
                    file_path_collected=sql_script_file_path_obtained,
                    conn_collected=conn_obtained
                )
                
            if type_of_create_tables_menu_input == "3":
                # Reads the path of a CSV file selected by the user and creates tables from it
                csv_file_path_obtained = read_csv_files()
                create_table_from_csv_file(
                    file_path_collected=csv_file_path_obtained,
                    conn_collected=conn_obtained
                )

            if type_of_create_tables_menu_input == "4":
                # Allows the user to enter a full CREATE TABLE statement directly in the console
                create_table_from_console(conn_collected=conn_obtained)
            
            if type_of_create_tables_menu_input == "0":
                # Exits the table creation loop/menu
                print("Exiting from this step...\n")
                tm.sleep(1)
                break