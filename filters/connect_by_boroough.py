import pandas as pd

def create_boro_edges(nodes_csv, output_edges_csv):

    df = pd.read_csv(nodes_csv)
    edges = []
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            if df.iloc[i]['BORO'] == df.iloc[j]['BORO']:
                edges.append([df.iloc[i]['Id'], df.iloc[j]['Id'], "Undirected", 1])  # Create edge


    edges_df = pd.DataFrame(edges, columns=["Source", "Target", "Type", "Weight"])
    edges_df.to_csv(output_edges_csv, index=False)



# Example usage:
NODES_CSV = "outputs/nodes.csv"  # Replace with your nodes CSV file
OUTPUT_EDGES_CSV = "outputs/boro_edges.csv"

create_boro_edges(NODES_CSV, OUTPUT_EDGES_CSV)