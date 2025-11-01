## Used to produce the coordinates of intersections in Albuquerque
## With respect to Betsy Patterson swimming pool (rough centre of city)
origin = [35.11938316384773, -106.55848652294833] ## Coords of the pool
with open('albuquerqueNum.json','r') as f:
    gridCoords = np.array(ast.literal_eval(f.read()))

