import duckdb
import logging
import time as tm

conn = duckdb.connect("matchbusiness_main_db.db")

def create_users_table(creation_tentative_collected):
    
    if creation_tentative_collected == True:
        
        try:
            
            tm.sleep(1)
            logging.info("Executing the attempt to create the 'users' table...")
            tm.sleep(1)

            conn.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT DEFAULT 'simple',
                    company_id INTEGER,
                    interests TEXT[],
                    profile_photo TEXT,
                    availability TEXT[],
                    FOREIGN KEY (company_id) REFERENCES companies(id)
                )
            """)
            
            tm.sleep(1)
            logging.info("The process of creating the 'users' table was successfully completed!")
            tm.sleep(1)
            
        except Exception as error:
            
            tm.sleep(1)
            logging.info(f"The attempt has raised an error: {error}")
            tm.sleep(1)
            
    else:
        
        tm.sleep(1)
        logging.info("The process of attempting to create the 'users' table is disabled.")
        tm.sleep(1)
        
def create_connections_table(creation_tentative_collected):
    
    if creation_tentative_collected == True:
        
        try:
        
            tm.sleep(1)
            logging.info("Executing the attempt to create the 'users' table...")
            tm.sleep(1)
            
            conn.execute("""
                CREATE TABLE connections (
                    id INTEGER PRIMARY KEY,      -- Identificador único da conexão
                    user1_id INTEGER,            -- ID do primeiro usuário
                    user2_id INTEGER,            -- ID do segundo usuário
                    status TEXT,                 -- Status da conexão (pendente, aceita, recusada)
                    created_at TIMESTAMP DEFAULT NOW(), -- Data e hora da criação da conexão
                    FOREIGN KEY (user1_id) REFERENCES users(id),
                    FOREIGN KEY (user2_id) REFERENCES users(id)
                )       
            """)
            
            tm.sleep(1)
            logging.info("The process of creating the 'connections' table was successfully completed!")
            tm.sleep(1)
            
        except Exception as error:
            
            tm.sleep(1)
            logging.info(f"The attempt has raised an error: {error}")
            tm.sleep(1)
            
    else:
        
        tm.sleep(1)
        logging.info("The process of attempting to create the 'connections' table is disabled.")
        tm.sleep(1)