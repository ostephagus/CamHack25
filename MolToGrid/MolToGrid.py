import json

## Read in the coordinates
with open('sample_data.json','r') as f:
    inputCoords = json.load(f)

print(inputCorods)
## Multiply coords by 10 and approximate coordinates as integers from origin
## Make a grid