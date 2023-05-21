import numpy as np
import matplotlib as mlp
import matplotlib.pyplot as plt
from matplotlib import ticker

# Global variable definitions
XRange              = 5
XRes                = 25
YRange              = 5
respuesta_impulsiva = ("Respuesta impulsiva","h(t)")
respuesta_sistema   = ("Respuesta del sistema","y(t)")
entrada_sistema     = ("Señal de entrada","f(t)")

# inputRead :: Str -> Str
# Takes an insecure user input and sanitizes it for eval()
def inputRead(_msg="Input"):
    filter=('"',"{","}","$"," ","\\")
    print(_msg+": ",end=" ")
    sanitized = list()
    for i in input():
        if i not in filter:
            sanitized.append(i)
        
    return "".join(sanitized)

# funcSweep :: Str, Int, Int -> list[int[],int[]]
# Takes a math expression and evaluates it on the given range
# The function is defined between [-5;5] by default and
# There will be range times resolution values inside the specified range
# the output has the structure [ [X_values], [Y_values] ]
def funcSweep(expr,_range=XRange,_resolution=XRes):
    X_values = list()
    Y_values = [i/_resolution for i in range(-_resolution*_range,
                                           _resolution*_range+1)]
    c = 0
    skip=False
    for t in Y_values:
        if skip:
            skip=False
            continue
        try:
            X_values.append(eval(expr))
        except:
            Y_values.remove(0)
            t -= 1/2**16
            Y_values.insert(c,t)
            X_values.append(eval(expr))
            t += 2/2**16
            Y_values.insert(c+1,t)
            X_values.append(eval(expr))
            skip=True
        c += 1
        
    return np.array([Y_values,X_values])

def plotter(data,title,y_title,_xlim=XRange,_ylim=YRange):
    ## Plot call and trimming
    fig, ax = plt.subplots()
    ax.set_xlim(-1,_xlim)
    ax.set_ylim(-1,_ylim)
    
    ## Main colors
    fig.set_facecolor("darkseagreen")
    ax.set_facecolor("linen")
    ax.plot(*data, color='firebrick')
    
    ## Grid, axes and locators
    ax.grid(color='darkred', linestyle='-', linewidth=0.5, which="major")
    ax.grid(color='maroon', linestyle='-', linewidth=0.1, which="minor")
    ax.axvline(color="black",linewidth=0.7,linestyle="--")
    ax.axhline(color="black",linewidth=0.7,linestyle="--")
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.2))
    
    ## Labels
    ax.set_title(title, size=18)
    ax.set_xlabel("t", loc="right",weight="bold")
    ax.set_ylabel(y_title,loc="top",rotation="horizontal",weight="bold")
    
    ## Save and export
    fig.savefig("figure.png")
    fig.show()

if __name__ == "__main__":
    my_expr=inputRead("Escribe algo")
    
    first_function= funcSweep(my_expr)
    
    plotter(first_function,*respuesta_impulsiva)
    
