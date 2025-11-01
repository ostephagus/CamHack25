import json
import matplotlib.pyplot as plt

## Read in the coordinates
with open('sample_data.json','r') as f:
    inputCoords = json.load(f)

# Idea: Have some way to represent different elements differently?
for atom1 in inputCoords:
   nodeNum=atom1['idx']
   atom1Coords = [atom1['x'],atom1['y']]
   for i in atom1['bonds']:
        i=int(i)
        if i>nodeNum:
            atom2 = inputCoords[i]
            atom2Coords = [atom2['x'],atom2['y']]
            plt.plot([atom1Coords[0],atom2Coords[0]],[atom1Coords[1],atom2Coords[1]],'ro-')

plt.show()
## Multiply coords by 10 and approximate coordinates as integers from origin
## Make a grid