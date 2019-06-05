columnas=['a','b','c','d','e','f']
cantidad=1

inicial=0
while inicial+cantidad<=len(columnas):
    salto=1
    if cantidad==1:
        salto=len(columnas)-inicial
    while inicial+salto+cantidad-1<=len(columnas):
        arrcol=[]
        #print inicial
        n=inicial
        arrcol.append(columnas[n])
        n=n+salto
        while len(arrcol)<cantidad:
            arrcol.append(columnas[n])
            n=n+1
        print arrcol
        salto=salto+1
    
    inicial=inicial+1

