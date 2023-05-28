from modules.PyConvolveCfg import defaultConfiguration as cfg
from modules.parsing import UserDefinedFunction
from modules.functions import plotter
from scipy import signal
import os
import time

def clear():
    if cfg.UNIX:
        os.system("clear")
        return
    os.system("cls")

def getInput(_msg,DEBUG=False):
    function_object = UserDefinedFunction(f"{_msg}:  \n")
    try:
        function_object.getValues()
    except Exception as e:
        clear()
        print(f"Ocurrió un error, inténtalo de nuevo.\nexpresión introducida: {function_object.raw_expression}")
        if DEBUG:
            print(e)
        return getInput(f"Vuelve a introducir la {_msg}")
    return function_object

def printStatus(sysinput,sysresponse):
    clear()
    print("Convolución finalizada.")
    print(f"Respuesta impulsiva:           {impulse_response.raw_expression}\nSeñal introducida al sistema:  {system_input.raw_expression}")
    print(f"la grafica ha sido exportada en {cfg.EXPORT_PATH}/Respuesta del sistema.pdf")

def updateResponse(system_input,impulse_response):
    # Convolution step

    system_response = [
        system_input.X_Axis,
        signal.convolve(
            system_input.Y_Axis, impulse_response.Y_Axis, mode="same"
        )
        / cfg.XRes,
    ]

    # Plotting system response
    plotter(system_response, *cfg.respuesta_sistema)

def editSignals(sysinput,sysresponse):
    clear()
    print("[R] Editar respuesta impulsiva\n[S] Editar señal de entrada\n[A] Editar ambas\n[E] Salir")
    answer = input().lower()
    if answer == "a":
        clear()
        sysresponse = getInput("Respuesta impulsiva del sistema",True)
        plotter([sysresponse.X_Axis,sysresponse.Y_Axis], *cfg.respuesta_impulsiva)

        clear()
        print(f"Respuesta impulsiva:   {sysresponse.raw_expression}")
        sysinput = getInput("Señal introducida al sistema")
        plotter([sysinput.X_Axis,sysinput.Y_Axis], *cfg.entrada_sistema)
        updateResponse(sysinput, sysresponse)
        return (sysinput,sysresponse)

    elif answer == "e":
        clear()
        return (sysinput,sysresponse)

    elif answer == "s":
        clear()
        print(f"Señal de entrada anterior:  {sysinput.raw_expression}")
        sysinput = getInput("Nueva señal de entrada")
        plotter([sysinput.X_Axis,sysinput.Y_Axis], *cfg.entrada_sistema)
        updateResponse(sysinput, sysresponse)
        return (sysinput,sysresponse)
    elif answer == "r":
        clear()
        print(f"Respuesta impulsiva anterior:  {sysresponse.raw_expression}")
        sysresponse = getInput("Nueva respuesta impulsiva")
        plotter([sysresponse.X_Axis,sysresponse.Y_Axis], *cfg.respuesta_impulsiva)
        updateResponse(sysinput, sysresponse)
        return (sysinput,sysresponse)
    else:
        print("No se reconoció el comando, intenta de nuevo")
        editSignals(sysinput, sysresponse)

def updateGraphs(system_input,system_response):
    plotter([impulse_response.X_Axis,impulse_response.Y_Axis], *cfg.respuesta_impulsiva)
    plotter([system_input.X_Axis,system_input.Y_Axis], *cfg.entrada_sistema)
    updateResponse(system_input, impulse_response)

def editGraph(sysinput,sysresponse):
    clear()
    print("[Y] Editar eje vertical\n[X] Editar eje horizontal, [E] Salir")
    answer = input().lower()

    if answer == "y":
        minimum = int(input("Valor mínimo de la gráfica: "))
        maximum = int(input("Valor máximo de la gráfica: "))
        cfg.YPlotRange = [minimum, maximum]
        updateGraphs(sysinput, sysresponse)
        del minimum
        del maximum
        printStatus(sysinput,sysresponse)
        return (sysinput,sysresponse)

    elif answer == "x":
        minimum = int(input("Valor mínimo de la gráfica: "))
        maximum = int(input("Valor máximo de la gráfica: "))
        cfg.XPlotRange = [minimum,maximum]
        
        if max((minimum,maximum)) > cfg.XRange[1]:
            cfg.updateRange()
            sysinput.getValues()
            sysresponse.getValues()
            updateGraphs(sysinput, sysresponse)
        else:
            updateGraphs(sysinput, sysresponse)
        del minimum
        del maximum
        return (sysinput,sysresponse)
    elif answer == "e":
        clear()
        return (sysinput,sysresponse)
    else:
        print("No se reconoció el comando, intenta de nuevo")
        editGraph(sysinput, sysresponse)

def mainMenu(sysinput,sysresponse):
    print("")
    print("[Enter] Finalizar ejecución")
    print("[G] Editar gráfica\n[E] Editar expresiones")
    answer = input().lower()
    options = ("g","e","p")

    if answer not in options:
        return (False,False)
    elif answer == "g":
        return editGraph(sysinput,sysresponse)
    elif answer == "e":
        return editSignals(sysinput,sysresponse)
    elif answer == "p":
        print(sysinput)
        print(sysresponse)
        input()
        return (sysinput,sysresponse)


if __name__ == "__main__":
    # function gathering and processing
    clear()
    impulse_response = getInput("Respuesta impulsiva del sistema")
    plotter([impulse_response.X_Axis,impulse_response.Y_Axis], *cfg.respuesta_impulsiva)

    clear()
    print(f"Respuesta impulsiva:   {impulse_response.raw_expression}")
    system_input = getInput("Señal introducida al sistema")
    plotter([system_input.X_Axis,system_input.Y_Axis], *cfg.entrada_sistema)

    # main loop
    while True:
        
        updateResponse(system_input, impulse_response)
        time.sleep(0.001)
        printStatus(system_input,impulse_response)
        system_input, impulse_response = mainMenu(system_input, impulse_response)
        if not system_input:
            break
