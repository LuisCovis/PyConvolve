from matplotlib import ticker
import os

class MainConfiguration:
    def __init__(self):

        # Global variable definitions
        self.UNIX                = True if os.name != "nt" else False
        self.EXPORT_PATH         = os.getcwd()+"/graphs/" if self.UNIX else os.getcwd()+"\graphs\\"
        self.XPlotRange          = [-5,5]
        self.YPlotRange          = [-2,2]
        self.XRange              = [-max(self.XPlotRange),max(self.XPlotRange)]
        self.XRes                = 25
        self.respuesta_impulsiva = ("Respuesta impulsiva",   "h(t)")
        self.respuesta_sistema   = ("Respuesta del sistema", "y(t)")
        self.entrada_sistema     = ("Señal de entrada",      "f(t)")
        self.nmfilter            = ('"',"{","}","$"," ","\\","ç")
        self.function_list       = ("sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "log")

        # Dictionaries
        self.color_palette       = {"background":     "#151515",
                                    "foreground":     "#FAFAFA",
                                    "plot_line":      "#F20000",
                                    "text_color":     "#FAFAFA"}

        self.grid_cfg            = {"minor":{
                                        "color":      "#C2C2C2",
                                        "linestyle":  "-",
                                        "linewidth":  0.1,
                                        "which":      "minor"
                                        },
                                    "major":{
                                        "color":     "#D2D2D2",
                                        "linestyle": "-",
                                        "linewidth":  0.5,
                                        "which":     "major"
                                        },
                                    "axis_line":{
                                        "color":      "black",
                                        "linewidth":  1,
                                        "linestyle":  "--"
                                        },
                                    "locator":        ticker.MultipleLocator(.5),
                                    "maj_locator":    ticker.AutoLocator()
                                    }

    def updateRange(self):
        self.XRange              = [-max(self.XPlotRange),max(self.XPlotRange)]

defaultConfiguration = MainConfiguration()