
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
#The MiscGan framework as described in the origional paper: https://www.frontiersin.org/articles/10.3389/fdata.2019.00003/full
def miscGan():
    return 0
