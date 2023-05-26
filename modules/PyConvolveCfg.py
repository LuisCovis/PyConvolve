from matplotlib import ticker

# Global variable definitions
XRange              = (-3,3)
XRes                = 25
YRange              = (-2,2)
respuesta_impulsiva = ("Respuesta impulsiva",   "h(t)")
respuesta_sistema   = ("Respuesta del sistema", "y(t)")
entrada_sistema     = ("Señal de entrada",      "f(t)")
nmfilter            = ('"',"{","}","$"," ","\\")

# Dictionaries
color_palette       = {"background":     "#418ED9",
                       "foreground":     "#C0C8C8",
                       "plot_line":      "#282020"}

grid_cfg            = {"minor":{
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