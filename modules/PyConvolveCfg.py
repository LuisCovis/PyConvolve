from matplotlib import ticker
import os

class MainConfiguration:
    def __init__(self):

        # Global variable definitions
        self.EXPORT_PATH         = "graphs"
        self.UNIX                = True if os.name != "nt" else False
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
        self.color_palette       = {"background":     "#418ED9",
                                    "foreground":     "#C0C8C8",
                                    "plot_line":      "#282020"}

        self.grid_cfg            = {"minor":{
                                        "color":      "#58B0B8",
                                        "linestyle":  "-",
                                        "linewidth":  0.1,
                                        "which":      "minor"
                                        },
                                    "major":{
                                        "color":     "#58B0B8",
                                        "linestyle": "-",
                                        "linewidth":  0.5,
                                        "which":     "major"
                                        },
                                    "axis_line":{
                                        "color":      "black",
                                        "linewidth":  1,
                                        "linestyle":  "--"
                                        },
                                    "locator":        ticker.MultipleLocator(0.25),
                                    "maj_locator":    ticker.MultipleLocator(1)
                                    }

    def updateRange(self):
        self.XRange              = [-max(self.XPlotRange),max(self.XPlotRange)]
defaultConfiguration = MainConfiguration()
