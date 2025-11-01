# CamHack25 Repository
## Idea
To allow the user to search for a chemical molecule, then to be able to display this as an OpenStreetMap of coordinates.

## Components
### Frontend
Use WPF to create a windows app that allows the user to search for a specific molecule, returns search results in a list, then allows the user to choose the molecule they want to display.

### API Calls
Given the molecule name, return search results from the PubChem REST API. Once the user selects the specific molecule, use the API again to get the data on the molecule.

### Visualisation
Given the data about the molecule, transform these into mapping coordinates using the 2D hexagons visualisation for compounds.
