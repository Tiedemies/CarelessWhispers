## Now we generate time series data for a random graph.

import numpy as np
import scipy.linalg as la
import scipy.sparse as sp
from icecream import ic
import networkx as nx
import matplotlib.pyplot as plt

import pandas as pd

from GraphSimpleVar import GSV
from GraphGen import BarabasiAlbert, ErdosRenyi, BlockModel

def GenerateData(n = 10,k = 3,T = 1000) -> tuple[nx.Graph, list]:
    kb = n//3
    g = BlockModel(n, kb, 0.5, 0.1)
    # Make the graph non-directed.
    g.to_undirected()
    model = GSV(g, k)
    data = model.generateDataSIN(T)
    return (g,data)

if __name__ == "__main__":
    trialname = "Trial3"
    n = 10
    k = 3
    T = 1000
    [g,data] = GenerateData(n,k, T)
    ## Visualize the graph and data in one plot.
    ## Create k+1 subplots.
    fig, axs = plt.subplots(k+1,1)
    ## Plot the graph in the first subplot.
    nx.draw(g, ax = axs[0])
    axs[0].set_title("Graph")
    ## Plot the data in the remaining subplots.
    for i in range(k):
        axs[i+1].plot(data[:,:,i])
        axs[i+1].set_title(f"Layer {i}")
    plt.show()
    ## Save the data to a csv file.
    ## Each layer in a separate csv file, name being trialname_Layer_i.csv
    ## Index is Time, columns are vertices.
    for i in range(k):
        df = pd.DataFrame(data[:,:,i])
        df.to_csv(f"{trialname}_Layer_{i}.csv")
    ## Save the graph to a gml file.
    nx.write_gml(g, f"{trialname}_graph.gml")
    