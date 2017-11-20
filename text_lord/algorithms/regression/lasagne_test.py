import numpy as np
import theano
import theano.tensor as T

import lasagne

l_in = lasagne.layers.InputLayer(shape=(None, 1, 28, 28),
                                 input_var=None)
