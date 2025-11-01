import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt


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