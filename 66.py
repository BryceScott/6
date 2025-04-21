import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Shortest Path Finder", layout="wide")
st.title("🚗 Shortest Path Finder with Custom Distance Matrix")

# Define nodes
towns = ['Origin', 'A', 'B', 'C', 'D', 'E', 'Destination']

# Editable distance matrix (initial values from original problem)
default_data = pd.DataFrame(np.nan, index=towns, columns=towns)
default_data.loc['Origin', ['A', 'B', 'C']] = [40, 60, 50]
default_data.loc['A', ['B', 'D']] = [10, 70]
default_data.loc['B', ['C', 'D', 'E']] = [20, 55, 40]
default_data.loc['C', 'E'] = 50
default_data.loc['D', 'E'] = 10
default_data.loc['E', 'Destination'] = 60

st.subheader("🛠️ Edit Distances (Leave blank for no direct road)")
distance_df = st.data_editor(
    default_data,
    use_container_width=True,
    key="matrix_editor"
)

# Create graph from edited matrix
G = nx.DiGraph()

for from_node in towns:
    for to_node in towns:
        weight = distance_df.loc[from_node, to_node]
        if pd.notna(weight):
            G.add_edge(from_node, to_node, weight=float(weight))

# Calculate shortest path
try:
    path = nx.dijkstra_path(G, source='Origin', target='Destination')
    total_distance = nx.dijkstra_path_length(G, source='Origin', target='Destination')

    st.subheader("🔍 Shortest Path")
    st.success(" → ".join(path))
    st.write(f"📏 Total Distance: `{total_distance}` miles")

    # Draw graph
    st.subheader("📍 Route Visualization")
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(10, 6))
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color="skyblue", arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Highlight path
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
    st.pyplot(fig)

except nx.NetworkXNoPath:
    st.error("❌ No path found from Origin to Destination. Please check your input.")
except Exception as e:
    st.error(f"Error: {e}")
