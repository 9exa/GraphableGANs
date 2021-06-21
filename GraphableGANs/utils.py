import tensorflow as tf
#functions to help encode/decode/manage data
#preferably not something that already exists in tensorflow

#turns a multi-edged graphs to a simple graphs (edgelist to adjmatrix)
def multiToSimple(graphs, handleMults = "ignore"):
    #"ignore" treats multiple connections as 1
    #"add" counts up multiple connections
    out = []
    for g in graphs:
        n = len(g)
        out.append(list(tf.zeroes([n,n])))
        for e in g.edges:
            out[-1][e[0]][e[1]] = 1
    return out
