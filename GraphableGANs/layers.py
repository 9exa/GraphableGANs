
import tensorflow as tf
from GraphableGANs import utils
#relative imports are scary, as you can't import submodules diresctly

#call takes in tuple, first element is tensor of adjacencies,
#second is tensor of features
class GraphLayer(tf.keras.layers.Layer):
    #edgeType determines method of node exploration
    def __init__(self, edgeType = "AdjMatrix", **kwargs):
        super(GraphLayer, self).__init__(kwargs)
        self.edgeType = edgeType
    def build(self, inputShape):
        super(GraphLayer, self).build(inputShape)
    def __tostring__(self):
        return "a GG Layer"




#layer that appends outputs to one-off Functions to
class PoolFeatures(GraphLayer):
    def __init__(self, *functions, **kwargs):
        super(PoolFeatures, self).__init__(trainable=False)
        self.functions = functions
    def call(self, inputs):
        adjMs = inputs[0]
        feats = inputs[1]
        newFeats = [f(inputs) for f in self.functions]
        # print(feats)
        # print(newFeats)
        return(adjMs, tf.concat([feats] + newFeats, axis = -1))
#bfs for every node a certain depth and adds transversed features based on weights

class VertConvolution(GraphLayer):
    def __init__(self, depth = 1, weights = None, edgeType = "Simple",
            trainable = False):
        """
        TODO edgeType can be:
            'Simple' - vertex features multiplied by weights
            'Multi' - vertex features multiplied by value in adjacency
            'Catagorical' - different weight matrix for each catagory
            'Feature' - edge features undergo bilinear transformation to change
            into the shape of vertex features, then multiplies as wee
        """
        super(VertConvolution, self).__init__(trainable=trainable)
        if weights != None:
            self.w = tf.Tensor(weights)
        else:
            self.w = tf.Variable(initial_value = 0.5 ** tf.range(depth + 1,
                    dtype = "float32"), trainable = True)
        self.depth = depth
        self.edgeType = edgeType
    def call(self, inputs):
        adjMs = inputs[0]
        feats = inputs[1]
        #performs the breadth-first-search via matrix multiplications
        #try to avoid for loops in python

        #travels - nodes connected at nth step powers of the adjacency matrix
        # @tf.function
        def excludePrior(x, y):
            return tf.where(tf.math.logical_and(y != 0, x == 0), y, 0.)
        id = tf.eye(adjMs.shape[1], batch_shape=[1, adjMs.shape[0]])
        #adjMs += id
        travels = tf.repeat(tf.expand_dims(adjMs, 0), self.depth, axis = 0)
        travels = tf.scan(tf.matmul, tf.concat([id, travels], axis = 0))
        #delete repeat nodes
        travels = tf.scan(excludePrior, travels, reverse = True)

        travels = tf.where(travels == 0, 0.0, 1.0)#normalize adjacencies to one

        # print(travels)
        collection = tf.map_fn(lambda x: tf.matmul(x, feats), travels)
        # print(self.w.shape, collection.shape)
        s = collection * self.w[:, tf.newaxis, tf.newaxis, tf.newaxis]
        # print(s.shape)
        out = tf.reduce_sum(s, axis = 0)


        return (adjMs, out)
    def callOG(self, inputs):
        adjMs = inputs[0]
        feats = inputs[1]
        out = self.w[0]
        visited = tf.eye(adjMs[-1], batch_shape[:-2])

        for d in range(self.depth):

            frontier = tf.clip_by_value(tf.matmul(visited, adjMs)
                    - verts * visited, tf.zeros(1), tf.ones(1))
            out = out + self.w[1 + d] * tf.matmul(frontier, feats)
            # print(visited)
            visited = visited + frontier
        return out

class AvgSquareDiff(GraphLayer):
    def __init__(self, keepOriginals = True):
        super(AvgSquareDiff, self).__init__(trainable=False, dynamic = False)
        self.build(None)
        self.keepOrigionals=keepOriginals
    def build(self, guhh):
        pass
    def call(self, inputs):
        adjMs = inputs[0]
        feats = inputs[1]
        startFeats =tf.repeat(tf.expand_dims(feats, 2), 8, 2)
        endFeats = tf.repeat(tf.expand_dims(feats, 1), 8, 1)
        squaredDiffs = (startFeats - endFeats) ** 2 * tf.expand_dims(adjMs, -1)
        sums = tf.reduce_sum(squaredDiffs, 2)
        ns = tf.reduce_sum(adjMs, 2, True)

        out = sums / ns
        if self.keepOrigionals:
            out = tf.concat([feats, out],-1)
        return (adjMs, out)

class VarDiff(GraphLayer):
    def __init__(self, keepOriginals = True):
        super(VarDiff, self).__init__(trainable=False, dynamic = False)
        self.build(None)
        self.keepOrigionals=keepOriginals
    def call(self, inputs):
        adjMs = inputs[0]
        feats = inputs[1]
        mask = tf.expand_dims(adjMs, -1)
        startFeats =tf.repeat(tf.expand_dims(feats, 2), 8, 2)
        endFeats = tf.repeat(tf.expand_dims(feats, 1), 8, 1)
        x = ((startFeats - endFeats) * mask)
        sums = tf.reduce_sum(x, 2)
        ns = tf.reduce_sum(adjMs, 2, True)
        out = tf.reduce_sum(((x-tf.expand_dims(sums / ns, 2))
                 * mask) ** 2, 2) / (ns-1)
        if self.keepOrigionals:
            out = tf.concat([feats, out],-1)
        return (adjMs, out)

class MinAndMax(GraphLayer):
    def __init__(self, keepOriginals = True):
        super(MinAndMax, self).__init__(trainable=False, dynamic = False)
        self.build(None)
        self.keepOriginals=keepOriginals
    def build(self, guhh):
        pass
    def call(self, inputs):
        #print(inputs)
        adjMs = inputs[0]
        feats = inputs[1]
        featMat = featurizedAdjacency(adjMs, feats)
        mins = tf.reduce_min(featMat, 2)
        maxs = tf.reduce_max(featMat, 2)
        out = tf.concat([mins, maxs], -1)
        #print(out)
        if self.keepOriginals:
            out = tf.concat([feats, out], -1)
        return (adjMs, out)
#multiplies all verticies by it's internal matrix
class VertMult(GraphLayer):
    def __init__(self, inOutShape):
        super(VertMult, self).__init__()
        self.w = self.add_weight(shape=inOutShape, initializer='random_normal', dtype="float32")

    def build(self, inOutShape):
        pass
    def call(self, inputs):
        if not isinstance(inputs, (list, tuple)):
              raise ValueError('A graph layer should be called on a list of inputs.')
        adjMs = inputs[0]
        features = inputs[1]
        return (adjMs, tf.matmul(features, self.w))
class DropAdj(GraphLayer):
    def __init__(self, toList = False):
        super(DropAdj, self).__init__(trainable=False)
        self.toList = toList
    def call(self, inputs):
        if self.toList:
            return list(inputs[1])
        else:
            return inputs[1]
class DropFeat(GraphLayer):
    def __init__(self):
        super(DropFeat, self).__init__(trainable=False)
    def call(self, inputs):
        return inputs[0]
class EmbedFeatures(GraphLayer):
    def __init__(self, method = "average"):
        super(EmbedFeatures, self).__init__(trainable=False)
        self.method = method
    def call(self, inputs):
        if self.method == "max":
            pass
        elif self.method == "average":
            return tf.reduce_mean(inputs, -2)

#generates adjacency matrix from the features using some bilnear weights
class BiDenseAdjacency(GraphLayer):
    def __init__(self, activation = "linear", invertProb = False, **kwargs):
        super(BiDenseAdjacency, self).__init__(kwargs, trainable=True)
        self.activation = tf.keras.activations.deserialize(activation)
        self.invert = invertProb
    def build(self, inputShape):
        nFeats = inputShape[1][-1] #number of features per vertex
        self.w = self.add_weight(shape = (nFeats, nFeats),
                            initializer = "random_normal",
                            trainable = True)
        self.b = self.add_weight(shape = (1,), trainable = True)


    def call(self, graphs):
        adjMs = graphs[0]
        feats = graphs[1]
        y = self.activation(tf.map_fn(self.getAdj, feats))
        """if this is true, y is interperated as the probability that a edge
        exists, which is is in inverted by the true adjacency matrix
        and interperated as the probablity that the graph is real"""
        if self.invert == True:
            y = 1- (adjMs - y) ** 2
        return (y, feats)

    def getAdj(self, verts):
        def biLinMult(u, v, W, b): #we'll use this
            c = tf.tensordot(u, W, 1)
            return tf.tensordot(c, v, 1) + b
            #the dot product but with W in the middle
        N = verts.shape[0] #number of verticies
        indicies = utils.cartesian(tf.range(N), tf.range(N))
        d = tf.map_fn(lambda t: biLinMult(verts[t[0]],
                                    verts[t[1]],
                                    self.w, self.b),
                indicies, dtype = "float32")
        return tf.reshape(d, (N, N))

#adjacency using normal linear layers and concatenate
class DenseAdjacency(GraphLayer):
    def __init__(self, activation = "linear", invertProb = False, **kwargs):
        super(DenseAdjacency, self).__init__(kwargs, trainable=True)
        self.activation = tf.keras.activations.deserialize(activation)
        self.invert = invertProb
    def build(self, inputShape):
        nFeats = inputShape[1][-1] #number of features per vertex
        self.w = self.add_weight(name = "weights",
                            shape = (1, nFeats*2),
                            initializer = "random_normal",
                            trainable = True)
        self.b = self.add_weight(name = "bias", shape = (1,), trainable = True)
        super(DenseAdjacency, self).build(inputShape)

    def getAdj(self, verts):
        def helper(t):
            v = tf.concat([t[0], t[1]],0)
            return tf.tensordot(self.w, v, 1) + self.b
        #the dot product but with W in the middle
        N = verts.shape[0]
        combs = utils.cartesian(verts, verts)
        d = tf.map_fn(helper, combs, dtype = "float32")
        return tf.reshape(d, (N, N))
    def call(self, graphs):
        adjMs = graphs[0]
        feats = graphs[1]
        y = self.activation(tf.map_fn(self.getAdj, feats))
        """if this is true, y is interperated as the probability that a edge
        exists, which is is in inverted by the true adjacency matrix
        and interperated as the probablity that the graph is real"""
        if self.invert == True:
            y = (adjMs - y) ** 2
        return (y, feats)

class NeuralFP(GraphLayer):
    pass
class DeepWalk(GraphLayer):
    #Ahash iw a function that (for each vertex v) maps a point in (0, 1) to a vertex adj of v
    def createAhash(G):
        from math import ceil
        potNext = []
        for v in range(len(G)):
            p = []
            for u in range(len(G[v])):
                if G[v][u]:
                    p.append(u)
            if len(p) == 0:
                p.append(v)
            potNext.append(p)
        return lambda v, x: potNext[v][ceil(len(potNext[v]) * x)-1]
    def randomWalk(Ahash, nv, d):
        walks = [tf.range(0, nv)]
        for i in range(d):
            out.append(tf.map_fn(Ahash, walks[i]))
        return tf.constant(walks[1:])
def heirarchicalSoftMax(data):
    outcomes = tf.stack([tf.ones(len(data)//2), tf.zeros(len(data)//2)])
    heirarchicalSoftMax
    pass
