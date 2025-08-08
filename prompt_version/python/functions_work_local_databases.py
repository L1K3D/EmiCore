import duckdb
import os
import time as tm

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

    db_file_path = file_path_collected

    conn = duckdb.connect(f'{db_file_path}')

    tables_df = conn.sql("SHOW TABLES").df()
    print(tables_df)

def work_local_databases_menu():

    print("Select the local database you want to work on (The files listed here are avalible at 'emicore/database/local_databases') \n")

    database_selected = select_database_to_work()

    list_tables_in_database()



