import numpy as np

alb = np.loadtxt("albNP.txt",dtype=float)

print(len(alb))

print(min(alb[:,0]),min(alb[:,1]), max(alb[:,0]), max(alb[:,1]))

tolerance = 0

# Trying to see just how tight we can keep the coordinates around Alberquerque while still getting a nice graph
while tolerance < 2.625:
    tolerance += 0.105
    albFiltered = []

    for i in alb:
        if 34.955694-tolerance < i[0] < 35.274869+tolerance and -106.7270000-tolerance < i[1] < -106.572076+tolerance:
            albFiltered.append(i)

    with open(f"filtereds/albNPFiltered{tolerance}.txt","w+") as f:
        for i in albFiltered:
            f.write(str(float(i[0]))+" "+str(float(i[1]))+"\n")