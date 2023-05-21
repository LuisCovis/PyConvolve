from PyConvolveCfg import respuesta_impulsiva, respuesta_sistema, entrada_sistema
from fnman import plotter, inputRead, funcSweep


if __name__ == "__main__":
    my_expr = inputRead("Escribe algo")

    first_function = funcSweep(my_expr)

    plotter(first_function, *respuesta_sistema)
