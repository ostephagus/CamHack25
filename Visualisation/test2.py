import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import folium
coordinates = np.loadtxt('albCoordsOfMolecule.txt', dtype=float)


# get the boundary polygon for Albuquerque; project and plot it
city = ox.geocode_to_gdf("Albuquerque")
ax = city.plot(fc="gray", ec="none")
ax.axis("off")


# Set origin as Sam's Club 1421, Albuquerque
origin = (35.138511, -106.613554)

# Define a buffer distance around origin (in meters)
dist = 50000 # 50 km radius

# Retrieve street network graph within 500 km of origin
graph = ox.graph_from_point(origin, dist=dist, network_type='drive')

# Plot street network centred at origin
fig, ax = ox.plot_graph(graph, show=False, close=False)
plt.show()

# Convert graph to GeoDataFrames for nodes and edges
nodes, edges = ox.graph_to_gdfs(graph)

print("Edges GeoDataFrame columns:", edges.columns)
print("Number of streets:", len(edges))

# Create network around point of molecule; leave unsimplified for now
origin = (coordinates[0])
graph = ox.graph_from_point(origin, network_type='drive', dist=50000, simplify=False)
ox.plot_graph(graph, node_color="r", figsize=(5,5))

# Simplify the network by removing unnecessary nodes
graph = ox.simplify_graph(graph)
ox.plot_graph(graph, node_color="r", figsize=(5,5))

route = [(i[0], i[1]) for i in coordinates]
map = folium.Map((route[0][1],route[0][0]), zoom_start=13)
for pt in route:
    marker = folium.Marker([pt[1], pt[0]]) #latitude,longitude
    map.add_child(marker) 
map

# Create graph
graph = ox.graph_from_point(route[0],network_type='drive')
# Create path
path = []

for first, second in zip(route, route[1:]):
    one = ox.get_nearest_node(graph, first)
    two= ox.get_nearest_node(graph, second)
    path.append(nx.shortest_path(graph,one,two))
print(path)

# Plot
fig, ax = ox.plot_graph_routes(graph, path,edge_color='k', bgcolor='w')