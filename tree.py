import networkx as nx
from pyvis.network import Network

def build_tree(instructions):
    G = nx.DiGraph()
    def add_nodes(instr_list, parent_id):
        for i, instr in enumerate(instr_list):
            node_id = f"{parent_id}-{i}"
            if instr[0] == 'while':
                G.add_node(node_id, label=f"{instr[0]} {instr[1]}", shape='box')
                G.add_edge(parent_id, node_id)
                add_nodes(instr[2], node_id)
            else:
                G.add_node(node_id, label=f"{instr[0]} {instr[1]}")
                G.add_edge(parent_id, node_id)

    root_id = "root"
    G.add_node(root_id, label="root", shape='ellipse')
    add_nodes(instructions, root_id)
    return G

def visualize_tree(instructions):
    G = build_tree(instructions)
    net = Network(notebook=True)
    net.from_nx(G)
    return net

def display_tree(instructions):
    net = visualize_tree(instructions)
    return net.generate_html()
