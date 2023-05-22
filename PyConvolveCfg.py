from matplotlib import ticker

# Global variable definitions
XRange              = (-6,6)
XRes                = 25
YRange              = (-2,2)
respuesta_impulsiva = ("Respuesta impulsiva",   "h(t)")
respuesta_sistema   = ("Respuesta del sistema", "y(t)")
entrada_sistema     = ("Señal de entrada",      "f(t)")
nmfilter            = ('"',"{","}","$"," ","\\")

# Dictionaries
color_palette       = {"background":     "darkseagreen",
                       "foreground":     "linen",
                       "plot_line":      "firebrick"}

grid_cfg            = {"minor":{
                           "color":      "darkred",
                           "linestyle":  "-",
                           "linewidth":  0.1,
                           "which":      "minor"
                           },
                       "major":{
                           "color":     "darkred",
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