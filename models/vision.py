import tensorflow as tf

__all__ = ['mobilenetv3_small', 'inceptionv3', 'vgg16']


class CNN_Encoder(tf.keras.Model):
    def __init__(self, base_model, embedding_dim):
        super(CNN_Encoder, self).__init__()
        self.base_model = base_model
        self.base_model.trainable = False
        self.embedding_dim = embedding_dim
        self.fc = tf.keras.layers.Dense(self.embedding_dim)

    def call(self, x):
        x = self.base_model(x)
        x = tf.reshape(x, (tf.shape(x)[0], -1, tf.shape(x)[3]))
        x = self.fc(x)
        x = tf.nn.relu(x)
        return x

    def get_config(self):
        return {
            'base_model': self.base_model,
            'embedding_dim': self.embedding_dim
        }

    @classmethod
    def from_config(cls, config):
        return cls(**config)


"""
We will need to handle preprossing differently for each model.
https://www.tensorflow.org/api_docs/python/tf/keras/applications/MobileNetV3Small
https://www.tensorflow.org/api_docs/python/tf/keras/applications/inception_v3/InceptionV3
https://www.tensorflow.org/api_docs/python/tf/keras/applications/vgg16/VGG16

"""


def mobilenetv3_small(input_shape, embedding_dim):
    base_model = tf.keras.applications.MobileNetV3Small(
        input_shape=input_shape, include_top=False, weights='imagenet', include_preprocessing=False)
    encoder = CNN_Encoder(base_model, embedding_dim)
    return encoder


def inceptionv3(input_shape, embedding_dim):
    base_model = tf.keras.applications.inception_v3.InceptionV3(
        input_shape=input_shape, include_top=False, weights='imagenet')
    encoder = CNN_Encoder(base_model, embedding_dim)
    return encoder


def vgg16(input_shape, embedding_dim):
    base_model = tf.keras.applications.vgg16.VGG16(input_shape=input_shape,
                                                   include_top=False,
                                                   weights='imagenet')
    encoder = CNN_Encoder(base_model, embedding_dim)
    return encoder