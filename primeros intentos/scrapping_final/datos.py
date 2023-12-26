


f = open("datos.txt","r")
for row in f:
    x =row.replace("\n","")
    v = x.split(";")
    print(v[1]+";"+v[4])