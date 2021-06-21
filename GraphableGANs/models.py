<<<<<<< HEAD
#module contains all of GAN models as well as generators and discriminators
import GraphableGANs as gg
import tensorflow as tf
from tensorflow.keras import Model

#general models for graphs
#call takes in tuple, first element is tensor of adjacencies, second is tensor of features
class GraphSequential(tf.keras.Model):

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
            if isinstance(lay, layers.GraphLayer) or not isinstance(curr, tuple):
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
    def __init__(self, generator, discriminator, gloss, dloss, **kwargs):
        super(BasicGan, self).__init__(kwargs)
        self.generator = generator
        self.discriminator = discriminator
        self.genLoss = gLoss
        self.discLoss = dLoss
    def train(self):
        pass
#two way GAN that learns genration from target domain to source domian
class BiGAN(Model):
    pass

#same as biGAN but also check for cyclic consistancy
class CycleGan(Model):
    pass
=======
#module contains all of GAN models as well as generators and discriminators
import GraphableGANs as gg
import tensorflow as tf
from tensorflow.keras import Model

#general models for graphs
#call takes in tuple, first element is tensor of adjacencies, second is tensor of features
class GraphSequential(tf.keras.Model):

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
            if isinstance(lay, layers.GraphLayer) or not isinstance(curr, tuple):
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
    def __init__(self, generator, discriminator, gloss, dloss, **kwargs):
        super(BasicGan, self).__init__(kwargs)
        self.generator = generator
        self.discriminator = discriminator
        self.genLoss = gLoss
        self.discLoss = dLoss
    def train(self):
        pass
#two way GAN that learns genration from target domain to source domian
class BiGAN(Model):
    pass

#same as biGAN but also check for cyclic consistancy
class CycleGan(Model):
    pass
>>>>>>> 523aa83195ddb6e076d66f660f7be7dc55a96411
