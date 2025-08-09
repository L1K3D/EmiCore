import duckdb
import os
import time as tm
from tabulate import tabulate

from functions_basics import get_time
from functions_database_creator import create_custom_table, create_table_from_console, read_csv_files, create_table_from_csv_file, read_sql_scripts, create_table_from_sql_script

def select_database_to_work():

    folder = "./prompt_version/database/local_databases/"

    db_files = [f for f in os.listdir(folder) if f.endswith('.db')]

    for i, file in enumerate(db_files, start=1):
        print(f"{i} - {file}")

    selection = int(input("\nSelect the number from the file: "))

    while True:
        print("If you want exit from this step, press 0 \n")

        if 1 <= selection <= len(db_files):
            file_path_selected = os.path.join(folder, db_files[selection - 1])
            print(f"\nYou select: {file_path_selected}")
            return file_path_selected
        
        elif selection == "0":
            print("Exiting from this step...")
            tm.sleep(1)
            break
        
        else:
            print("\nInvalid number, please, try again.")

def delete_databases():

    folder = "./prompt_version/database/local_databases/"

    db_files = [f for f in os.listdir(folder) if f.endswith('.db')]

    for i, file in enumerate(db_files, start=1):
        print(f"{i} - {file}")

    selection = int(input("\nSelect the number from the file: "))

    while True:
        print("If you want exit from this step, press 0 \n")

        if 1 <= selection <= len(db_files):
            file_path_selected = os.path.join(folder, db_files[selection - 1])
            option_delete_database_input = input(f"\nYou selected: {file_path_selected}. Are you sure you want to delete it? (Y/N)")
            
            if option_delete_database_input.strip().upper() == "Y":
                os.remove(file_path_selected)
                print(f"The database {file_path_selected} was deleted")

            elif option_delete_database_input.strip().upper() == "N":
                print(f"({get_time()}) | Process aborted by the user.")
                break

            else:
                print("Please, select a valid option")

        if selection == "0":
            print("Exiting from this step...")
            tm.sleep(1)
            break

def list_tables_in_database(file_path_collected):

    print("-----")

    conn = duckdb.connect(f'{file_path_collected}')

    tables_df = conn.sql("SHOW TABLES").df()
    print(tables_df)
    print("-----")

def delete_selected_database(file_path_collected):
    
    db_file_path = file_path_collected

    os.remove(db_file_path)

    print(f"The database named {db_file_path} was deleted sucefully")

#---###---#

def execute_custom_query(file_path_collected):
    
    print("-----")
    print("\nWrite your SQL query here, or write 'exit' to back to menu:\n")
    
    #---###---#
    
    # Open a connection to the DuckDB database file located at 'file_path_collected'
    conn = duckdb.connect(file_path_collected)
    
    while True:
        # Prompt the user to input an SQL query
        query = input("SQL> ")

        # Exit condition: if the user types 'exit', break the loop and return to menu
        if query.strip().lower() == "exit":
            break

        print("#---result---#")

        try:
            # Execute the SQL query and fetch all results as a pandas DataFrame
            df = conn.execute(query).fetchdf()

            # Check if the DataFrame contains any rows (i.e., the query returned results)
            if not df.empty:
                # Using 'tabulate' to print the DataFrame in a well-formatted table style
                # 'headers="keys"' means the column names will be printed as headers
                # 'tablefmt="psql"' styles the table similar to PostgreSQL console output
                # 'showindex=False' hides the DataFrame's index column for cleaner output
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            else:
                # Inform the user that the query ran successfully but returned no rows (e.g., for INSERT, UPDATE)
                print("Query executed successfully (no results to show).")

            print("")

        except Exception as e:
            # Catch and display any errors that occur during query execution, such as syntax errors
            print(f"Erro: {e}")

#---###---#

def work_local_databases_menu():

    while True:
        action_on_local_databases_input = input(
            "1 - Select a database to work at; \n"
            "2 - Delete a database; \n"
            "0 - Exit \n\n"
            "-> "
        )

        if action_on_local_databases_input == "0":
            print("Returning to the 'Main' menu...")
            tm.sleep(1)
            break

        elif action_on_local_databases_input == "1":
            print("Select a database to work at:")
            database_selected = select_database_to_work()

            while True:
                workin_at_select_database_input = input(
                    "1 - List tables; \n"
                    "2 - Execute SQL query; \n"
                    "3 - Create your own table using console interaction; \n"
                    "3 - Delete table; \n"
                    "4 - Delete database; \n"
                    "0 - Exit \n\n"
                    "-> "
                )
                
                if workin_at_select_database_input == "0":
                    print("Returning to the 'Action on Databases' menu...")
                    break

                elif workin_at_select_database_input == "1":
                    list_tables_in_database(database_selected)

                elif workin_at_select_database_input == "2":
                    execute_custom_query(database_selected)

                elif workin_at_select_database_input == "3":
                    conn_obtained=duckdb.connect(database_selected)
                    create_custom_table(conn_collected=conn_obtained)

                elif workin_at_select_database_input == "4":
                    delete_selected_database(database_selected)

        elif action_on_local_databases_input == "2":
            delete_databases()