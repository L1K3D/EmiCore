import duckdb
import logging
import time as tm
from main import get_time
import pandas as pd
import re

#---###---#

def create_database(database_name_collected):
    
    try:
        
        conn = duckdb.connect(f'{database_name_collected}.db')
        
        logging.info(f"({get_time()}) | The database named {database_name_collected} was created sucessfully!")
        print(f"({get_time()}) | The database named {database_name_collected} was created sucessfully!")
        tm.sleep()
        
        return conn
    
    except ValueError as error:
        
        logging.error(f"({get_time()}) | The function 'create_database' has returned an error: {error}")
        print(f"({get_time()}) | The function 'create_database' has returned an error: {error}")
        tm.sleep(1)
    
#---###---#    

def create_table_from_sql_script(database_path_collected, file_collected, conn_collected):
    """
    Function to execute an SQL script and create tables in the DuckDB database.
    """
    sql_script_path = database_path_collected + file_collected
    
    try:
        # Open and read the SQL file
        with open(sql_script_path, "r", encoding="utf-8") as file:
            sql_script = file.read().strip()  # Removing extra spaces

        # Check if the script contains a CREATE TABLE command
        if re.search(r"^\s*CREATE\s+TABLE", sql_script, re.IGNORECASE):
            logging.info(f"({get_time()}) | Executing SQL script:\n{sql_script}")
            print(f"\nScript content:\n{sql_script}\n")

            proceed_sql_script_execution = input("This SQL script will be executed. Do you want to proceed? (Y/N): ")

            if proceed_sql_script_execution.strip().upper() == "Y":
                conn_collected.execute(sql_script)
                
                logging.info(f"({get_time()}) | File '{sql_script_path}' executed successfully!")
                print(f"({get_time()}) | File '{sql_script_path}' executed successfully!")
                tm.sleep(1)
                
            else:
                logging.info(f"({get_time()}) | Process aborted by the user.")
                print(f"({get_time()}) | Process aborted by the user.")
                tm.sleep(1)
                
        else:
            logging.warning(f"({get_time()}) | The SQL script must contain CREATE TABLE statements.")
            print(f"({get_time()}) | The SQL script must contain CREATE TABLE statements.")
            tm.sleep(1)
            
    except FileNotFoundError:
        logging.error(f"({get_time()}) | Error: File '{sql_script_path}' not found.")
        print(f"({get_time()}) | Error: File '{sql_script_path}' not found.")
        tm.sleep(1)
        
    except Exception as error:
        logging.error(f"({get_time()}) | Error executing SQL script: {error}")
        print(f"({get_time()}) | Error executing SQL script: {error}")
        tm.sleep(1)
            
#---###---#            

def create_table_from_csv_file(database_path_collected, file_collected, conn_collected):
    csv_file_path = database_path_collected + file_collected
    
    try:
        # Carrega o CSV em um DataFrame do Pandas
        df_csv_file = pd.read_csv(csv_file_path)
        print(df_csv_file.head(5))  # Exibe as primeiras linhas do arquivo
        
        proceed_csv_file_execution = input("This csv file converted to pandas DataFrame will be created as a sql table. Do you want to proceed? (Y/N): ")
        
        if proceed_csv_file_execution.strip().upper() == "Y":
            table_name = file_collected.replace(".csv", "").replace("-", "_").replace(" ", "_")  # Nome limpo da tabela
            
            # Executa a criação da tabela a partir do DataFrame Pandas
            conn_collected.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} AS 
                    SELECT * 
                    FROM df_csv_file""", 
                df_csv_file)
            
            logging.info(f"({get_time()}) | The '.csv' file has been created as a sql table sucessfully!")
            print(f"({get_time()}) | The '.csv' file has been created as a sql table sucessfully!")
            tm.sleep(1)
        
        else:
            logging.info(f"({get_time()}) | Aborted! User doesn't agree with the '.csv' file.")
            print(f"({get_time()}) | Aborted! User doesn't agree with the '.csv' file.")
            tm.sleep(1)
    
    except FileNotFoundError:
        logging.info(f"({get_time()}) | File {df_csv_file} doesn't found.")
        print(f"({get_time()}) | File {df_csv_file} doesn't found.")
        tm.sleep(1)
        
    except Exception as error:
        logging.info(f"({get_time()}) |The function 'create_table_from_csv_file' has returned an error: {error}")
        print(f"({get_time()}) |The function 'create_table_from_csv_file' has returned an error: {error}")
        tm.sleep(1)
        
#---###---#