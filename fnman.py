import math
import numpy as np
import matplotlib.pyplot as plt
from PyConvolveCfg import *
from matplotlib import ticker

# catchConstants :: Str -> Str
# takes a math function and looks for mathematic constants such as pi and euler
def catchConstants(expr):
    c = 0
    skip = False

    for i in expr:
        if skip:
            skip = False
            continue

        if i == "e":
            expr.pop(c)
            expr.insert(c, str(math.e))

        elif i == "p":
            if expr[c + 1] == "i":
                expr.pop(c)
                expr.pop(c)
                expr.insert(c, str(math.pi))
            # skip=True

        elif i == "^":
            expr.pop(c)
            expr.insert(c, "**")
        c += 1
    return


# catchFunctions :: Str -> Str
# Adds the math module to trigonometric functions present in the input
def catchFunctions(expr):
    valid_fn = ("sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "log", "ln(")
    trigger = set(list([x[0] for x in valid_fn]))  # First letter of each case
    c = 0
    pos = list()
    skip = [False, 0]

    for i in expr:

        if skip[0]:
            if skip[1] < 1:
                skip[0] = False
            skip[1] -= 1
            continue

        if i in trigger:
            if (
                "".join(expr[c : c + 3]) in valid_fn
                or "".join(expr[c : c + 4]) in valid_fn
            ):
                pos.append(c)
                skip = [True, 2]
        c += 1

    pos.sort(reverse=True)
    for j in pos:
        expr.insert(j, "math.")

    return


# signalCatch :: Str -> Int[]
# Deletes signal functions if present. outputs an array describing
# said function. Accepts: d(dirac), u(step), p(pulse)
# output: [ [ index_start, fn_type, operation, [ description ] ] ]
# the description is either an expression for t=0 or in the case of a pulse
# a range a,b
# then modifiers takes that array and replaces the definition with an array
def signalCatch(expr):
    sigOnly = False
    finder = list()
    c = 0
    _id = 0
    capture = False
    internal = list()
    # signal finder: gets the start, type and content of the signal funtions
    for i in expr:
        if capture:
            internal.append(i)
            if i == ")":
                capture = False
                finder[_id].append("".join(internal[1:-1]))
                internal = []
                _id += 1
        if i in ("d", "u", "p"):
            finder.append(
                [c, i, expr[c - 1] if c != 0 else ""]
            )  # Index, Type, operation
            r = 1
            while finder[_id][2] == "(":
                finder[_id][2] = expr[c - r]
                r += 1
            capture = True
        c += 1
    if len(finder) == 0:
        return expr
    # function replacer: takes the information gathered and replaces signal
    # functions with a modifiers() call, wich in turn outputs an array
    finder.reverse()

    # deleting signals and creating a copy
    new_expr = str(expr)
    for func in finder:
        end_index = func[0] + len(func[3]) + 3
        new_expr = [
            new_expr[x]
            for x in range(len(new_expr))
            if x not in range(func[0] - 1, end_index)
        ]
        new_expr = "".join(new_expr)

    # Fail check
    fail = True
    while fail:
        try:
            eval(new_expr, {"np": np, "math": math}, {"t": 1.0283, "i": 1.0283})
            fail = False
        except:
            new_expr = list(new_expr)
            new_expr.pop()
            new_expr = "".join(new_expr)

    if len(new_expr) >= 1:
        expr_len = len(range(*XRange)) * XRes + findRoot(new_expr)
    else:
        expr_len = len(range(*XRange)) * XRes
        sigOnly = True

    final_expr = list(new_expr)
    for func in finder:
        end_index = func[0] + len(func[3]) + 3
        if not sigOnly:
            final_expr = [
                expr[x]
                for x in range(len(expr))
                if x not in range(func[0] - 1, end_index)
            ]
        final_expr.insert(func[0], modifiers(func, expr_len))

    return final_expr


# modifiers :: Array, Int -> 1D Array
# takes the output of signalCatch and the lenght of the X axis
# evaluates each case, outputting a single array that will operate the Y axis
def modifiers(func, lenght):
    # find the zero value
    c = 0
    zero_index = int()
    values = list()
    for j in range(*XRange):
        if j == 0:
            zero_index = c * XRes # output
            break
        c += 1

    if func[1] == "u":  ## Step function
        displacement = -eval(func[3], {}, {"t": 0})
        clist = [
            0 if x < zero_index + displacement * XRes else 1 for x in range(lenght)
        ]
        values.append([clist, func[2]])
        
    elif func[1] == "p":  ## Pulse from a to b
        limits = list(map(int, str(func[3]).split(",")))
        clist = [
            1 if (limits[0] + 1) * XRes < x and x < (limits[1] + 1) * XRes else 0
            for x in range(lenght)
        ]
        values.append([clist, func[2]])

    elif func[1] == "d":  ## Dirac delta, an impulse
        displacement = -eval(func[3], {}, {"t": 0})
        clist = [
            0 if x != zero_index + displacement * XRes else 1 for x in range(lenght)
        ]
        values.append([clist, func[2]])

    # Conversion from list to expression
    values = list(*values)
    expression_value = f"{values[1]}np.array({values[0]})[i]"
    return expression_value


# inputRead :: Str -> Str
# Takes an insecure user input and sanitizes it for eval()
def inputRead(_msg="Input"):
    print(_msg + ": ", end=" ")
    sanitized = list()
    for i in input():
        if i not in nmfilter:
            sanitized.append(i)
    catchConstants(sanitized)
    catchFunctions(sanitized)
    final = signalCatch("".join(sanitized))

    return "".join(final)


# findRoot :: Str -> Int
# given an expression, finds the number of undefined points
def findRoot(expr):
    roots = 0
    X_values = [i / XRes for i in range(XRes * XRange[0], XRes * XRange[1] + 1)]

    for t in X_values:
        try:
            eval(expr)

        except ZeroDivisionError:
            roots += 2

    return roots


# funcSweep :: Str, Int, Int -> list[int[],int[]]
# Takes a math expression and evaluates it on the given range
# The function is defined between [-5;5] by default and
# There will be range times resolution values inside the specified range
# the output has the structure [ [X_values], [Y_values] ]
def funcSweep(expr, _range=XRange, _resolution=XRes):
    X_values = list()
    Y_values = [
        i / _resolution
        for i in range(_resolution * _range[0], _resolution * _range[1] + 1)
    ]

    c = 0
    skip = False
    for t in Y_values:
        if skip:
            skip = False
            continue
        evaluation = (expr, {"i": c}, {"t": t, "np": np, "math": math})
        try:
            X_values.append(eval(*evaluation))
        except ZeroDivisionError:
            Y_values.remove(t)
            t -= 1 / 2**16
            Y_values.insert(c, t)
            X_values.append(eval(*evaluation))
            t += 2 / 2**16
            Y_values.insert(c + 1, t)
            X_values.append(eval(*evaluation))
            skip = True

        except ValueError:
            X_values.append(0)

        except IndexError:
            X_values.append(X_values[-1])
            return np.array([Y_values, X_values])

        c += 1

    return np.array([Y_values, X_values])


# plotter :: List[Float[]], Str, Str -> IO
# Takes a list of XY values and outputs a png of the plot
# Aditionally takes text data for the title and axis label
def plotter(data, title, y_title, _xlim=XRange, _ylim=YRange):
    ## Plot call and trimming
    fig, ax = plt.subplots()
    ax.set_xlim(*_xlim)
    ax.set_ylim(*_ylim)

    ## Main colors
    fig.set_facecolor(color_palette["background"])
    ax.set_facecolor(color_palette["foreground"])
    ax.plot(*data, color=color_palette["plot_line"])

    ## Grid, axes and locators
    ax.grid(**grid_cfg["minor"])
    ax.grid(**grid_cfg["major"])
    ax.axvline(**grid_cfg["axis_line"])
    ax.axhline(**grid_cfg["axis_line"])
    ax.xaxis.set_minor_locator(grid_cfg["locator"])
    ax.yaxis.set_minor_locator(grid_cfg["locator"])

    ## Labels
    ax.set_title(title, size=18)
    ax.set_xlabel("t", loc="right", weight="bold")
    ax.set_ylabel(y_title, loc="top", rotation="horizontal", weight="bold")

    ## Save and export
    fig.savefig("figure.png")
    fig.show()