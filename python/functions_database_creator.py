import duckdb
import logging
import time as tm
from main import get_time
import pandas as pd

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

def create_table_from_sql_script(database_path_collected, file_collected, coon_collected):
    
    sql_script_path = database_path_collected + file_collected
    
    try:
        with open(sql_script_path, "r", encoding="utf-8") as file:
            sql_script = file.read()
            
            if "CREATE TABLE" in sql_script:
                
                logging.info(sql_script)
                print(sql_script)
                
                logging.info()
                print()
                
                proceed_sql_script_execution = input("This sql script will be executed. Do you want to proceed? (Y/N)")
            
                if proceed_sql_script_execution == "Y":
            
                    coon_collected.execute(sql_script)
                    
                    logging.info(f"({get_time()}) | File '{sql_script}' executed sucessfully!")
                    print(f"({get_time()}) | File '{sql_script}' executed sucessfully!")
                    tm.sleep(1)
                    
                else:
                    
                    logging.info(f"({get_time()}) | Aborted! User doesn't agree with the sql script.")
                    print(f"({get_time()}) | Aborted! User doesn't agree with the sql script.")
                    tm.sleep(1)
                
            else:
                
                logging.info(f"({get_time()}) | The sql script must be an creation table action")
                print(f"({get_time()}) | The sql script must be an creation table action")
                tm.sleep(1)
    
    except FileNotFoundError:
        logging.info(f"({get_time()}) | File '{sql_script}' doesn't found.")
        print(f"({get_time()}) | File '{sql_script}' doesn't found.")
        tm.sleep(1)
        
    except Exception as error:
        logging.info(f"({get_time()}) |The function 'create_table_from_sql_script' has returned an error: {error}")
        print(f"({get_time()}) |The function 'create_table_from_sql_script' has returned an error: {error}")
        tm.sleep(1)
            
#---###---#            

def create_table_from_csv_file(database_path_collected, file_collected, coon_collected):
    
    csv_file_path = database_path_collected + file_collected
    
    try:
        
        df_csv_file = pd.read_csv(f'{csv_file_path}')
        print(df_csv_file.head(5))
        
        proceed_csv_file_execution = input("This csv file converted to pandas DataFrame will be created as a sql table. Do you want to proceed? (Y/N)")
        
        if proceed_csv_file_execution == "Y":
            
            table_name = file_collected[:3]
            
            coon_collected.execute(f"""
                                    
                CREATE TABLE IF NOT EXISTS {table_name} AS
                    SELECT *
                    FROM {df_csv_file}
                                   
            """)
            
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