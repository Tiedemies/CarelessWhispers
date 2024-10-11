## Generate random graphs with different models.

import numpy as np
import scipy.linalg as la
import scipy.sparse as sp
import networkx as nx

## Erdös-Rényi model
def ErdosRenyi(n, p):
    return ig.Graph.Erdos_Renyi(n, p)

## Barabási-Albert model
def BarabasiAlbert(n, m):
    return ig.Graph.Barabasi(n, m)

## Block model: n = Number of vertices, k = number of blocks, p = probability of intra-block edge, q = probability of inter-block edge
def BlockModel(n,k,p:float = 0.5,q:float = 0.1):

    ## Generate a graph of n vertices, no edges first:
    g = nx.Graph()
    g.add_nodes_from(range(n))
    ## Generate the block structure: Randomly assign each vertex to a block 0,1,2,...,k-1
    blocks = [[] for i in range(k)]
    for i in range(n):
        blocks[np.random.randint(k)].append(i)

    # Generate a random spanning tree for each block:
    for block in blocks:
        if len(block) > 1:           
            root = block[np.random.randint(len(block))]
            treevert = [root]
            for i in block:
                if i != root:
                    g.add_edge(i,treevert[np.random.randint(len(treevert))])
                    treevert.append(i)
    
    ## Generate the edges inside each block:
    for block in blocks:
        for i in block:
            for j in block:
                if i < j and np.random.rand() < p:
                    ## If the edge is not already there, add it.
                    if not g.has_edge(i,j):
                       g.add_edge(i,j)

    # Generate a spanning tree of blocks
    for i in range(1,k):
        # First pick a random block less than i:
        j = np.random.randint(i)
        # Then pick a random vertex from each block and connect them:
        u = blocks[i][np.random.randint(len(blocks[i]))]
        v = blocks[j][np.random.randint(len(blocks[j]))]
        g.add_edge(u,v)
 
    ## Generate the edges between the blocks:
    for i in range(k):
        for j in range(i+1,k):
            for u in blocks[i]:
                for v in blocks[j]:
                    if np.random.rand() < q/(len(blocks[i])*len(blocks[j])):
                        # If there is no edge between u and v, add it.
                        if not g.has_edge(u,v):
                            g.add_edge(u,v)
    return g



