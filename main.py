from modules.PyConvolveCfg import (
    respuesta_impulsiva,
    respuesta_sistema,
    entrada_sistema,
    XRange,
    XRes,
)
from modules.functions import plotter, inputRead, funcSweep
from scipy import signal
import os


if __name__ == "__main__":
    # function gathering and processing
    os.system("cls" if os.name == "nt" else "clear")

    current_expr = inputRead("Ecuación que describe la respuesta del sistema: \n")
    impulse_response = funcSweep(current_expr)
    plotter(impulse_response, *respuesta_impulsiva)

    current_expr = inputRead("Señal introducida al sistema: \n")
    system_input = funcSweep(current_expr)
    plotter(system_input, *entrada_sistema)

    del current_expr

    system_response = [
        system_input[0],
        signal.fftconvolve(system_input[1], impulse_response[1],mode="same")/XRes,
    ]
    double_resolution = XRes * 2
    plotter(system_response, *respuesta_sistema)
