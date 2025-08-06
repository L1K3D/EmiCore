import os

from functions_work_local_databases import work_local_databases_menu
from functions_database_creator import create_new_database_menu
from functions_basics import *

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
    
    print("#---###---#---###---#---###---# \n\n Hello! Welcome to EmiCore! \n\n #---###---#---###---#---###---# \n\n")
    
    #---###---#
    
    while True:
    
        main_menu_input = input(
            "1 - Create a new database; \n"
            "2 - Work on local databases; \n"
            "0 - Exit \n\n"
            "-> "
        )
        
        if main_menu_input == "0":
            print("Closing system...")
            tm.sleep(1)
            break
        
        elif main_menu_input == "1":
            create_new_database_menu()

        elif main_menu_input == "2":
            work_local_databases_menu()
        
    #---###---#

    input("\nPressione ENTER para fechar...")
    os.system("pause")