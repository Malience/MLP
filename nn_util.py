import tensorflow as tf
import numpy as np

#resets tensor flow
def ResetTensorflow(seed):
    tf.reset_default_graph()
    tf.set_random_seed(seed)
    np.random.seed(seed)
    
#selu method    
def Selu(z, scale=1.0507009873554804934193349852946, alpha=1.6732632423543772848170429916717):
    return scale * tf.where(z >= 0.0, z, alpha * tf.nn.elu(z))