import re
import math
import numpy as np
from modules.functions import p, u, d
from modules.PyConvolveCfg import defaultConfiguration as cfg
#import time

REGEX_SANITIZING_FILTER = "|\\".join(cfg.nmfilter)
REGEX_FUNCTIONS = "|".join(cfg.function_list)

class UserDefinedFunction:
    def __init__(self, message):
        self.expression = re.sub(REGEX_SANITIZING_FILTER, "", input(f"{message}:  "))
        self.raw_expression = self.expression
        self.X_Axis = list()
        self.Y_Axis = list()
        self.__findAbsoluteValues()
        self.__processSignals()
        self.__processFunctions()
        self.__processConstants()

    def __findAbsoluteValues(self):
        PATTERN = "(?<=\|).*?(?=\|)"
        self.expression = re.sub(
            PATTERN, lambda match: f"abs({match[0]})", self.expression
        )
        self.expression = re.sub("\|", "", self.expression)
        return

    def __processFunctions(self):
        self.expression = re.sub(
            REGEX_FUNCTIONS, lambda match: f"math.{match[0]}", self.expression
        )
        return

    def __processConstants(self):
        self.expression = re.sub("e", str(math.e), self.expression)
        self.expression = re.sub("pi", str(math.pi), self.expression)
        self.expression = re.sub("\^", "**", self.expression)
        return

    def __processSignals(self):
        EXPRESSION = "((?<=u\()|(?<=p\()|(?<=d\()).*?(?=\))"
        self.expression = re.sub(
            EXPRESSION, lambda match: f"'{match[0]}',i", self.expression
        )

    def getValues(self):
        #start = time.time()
        cfg.updateRange()
        self.X_Axis = [
            i / cfg.XRes
            for i in range(cfg.XRes * cfg.XRange[0], cfg.XRes * cfg.XRange[1] + 1)
        ]
        self.Y_Axis = []
        c = 0
        for t in self.X_Axis:
            evaluation = (
                self.expression,
                {},
                {"i": c, "t": t, "math": math, "p": p, "u": u, "d": d, "np": np},
            )
            try:
                self.Y_Axis.append(eval(*evaluation))
            except ZeroDivisionError:
                self.Y_Axis.append(2**15)

            except ValueError:
                self.Y_Axis.append(0)

            except IndexError:
                self.Y_Axis.append(self.Y_Axis[-1])
            c += 1
        #print(f"La funcion tardó {time.time() - start} segundos en generar")
        #input()
        return np.array([self.X_Axis, self.Y_Axis])

    def __str__(self):
        return f"La expresión inicial es {self.raw_expression}, que se convirtió a {self.expression}. actualmente el eje X tiene {len(self.X_Axis)} números, mientras que el eje Y tiene {len(self.Y_Axis)}"


def getInput(_msg="Input"):
    return UserDefinedFunction(_msg)
