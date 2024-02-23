## A simple vector autoregressive model that uses the graph structure as
## a prior for the model.

import numpy as np
import scipy.linalg as la
import scipy.sparse as sp
from icecream import ic

## We use igraph to represent the graph structure.
import igraph as ig

## GraphVar class contains a graph, and a parameter k for the dimension of the vectors generated.
## We generate a fake "time series", for each vertex u of the graph, we generate a vector of k
## for every time step.  Data is for seeding the model, it is currently not supported. kappa is the coupling coeffient
class GraphVar:
    def __init__(self, graph, k, data=None, lag=1, prior=None, kappa=0.01):
        self.graph = graph
        self.k = k
        self.lag = lag
        self.prior = prior
        self.data = data
        self.n = graph.vcount()
        self.kappa = kappa
        self._initialize_matrices()
    
    ## Create the VAR matrices from the graph. 
    def initialize_matrices(self):
        ## We use an uniform A matrix. 
        ## The model for each vertex u is a VAR model of the form:
        ## x(u)_t = A * x(u)_{t-1} + kappa* sum_{v in N(u)} w(u,v) * B * x(v)_{t-1} + noise
        ## Where A is the same for all vertices, and B is the coupling matrix, w is the edge weight.

        ## First we generate A, to be a random matrix with eigenvalues in the unit circle.
        A = np.random.rand(self.k, self.k)
        A = la.orth(A)
        A = A / np.abs(la.eigvals(A)).max()
        self.A = A

        ## We generate the coupling matrix B, to be a random matrix with eigenvalues in the unit circle.
        B = np.random.rand(self.k, self.k)
        B = la.orth(B)
        B = B / np.abs(la.eigvals(B)).max()
        self.B = B

    def intialize_vectors(self):
        ## We initialize the vectors for each vertex. A random vector is generated for each vertex.
        ## The random vector is generated from a normal distribution.
        self.x = [np.random.standard_normal(self.k) for i in range(self.n)]
    
    ## Generate one time step for the whole graph:
    def update(self):
        new_x = []
        for u in range(self.n):
            new_x.append(self.update_vertex(u))
        self.x = new_x

    ## Generate one time step for a single vertex.
    def update_vertex(self, u):
        ## We generate the sum of the coupling term.
        sum_coupling = np.zeros(self.k)
        for v in self.graph.neighbors(u):
            sum_coupling += self.graph[u,v] * self.B @ self.x[v]
        return self.A @ self.x[u] + self.kappa * sum_coupling + np.random.standard_normal(self.k)
    

    ## Generate a random time series for the graph.
    def generate_time_series(self, T):
        time_series = []
        for t in range(T):
            time_series.append([self.x[u] for u in range(self.n)])
            self.update()

if __name__ == "__main__":
    print("This is a module.")