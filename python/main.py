import time as tm

from functions_database_creator import create_database
from functions_basics import get_time
from functions_basics import install_libs
from functions_basics import print_logo
from functions_basics import install_python

#---###---#

install_python()

#---###---#

print()
packages_input = ["duckdb", "pandas"]
install_libs(packages_input)
print()

#---###---#

print()
print_logo()
print()

#---###---#

if __name__ == "__main__":
    
    print("#---###---#---###---#---###---# \n\n Hello! Welcome to EmiCore! \n For your first setup, you must create a database and this database need's to have at least one table configured. \n |Remember!| your sql scripts or csv files must exist in your 'database' folder.")
    print()
    
    #---###---#
    
    database_name_input = input('Please, enter a name to your database: ')
    tm.sleep(1)
    
    proceed_database_creation = input(f'The name seted up for your database is: {database_name_input}. Do you want proceed? (Y/N)')
    
    if proceed_database_creation.strip().upper() == 'Y':
        
        tm.sleep(1)
        create_database(database_name_input)
        tm.sleep(1)
    
    else:
        
        print(f"({get_time()}) #-# The creation of database has been aborted, so the other configurations can't be continued. Please, if you changed your mind now or later, do: 'exec EmiCore.exe' in your console again.")
        
    #---###---#