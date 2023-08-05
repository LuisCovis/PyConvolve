try:
    import math
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy
    from modules.PyConvolveCfg import defaultConfiguration as cfg
    from matplotlib import ticker
except:
    print("No se encontraron algunas dependencias, asegúrate de instalar MatPlotLib, Numpy y sciPy antes de ejecutar.")
    input()
    exit()

def getLenght():
    return len(range(*cfg.XRange)) * cfg.XRes


def getZero_index():
    return getLenght() // 2


def u(step_expression: int, index: int) -> int:  # Step function
    displacement = -eval(step_expression, {}, {"t": 0})
    t_isPositive = (eval(step_expression, {}, {"t": 1}) + displacement) > 0
    lenght = getLenght()
    zero_index = getZero_index()
    if t_isPositive:
        return 0 if index <= zero_index + displacement * cfg.XRes else 1

    return 1 if index <= zero_index + displacement * cfg.XRes else 0


def p(pulse_range: int, index: int, *args) -> int:  # Pulse signal
    limits = tuple(map(float, str(pulse_range).split(",")))
    lenght = getLenght()
    zero_index = getZero_index()
    return (
        1
        if zero_index + limits[0] * cfg.XRes <= index
        and index < zero_index + limits[1] * cfg.XRes
        else 0
    )


def d(dirac_expression: int, index: int) -> int:  # Dirac delta
    displacement = -eval(dirac_expression, {}, {"t": 0})
    lenght = getLenght()
    zero_index = getZero_index()
    return 0 if index != zero_index + displacement * cfg.XRes else cfg.XRes


# plotter :: List[Float[]], Str, Str -> IO
# Takes a list of XY values and outputs a png of the plot
# Aditionally takes text data for the title and axis label
def plotter(
    data,
    title,
    y_title,
    PATH=cfg.EXPORT_PATH,
):
    _xlim=cfg.XPlotRange
    _ylim=cfg.YPlotRange
    ## Plot call and trimming
    fig, ax = plt.subplots()
    ax.set_xlim(*_xlim)
    ax.set_ylim(*_ylim)

    ## Main colors
    fig.set_facecolor(cfg.color_palette["background"])
    ax.set_facecolor(cfg.color_palette["foreground"])
    ax.plot(*data, color=cfg.color_palette["plot_line"])

    ## Grid, axes and locators
    ax.grid(**cfg.grid_cfg["minor"])
    ax.grid(**cfg.grid_cfg["major"])
    ax.axvline(**cfg.grid_cfg["axis_line"])
    ax.axhline(**cfg.grid_cfg["axis_line"])
    ax.xaxis.set_minor_locator(cfg.grid_cfg["locator"])
    ax.xaxis.set_major_locator(cfg.grid_cfg["maj_locator"])
    ax.yaxis.set_minor_locator(cfg.grid_cfg["locator"])

    ## Labels
    ax.set_title(title, size=18)
    ax.set_xlabel("t", loc="right", weight="bold")
    ax.set_ylabel(y_title, loc="top", rotation="horizontal", weight="bold")

    ## Save and export
    fig.savefig(f"{PATH}/{title}.pdf")
