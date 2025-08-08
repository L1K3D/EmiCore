import duckdb
import os
import time as tm

from functions_basics import get_time

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
        if selection == "0":
            print("Exiting from this step...")
            tm.sleep(1)
            break
        else:
            print("\nInvalid number, please, try again.")

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
                    "2 - Execute fast SQL query; \n"
                    "3 - Delete table; \n"
                    "0 - Exit \n\n"
                    "-> "
                )
                
                if workin_at_select_database_input == "0":
                    print("Returning to the 'Action on Databases' menu...")
                    break

                elif workin_at_select_database_input == "1":
                    list_tables_in_database(database_selected)

        elif action_on_local_databases_input == "2":
            delete_databases()