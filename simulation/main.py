from geopy.distance import geodesic
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from typing import List, Tuple

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Define central location (Seoul)
central_point = (37.5665, 126.9780)

# Define 4 spatially spread hubs (Seoul, Incheon, Seongnam, Eastern Seoul)
hub_locations = [
    (37.5665, 126.9780),   # Seoul center
    (37.4563, 126.7052),   # Incheon
    (37.3219, 127.1265),   # Seongnam
    (37.5407, 127.0795),   # Eastern Seoul (Gwangjin)
]
hubs = hub_locations
num_hubs = len(hubs)

# Generate more widely spread edge nodes
num_nodes_large = 80
nodes_large = [(central_point[0] + np.random.normal(0, 0.1),
                central_point[1] + np.random.normal(0, 0.1)) for _ in range(num_nodes_large)]

# Define color map
colors = plt.cm.get_cmap('tab10', num_hubs)

# Function: Assign node to the closest hub (no capacity constraint)
def assign_nodes_to_closest_hub(nodes: List[Tuple[float, float]],
                                 hubs: List[Tuple[float, float]]) -> List[int]:
    assignments = []
    for node in nodes:
        distances = [geodesic(node, hub).km for hub in hubs]
        nearest_hub = np.argmin(distances)
        assignments.append(nearest_hub)
    return assignments

# Assign nodes
assignments_large = assign_nodes_to_closest_hub(nodes_large, hubs)

# Create DataFrames
df_nodes_large = pd.DataFrame(nodes_large, columns=['lat', 'lon'])
df_nodes_large['assigned_hub'] = assignments_large
df_hubs = pd.DataFrame(hubs, columns=['lat', 'lon'])
df_hubs['id'] = range(num_hubs)

# Plotting
fig, ax = plt.subplots(figsize=(10, 8))
for i in range(num_hubs):
    assigned = df_nodes_large[df_nodes_large['assigned_hub'] == i]
    ax.scatter(assigned['lon'], assigned['lat'], label=f'Hub {i} Nodes ({len(assigned)})', color=colors(i))
    ax.scatter(df_hubs.iloc[i]['lon'], df_hubs.iloc[i]['lat'], marker='X', s=150, color=colors(i), edgecolor='black', linewidth=1.5)

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Greedy Nearest Hub Assignment (80 Edge Nodes, Spatially Spread)')
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
ax.grid(True)
plt.tight_layout()
plt.show()
