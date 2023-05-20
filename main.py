def inputRead(msg="Input"):
    filter=('"','\\',"{","}","$","ç")
    print(msg+": ",end=" ")
    sanitized = list()
    for i in input():
        if i not in filter:
            sanitized.append(i)
        
    return "".join(sanitized)
    

if __name__ == "__main__":
    print(inputRead("Escribe algo"))