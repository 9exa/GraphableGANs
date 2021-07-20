
import tensorflow as tf
#functions to help encode/decode/manage data
#preferably not something that already exists in tensorflow

#returns cartesian product of 2 Tensors
def cartesian(a, b):
    assert(len(a.shape) == len(b.shape))
    if len(a.shape) == 1:
        c = tf.stack(tf.meshgrid(a, b, indexing = 'ij'), axis = 2)
        c = tf.reshape(c, (-1, 2))
        return c
    else:
        na, nb = tf.range(a.shape[0]), tf.range(b.shape[0])
        c = tf.stack(tf.meshgrid(na, nb, indexing = 'ij'), axis = -1)
        c = tf.reshape(c, (-1, 2))
        #gets cords of combinations of a and b and slaps em together
        # in a map function. probably inefficient
        t = c[0]
        return tf.map_fn(lambda t : tf.stack([a[t[0]], b[t[1]]]), c,
                dtype = a.dtype)
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

def sparseToDense():
    pass
def coarser():
    pass
