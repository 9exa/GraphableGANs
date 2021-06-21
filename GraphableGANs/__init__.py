<<<<<<< HEAD
#importing children
from . import layers
from .models import *
from . import prebuilt
#import importlib
#importlib.reload(layers)

import tensorflow as tf
from tensorflow.keras.layers import Layer
from time import time
#returns adjacency matricies filled with features of verts instead of 0s and 1s
@tf.function
def featurizedAdjacency(adjM, feat):
    return tf.repeat(tf.expand_dims(feat, 1), adjM.shape[1], 1) * tf.expand_dims(adjM, -1)

#One-off functions
@tf.function
def minMaxAngle(graphs):
    #takes a list of vectors, returns a tensor containing the min and max
    #angles between all pairs of those vectors
    def vecMibMaxAngles(vectors):
        def angleBetween(vs):
            v, u = vs[0], vs[1]
            if (tf.math.count_nonzero(v) * tf.math.count_nonzero(u)
                    * tf.math.count_nonzero(v-u)) != 0:

                return tf.math.acos([tf.tensordot(u,v, 1) / (tf.norm(v)*tf.norm(u))])
            else:
                return tf.constant([float("NaN")])
        g = cProduct(vectors, vectors)
        # print(tf.map_fn(angleBetween, g))
        p= tf.map_fn(angleBetween, g, parallel_iterations = 16)
        # print("p:", p)
        # p = tf.concat([p,[ 4.0, -1.0]], 0)
        minimum = tf.reduce_min(p)
        maximum = tf.reduce_max(p)
        # print([minimum, maximum])
        return tf.stack([minimum, maximum])
    #cartesian Product of two tensors https://stackoverflow.com/questions/47132665/cartesian-product-in-tensorflow/50195230
    def cProduct(a, b):
        return tf.stack([tf.repeat(a, b.shape[0], 0),
                tf.concat(a.shape[0]*[b],0)], 1)
    adjMs = graphs[0]
    feats = graphs[1]
    verts = adjMs.shape[1]
    mask = tf.expand_dims(adjMs, axis = -1)
    startFeat = tf.repeat(tf.expand_dims(feats, axis = 2), verts, 2)
    endFeat = tf.repeat(tf.expand_dims(feats, axis = 1), verts, 1)
    diffs = (endFeat - startFeat) * mask
    out = tf.stop_gradient(tf.map_fn(lambda x: tf.map_fn(vecMibMaxAngles, x),
            diffs, parallel_iterations = 20))
    return out

#returns the min and max squared difference of every vector element
@tf.function
def minMaxSquaredDiff(graphs):
    adjMs = graphs[0]
    feats = graphs[1]
    verts = adjMs.shape[1]
    mask = tf.expand_dims(adjMs, axis = -1)
    startFeat = tf.repeat(tf.expand_dims(feats, axis = 2), verts, 2)
    endFeat = tf.repeat(tf.expand_dims(feats, axis = 1), verts, 1)
    diffs = (endFeat - startFeat) * mask
    out = (tf.concat([tf.reduce_min(diffs * diffs , 2),
            tf.reduce_max(diffs * diffs , 2)], -1))
    return out
@tf.function
def minMaxDist(graphs):
    adjMs = graphs[0]
    feats = graphs[1]
    verts = adjMs.shape[1]
    mask = tf.expand_dims(adjMs, axis = -1)
    startFeat = tf.repeat(tf.expand_dims(feats, axis = 2), verts, 2)
    endFeat = tf.repeat(tf.expand_dims(feats, axis = 1), verts, 1)
    diffs = (endFeat - startFeat) * mask
    diffs = tf.where(diffs == 0, float("NaN"), diffs)

    out = (tf.concat([tf.reduce_min(tf.norm(diffs, axis = -1, keepdims=True),2),
            tf.reduce_max(tf.norm(diffs, axis = -1, keepdims=True), 2)], -1))
    return out


print("Import success")
=======
#importing children
from . import layers
from .models import *
from . import prebuilt
#import importlib
#importlib.reload(layers)

import tensorflow as tf
from tensorflow.keras.layers import Layer
from time import time
#returns adjacency matricies filled with features of verts instead of 0s and 1s
@tf.function
def featurizedAdjacency(adjM, feat):
    return tf.repeat(tf.expand_dims(feat, 1), adjM.shape[1], 1) * tf.expand_dims(adjM, -1)

#One-off functions
@tf.function
def minMaxAngle(graphs):
    #takes a list of vectors, returns a tensor containing the min and max
    #angles between all pairs of those vectors
    def vecMibMaxAngles(vectors):
        def angleBetween(vs):
            v, u = vs[0], vs[1]
            if (tf.math.count_nonzero(v) * tf.math.count_nonzero(u)
                    * tf.math.count_nonzero(v-u)) != 0:

                return tf.math.acos([tf.tensordot(u,v, 1) / (tf.norm(v)*tf.norm(u))])
            else:
                return tf.constant([float("NaN")])
        g = cProduct(vectors, vectors)
        # print(tf.map_fn(angleBetween, g))
        p= tf.map_fn(angleBetween, g, parallel_iterations = 16)
        # print("p:", p)
        # p = tf.concat([p,[ 4.0, -1.0]], 0)
        minimum = tf.reduce_min(p)
        maximum = tf.reduce_max(p)
        # print([minimum, maximum])
        return tf.stack([minimum, maximum])
    #cartesian Product of two tensors https://stackoverflow.com/questions/47132665/cartesian-product-in-tensorflow/50195230
    def cProduct(a, b):
        return tf.stack([tf.repeat(a, b.shape[0], 0),
                tf.concat(a.shape[0]*[b],0)], 1)
    adjMs = graphs[0]
    feats = graphs[1]
    verts = adjMs.shape[1]
    mask = tf.expand_dims(adjMs, axis = -1)
    startFeat = tf.repeat(tf.expand_dims(feats, axis = 2), verts, 2)
    endFeat = tf.repeat(tf.expand_dims(feats, axis = 1), verts, 1)
    diffs = (endFeat - startFeat) * mask
    out = tf.stop_gradient(tf.map_fn(lambda x: tf.map_fn(vecMibMaxAngles, x),
            diffs, parallel_iterations = 20))
    return out

#returns the min and max squared difference of every vector element
@tf.function
def minMaxSquaredDiff(graphs):
    adjMs = graphs[0]
    feats = graphs[1]
    verts = adjMs.shape[1]
    mask = tf.expand_dims(adjMs, axis = -1)
    startFeat = tf.repeat(tf.expand_dims(feats, axis = 2), verts, 2)
    endFeat = tf.repeat(tf.expand_dims(feats, axis = 1), verts, 1)
    diffs = (endFeat - startFeat) * mask
    out = (tf.concat([tf.reduce_min(diffs * diffs , 2),
            tf.reduce_max(diffs * diffs , 2)], -1))
    return out
@tf.function
def minMaxDist(graphs):
    adjMs = graphs[0]
    feats = graphs[1]
    verts = adjMs.shape[1]
    mask = tf.expand_dims(adjMs, axis = -1)
    startFeat = tf.repeat(tf.expand_dims(feats, axis = 2), verts, 2)
    endFeat = tf.repeat(tf.expand_dims(feats, axis = 1), verts, 1)
    diffs = (endFeat - startFeat) * mask
    diffs = tf.where(diffs == 0, float("NaN"), diffs)

    out = (tf.concat([tf.reduce_min(tf.norm(diffs, axis = -1, keepdims=True),2),
            tf.reduce_max(tf.norm(diffs, axis = -1, keepdims=True), 2)], -1))
    return out


print("Import success")
>>>>>>> 523aa83195ddb6e076d66f660f7be7dc55a96411
