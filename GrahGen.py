## Generate random graphs with different models.

import numpy as np
import scipy.linalg as la
import scipy.sparse as sp
import igraph as ig

def ErdosRenyi(n, p):
    return ig.Graph.Erdos_Renyi(n, p)

def BarabasiAlbert(n, m):
    return ig.Graph.Barabasi(n, m)


