import duckdb
import logging
import time as tm

#---###---#

conn = duckdb.connect("matchbusiness_main_db.db")

#---###---#

def create_users_table(creation_tentative_collected):
    
    if creation_tentative_collected == True:
        
        try:
            
            
            logging.info("Executing the attempt to create the 'users' table...")
            

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
            
            
            logging.info("The process of creating the 'users' table was successfully completed!")
            
            
        except Exception as error:
            
            
            logging.error(f"The attempt has raised an error: {error}")
            
            
    else:
        
        
        logging.info("The process of attempting to create the 'users' table is disabled.")
        
        
#---###---#
        
def create_connections_table(creation_tentative_collected):
    
    if creation_tentative_collected == True:
        
        try:
        
            
            logging.info("Executing the attempt to create the 'connections' table...")
            
            
            conn.execute("""
                CREATE TABLE connections (
                    id INTEGER PRIMARY KEY,
                    user1_id INTEGER,
                    user2_id INTEGER,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT NOW(), -- Data e hora da criação da conexão
                    FOREIGN KEY (user1_id) REFERENCES users(id),
                    FOREIGN KEY (user2_id) REFERENCES users(id)
                )       
            """)
            
            logging.info("The process of creating the 'connections' table was successfully completed!")
            
        except Exception as error:
            
            logging.error(f"The attempt has raised an error: {error}")
            
            
    else:
        
        
        logging.info("The process of attempting to create the 'connections' table is disabled.")
        
        
#---###---#
        
def create_messages_table(creation_tentative_collected):
    
    if creation_tentative_collected == True:
        
        try:
        
            
            logging.info("Executing the attempt to create the 'messages' table...")
            

            conn.execute("""
                CREATE TABLE messages (
                    id INTEGER PRIMARY KEY,
                    sender_id INTEGER,
                    receiver_id INTEGER,
                    content TEXT,
                    send_at TIMESTAMP DEFAULT NOW(),
                    status TEXT,
                    FOREIGN KEY (sender_id) REFERENCES users(id),
                    FOREIGN KEY (receiver_id) REFERENCES users(id)
                )       
            """) 
            
            
            
            logging.info("The process of creating the 'messages' table was successfully completed!")
            
            
        except Exception as error:
            
            logging.error(f"The attempt has raised an error: {error}")
            
            
    else:
        
        logging.info("The process of attempting to create the 'messages' table is disabled.")
        
        
#---###---#

def create_meetings_table(creation_tentative_collected):
    
    if creation_tentative_collected == True:
        
        try:
        
            
            logging.info("Executing the attempt to create the 'meetings' table...")
            

            conn.execute("""
                CREATE TABLE meetings (
                    id INTEGER PRIMARY KEY,
                    date_time TIMESTAMP,
                    location TEXT,
                    participants TEXT[],
                    status TEXT
                )       
            """) 
            
            
            
            logging.info("The process of creating the 'meetings' table was successfully completed!")
            
            
        except Exception as error:
            
            
            logging.error(f"The attempt has raised an error: {error}")
            
            
    else:
        
        
        logging.info("The process of attempting to create the 'meetings' table is disabled.")
        

#---###---#
        
def create_places_table(creation_tentative_collected):
    
    if creation_tentative_collected == True:
        
        try:
        
            
            logging.info("Executing the attempt to create the 'places' table...")
            

            conn.execute("""
                CREATE TABLE places (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    address TEXT,
                    category TEXT,
                    rating FLOAT
                )       
            """) 
            
            
            
            logging.info("The process of creating the 'places' table was successfully completed!")
            
            
        except Exception as error:
            
            
            logging.error(f"The attempt has raised an error: {error}")
            
            
    else:
        
        
        logging.info("The process of attempting to create the 'places' table is disabled.")
        
        
#---###---#
        
def create_feedbacks_table(creation_tentative_collected):
    
    if creation_tentative_collected == True:
        
        try:
        
            
            logging.info("Executing the attempt to create the 'feedbacks' table...")
            

            conn.execute("""
                CREATE TABLE feedbacks (
                    id INTEGER PRIMARY KEY,
                    meeting_id INTEGER,
                    user_id INTEGER,
                    score INTEGER CHECK (score BETWEEN 1 AND 5),
                    comment TEXT,
                    FOREIGN KEY (meeting_id) REFERENCES meetings(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )       
            """) 
            
            
            
            logging.info("The process of creating the 'feedbacks' table was successfully completed!")
            
            
        except Exception as error:
            
            
            logging.error(f"The attempt has raised an error: {error}")
            
            
    else:
        
        
        logging.info("The process of attempting to create the 'feedbacks' table is disabled.")
        
        
#---###---#
        
def create_user_settings_table(creation_tentative_collected):
    
    if creation_tentative_collected == True:
        
        try:
        
            
            logging.info("Executing the attempt to create the 'user_settings' table...")
            

            conn.execute("""
                CREATE TABLE user_settings (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    notifications_enabled BOOLEAN,
                    dark_mode BOOLEAN,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )       
            """) 
            
            
            
            logging.info("The process of creating the 'user_settings' table was successfully completed!")
            
            
        except Exception as error:
            
            
            logging.error(f"The attempt has raised an error: {error}")
            
            
    else:
        
        
        logging.info("The process of attempting to create the 'user_settings' table is disabled.")
        
        
#---###---#
#---###---#
#---###---#

if __name__ == "__main__":
    
    create_users_table(True)
    create_connections_table(True)
    create_messages_table(True)
    create_meetings_table(True)
    create_places_table(True)
    create_feedbacks_table(True)
    create_user_settings_table(True)