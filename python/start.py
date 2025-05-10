import subprocess
import time as tm

#---###---#

def start_emicore():
    # Executa o Python dentro de um novo console com code page 65001 (UTF-8)
    command = 'chcp 65001 > nul && python main.py'
    subprocess.run(["cmd.exe", "/K", command], creationflags=subprocess.CREATE_NEW_CONSOLE)

#---###---#

try:
    tm.sleep(2)  # Pausa para suavizar o início
    start_emicore()

except ValueError as error:
    print(f"Erro capturado ao iniciar: {error}")
    tm.sleep(10)