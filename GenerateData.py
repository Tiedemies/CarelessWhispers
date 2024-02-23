## Now we generate time series data for a random graph.

import numpy as np
import scipy.linalg as la
import scipy.sparse as sp
from icecream import ic
import igraph as ig

import pandas as pd

from GraphVar import GraphVar
from GraphGen import BarabasiAlbert


if __name__ == "__main__":
    n = 100
    m = 2
    k = 3
    g = BarabasiAlbert(n, m)
    ## Generate random weights for the edges.
    g.es["weight"] = np.random.rand(g.ecount())
    ic(g)

    ## Save the graph to a file.
    g.write("graph.gml", format="gml")

    ## Create a graph variable model.
    model = GraphVar(g, k, kappa=0.1)
    model.initialize_matrices()
    model.intialize_vectors()
    ## Generate a time series of length 100.
    L = []
    for i in range(100):
        model.update()
        L.append(model.x)
    ## Create a pandas dataframe from the time series.
    df = pd.DataFrame(L)
    ## Name the columns accoring to the graph vertex numbers:
    df.columns = [str(i) for i in range(n)]
    ## Save the time series to a file.
    df.to_csv("timeseries.csv", index=False)
