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
    return model
