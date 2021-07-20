
#contains prebuild models for specific applications
import GraphableGANs as gg
import tensorflow as tf


def shapeGenerator(dimensions = 2):
    model = gg.GraphSequential()
    pooler = gg.layers.PoolFeatures(gg.minMaxAngle, gg.minMaxDist)
    convoluter = gg.layers.VertConvolution(depth = 1)
    dense = tf.keras.layers.Dense(dimensions)
    for _ in range(3):
        model.add(pooler)
        model.add(convoluter)
        model.add(dense)
    model.add(tf.keras.layers.tanh())
    return model
#gets more features, but otherwise a more straitforward model
def shapeDiscriminator():
    model = gg.GraphSequential()
    model.add(gg.layers.PoolFeatures(gg.minMaxAngle))
    model.add(gg.layers.DropAdj())
    model.add(tf.keras.layers.Dense(12, activation = "relu"))
    model.add(tf.keras.layers.Dense(1, activation = "sigmoid"))
    return model

#guases the probablity that an edge exist between 2 nodes based on features
def simpleEdgePredict():
    generator = gg.GraphSequential([
        gg.layers.BiDenseAdjacency(activation = "sigmoid"),
    ])
    discriminator = gg.GraphSequential([
        gg.layers.BiDenseAdjacency(activation = "sigmoid", invertProb = True),
        gg.layers.DropFeat()
    ])
    crossEntropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)

    def discLoss(fake, real):
        fake = tf.reshape(fake , (-1, 1))
        real = tf.reshape(real, (-1, 1))
        realLoss = crossEntropy(tf.ones_like(real), real)
        fakeLoss = crossEntropy(tf.zeros_like(fake), fake)
        #subtract to trick the optimiser into maximizing the losses
        return realLoss+fakeLoss
    def genLoss(fake):
        fake = tf.reshape(fake , (-1, 1) )
        return crossEntropy(tf.ones_like(fake), fake)
    model = gg.BasicGan(generator, discriminator, genLoss, discLoss)
    return model
    #
    # def __init__(self):
    #     super(SimpleEdgePredict, self).__init__()
#The MiscGan framework as described in the origional paper: https://www.frontiersin.org/articles/10.3389/fdata.2019.00003/full
def miscGan():
    return 0
