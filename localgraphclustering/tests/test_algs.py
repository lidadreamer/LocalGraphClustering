from localgraphclustering import *
import time

def test_algs():

    # Read graph. This also supports gml and graphml format.
    g = GraphLocal("localgraphclustering/tests/data/dolphins.edges",separator=" ")

    # Call the global spectral partitioning algorithm.
    output_sp = fiedler(g)

    # Only one input graph is given, i.e., [g].
    # Extract the array from position 0 and store it.
    eig2 = output_sp

    # Round the eigenvector
    output_sc = sweep_cut(g,eig2)

    # Extract the partition for g and store it.
    eig2_rounded = output_sc[0]

    # Conductance before improvement
    print("Conductance before improvement:",g.compute_conductance(eig2_rounded))
    #print(eig2_rounded)

    # Start calling SimpleLocal
    start = time.time()
    output_SL = SimpleLocal(g,eig2_rounded)
    end = time.time()
    print("running time:",str(end-start)+"s")
    print(output_SL)

    # Conductance after improvement
    print("Conductance after improvement:",g.compute_conductance(output_SL[0]))

    # Compute triangle clusters and cluster metrics
    cond,cut,vol,cc,t = triangleclusters(g)
    minverts, minvals = g.local_extrema(cond,True)
    print("vertices with minimum conductance neighborhood:",minverts)

def test_fiedler():
    import numpy as np
    g = GraphLocal("localgraphclustering/tests/data/dolphins.edges",separator=" ")
    output_sp = fiedler(g)
    R = [1]
    R.extend(g.neighbors(R[0]))
    output_sp2 = fiedler_local(g,R)
    assert(np.all(output_sp2[0][1] >= -1.0e-6)) # make sure everything is almost positive. 
    
def test_fiedler_local():    
    g = GraphLocal("localgraphclustering/tests/data/dolphins.edges",separator=" ")
    R = [1]
    R.extend(g.neighbors(R[0]))
    phi0 = g.set_scores(R)["cond"]
    sparse_vec = fiedler_local(g,R)[0]
    S = sweep_cut(g,sparse_vec)[0]
    phi1 = g.set_scores(S)["cond"]
    assert(phi1 <= phi0)
    
    S = spectral_clustering(g, R, method="fiedler_local")[0]
    phi1 = g.set_scores(S)["cond"]
    assert(phi1 <= phi0)
    
    

def test_sweep_cut():
    g = GraphLocal("localgraphclustering/tests/data/dolphins.edges",separator=" ")
    sweep_cut(g,([1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]))

def test_spectral_clustering():
    g = GraphLocal("localgraphclustering/tests/data/dolphins.edges",separator=" ")
    output_sp = fiedler(g)
    R = [1]
    R.extend(g.neighbors(R[0]))
    insize = len(R)
    output_sp2 = spectral_clustering(g,R,method="fiedler_local")[0]
    Z = set(R).union(output_sp2)
    assert(len(Z) == insize)
