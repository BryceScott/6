import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.title("🚗 Shortest Path Finder - Town Navigation App")

# Define the graph using adjacency list
edges = {
    'Origin': {'A': 40, 'B': 60, 'C': 50},
    'A': {'B': 10, 'D': 70},
    'B': {'C': 20, 'D': 55, 'E': 40},
    'C': {'E': 50},
    'D': {'E': 10},
    'E': {'Destination': 60},
    'Destination': {}
}

# Create a directed graph
G = nx.DiGraph()

# Add edges and weights to the graph
for u in edges:
    for v, w in edges[u].items():
        G.add_edge(u, v, weight=w)

# Function to draw the graph with optional highlighted path
def draw_graph(path=None):
    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=14, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Highlight the shortest path
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)

    st.pyplot(plt)

# Calculate shortest path
try:
    path = nx.dijkstra_path(G, source='Origin', target='Destination')
    total_distance = nx.dijkstra_path_length(G, source='Origin', target='Destination')

    st.subheader("🔍 Shortest Path")
    st.write(" → ".join(path))
    st.write(f"📏 Total Distance: {total_distance} miles")

    st.subheader("🧭 Network Map")
    draw_graph(path)
except Exception as e:
    st.error(f"❌ Unable to find a path: {e}")
