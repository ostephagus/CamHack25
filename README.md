# CamHack25 Repository
## Idea
To allow the user to search for a chemical molecule, then to be able to display this as an OpenStreetMap of coordinates.

## Components
### Frontend
Use CLI or (if time) GUI to allow the user to specify a given molecule. If multiple search results exist, allow the user to choose the one they want.

### API Calls
Given the molecule name, search using the PubChem REST API to get the data on the molecule. Once the user has selected theirs, transfer the list of coordinates to the visualiser.

### Visualisation
Given the data about the molecule, transform these into mapping coordinates using the hexagon visualisation for compounds.
