from geopy.distance import geodesic
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from typing import List, Tuple

# seed= 42
seed= 38

# Set random seed for reproducibility
random.seed(seed)
np.random.seed(seed)

# Define central location (Seoul)
central_point = (37.5665, 126.9780)

# Define 4 spatially spread hubs (Seoul, Incheon, Seongnam, Eastern Seoul)
hub_locations = [
    (37.5665, 126.9780),   # Hub 0 - Seoul center
    (37.4563, 126.7052),   # Hub 1 - Incheon (Now GPU-specialized)
    (37.3219, 127.1265),   # Hub 2 - Seongnam
    (37.5407, 127.0795),   # Hub 3 - Eastern Seoul
]
hubs = hub_locations
num_hubs = len(hubs)
hub_roles = ['cpu', 'gpu', 'cpu', 'cpu']  # Hub 1 is now GPU-specialized

# Generate 80 evenly and widely dispersed edge nodes
num_nodes_even = 80
lat_range = (37.3, 37.7)
lon_range = (126.7, 127.2)
nodes_even = [(np.random.uniform(lat_range[0], lat_range[1]),
               np.random.uniform(lon_range[0], lon_range[1])) for _ in range(num_nodes_even)]

# Randomly assign 4 GPU-demanding nodes
gpu_indices_even = random.sample(range(num_nodes_even), 4)
node_roles_even = ['gpu' if i in gpu_indices_even else 'cpu' for i in range(num_nodes_even)]

# Define color map
colors = plt.cm.get_cmap('tab10', num_hubs)

# Role-aware assignment function
def assign_nodes_with_gpu_preference(nodes: List[Tuple[float, float]],
                                     hubs: List[Tuple[float, float]],
                                     node_roles: List[str],
                                     hub_roles: List[str]) -> List[int]:
    assignments = []
    for i, node in enumerate(nodes):
        role = node_roles[i]
        if role == 'gpu':
            gpu_hubs = [j for j, r in enumerate(hub_roles) if r == 'gpu']
            distances = [(j, geodesic(node, hubs[j]).km) for j in gpu_hubs]
        else:
            distances = [(j, geodesic(node, hub).km) for j, hub in enumerate(hubs)]
        nearest_hub = min(distances, key=lambda x: x[1])[0]
        assignments.append(nearest_hub)
    return assignments

# Apply assignment
assignments_even = assign_nodes_with_gpu_preference(nodes_even, hubs, node_roles_even, hub_roles)

# Create DataFrames
df_nodes_even = pd.DataFrame(nodes_even, columns=['lat', 'lon'])
df_nodes_even['assigned_hub'] = assignments_even
df_nodes_even['role'] = node_roles_even
df_hubs = pd.DataFrame(hubs, columns=['lat', 'lon'])
df_hubs['id'] = range(num_hubs)
df_hubs['role'] = hub_roles

# Plotting with larger font and legend-based hub labeling only
# plt.style.use('seaborn-white')
fig, ax = plt.subplots(figsize=(10, 8))

for i in range(num_hubs):
    assigned = df_nodes_even[df_nodes_even['assigned_hub'] == i]
    ax.scatter(assigned['lon'], assigned['lat'],
               label=f'Hub {i+1} ({hub_roles[i]}) - {len(assigned)} nodes',
               color=colors(i), s=50, alpha=0.9, edgecolor='k', linewidth=0.3)
    ax.scatter(df_hubs.iloc[i]['lon'], df_hubs.iloc[i]['lat'],
               marker='X', s=180, color=colors(i), edgecolor='black', linewidth=1.5)

# Dummy entries for legend
ax.scatter([], [], marker='o', color='gray', label='Edge Node', s=50)
ax.scatter([], [], marker='X', color='gray', label='Hub', s=100)

# Labels and title
ax.set_xlabel('Longitude', fontsize=14)
ax.set_ylabel('Latitude', fontsize=14)
ax.set_title('Hub-based Grouping Algorithm Simulation', fontsize=16, fontweight='bold')

# Grid and legend
ax.grid(True, linestyle='--', linewidth=0.5)
ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0., fontsize=12)
ax.tick_params(axis='both', labelsize=12)

plt.tight_layout()
plt.show()
