#module contains all of GAN models as well as generators and discriminators
import GraphableGANs as gg
import tensorflow as tf
from tensorflow.keras import Model

#general models for graphs
#call takes in tuple, first element is tensor of adjacencies, second is tensor of features
class GraphSequential(Model):

    def __init__(self, lays = None):
        super(GraphSequential, self).__init__()
        if lays != None:
            self.lays = lays
        else:
            self.lays = []
        self.l = 0
    def add(self,layer):
        self.l += 1
        self.lays.append(layer)
    def call(self, inputs, trackTime = False):
        curr = inputs

        # print(curr)#
        for lay in self.lays:
            # if trackTime:
                # start = time()
            # print(curr[0].shape)
            if (isinstance(lay, gg.layers.GraphLayer)
                or not isinstance(curr, tuple)):
                # print("HERE!")
                curr = lay(curr)
            else:
                #by default all non-graph layers are only applied to the feature vector
                # print("THERE!", isinstance(lay, layers.GraphLayer))
                curr = (curr[0], lay(curr[1]))
            # if trackTime:
                # print(time()-start, lay)

        return curr


#GAN frameworks
#in this package, GANs contain an (or more) acociated generator model
#discriminator model and loss function
#generators/discriminators/etc are initialized outide these frameworks

#one-way GAN framework, analogous to origional GAN implementation
class BasicGan(Model):
    def __init__(self, generator, discriminator, genLoss, discLoss,
            genOptimizer = None, discOptimizer = None, **kwargs):
        super(BasicGan, self).__init__(kwargs)
        self.generator = generator
        self.discriminator = discriminator
        self.genLoss = genLoss
        self.discLoss = discLoss
        if genOptimizer == None:
            self.genOptimizer = tf.keras.optimizers.Adam(0.01)
        if discOptimizer == None:
            self.discOptimizer = tf.keras.optimizers.Adam(0.01)
    @tf.function
    def trainStep(self, noiseGraphs, exampleGraphs, trackTime = False):
        if trackTime:
            tstart = time()

        with tf.GradientTape() as genTape, tf.GradientTape() as discTape:
            if trackTime:
                start = time()
            falseGraphs = self.generator(noiseGraphs, training = True)
            if trackTime:
                print("generation time:", time()-start)
                start = time()
            realOutput = self.discriminator(exampleGraphs, training = True)
            fakeOutput = self.discriminator(falseGraphs, training = True)
            if trackTime:
                print("discrimination time:", time() - start)
                start = time()
            gLoss = self.genLoss(fakeOutput)
            dLoss = self.discLoss(fakeOutput, realOutput)
            print(dLoss)
        genGrad = genTape.gradient(gLoss,
                                        self.generator.trainable_variables)
        discGrad = discTape.gradient(dLoss,
                                        self.discriminator.trainable_variables)
        self.genOptimizer.apply_gradients(zip(genGrad,
                                            self.generator.trainable_variables))
        self.discOptimizer.apply_gradients(zip(discGrad,
                                            self.discriminator.trainable_variables))
        if trackTime:
            print("Gradient decent time:", time() - start)
    def call(self, input):
        return self.generator(input)
#two way GAN that learns genration from target domain to source domian
class BiGAN(Model):
    pass

#same as biGAN but also check for cyclic consistancy
class CycleGan(Model):
    pass

#generators


#The generator framework used in the miscGan paper

class miscGanGenerator(GraphSequential):
    """
    Breaks graph into layers using coarser matricies, constructs new graphs
    by multiplying them by learnable reconstruction matricies.
    Output is list of reconstructed graphs

    "Generated graph" is supposed to be linear combination of reconstructed gs
    """
    def __init__(self, coarsers):
        pass
