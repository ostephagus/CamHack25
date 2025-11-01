# CamHack25 Repository
## Idea
To allow the user to search for a chemical molecule, then to be able to display this as an OpenStreetMap of coordinates.

## Components
### Frontend
Use WPF to create a windows app that allows the user to search for a specific molecule, returns search results in a list, then allows the user to choose the molecule they want to display.

### API Calls
Given the molecule name, return search results from the PubChem REST API. Once the user selects the specific molecule, use the API again to get the data on the molecule.

### Molecule-to-grid
Use a best-fit algorithm to convert the molecule position data to a grid of road intersections. Apply appropriate scaling/rotations to get a good fit.

### Visualisation
Given the set of coordinates of intersections, plot the points on a map.
