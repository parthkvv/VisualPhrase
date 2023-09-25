from models.vision import inceptionv3
import tensorflow as tf

__all__ = ["rnn", "rnn_attention"]


# class RNN(tf.keras.Model):
#     def __init__(self, embedding_dim, units, vocab_size):
#         super(RNN, self).__init__()
#         self.units = units
#         self.embedding_dim = embedding_dim
#         self.vocab_size = vocab_size
#         self.embedding = tf.keras.layers.Embedding(self.vocab_size,
#                                                    self.embedding_dim)
#         self.gru = tf.keras.layers.GRU(self.units,
#                                        return_sequences=True,
#                                        return_state=True,
#                                        recurrent_initializer='glorot_uniform')
#         self.fc1 = tf.keras.layers.Dense(self.units)
#         self.fc2 = tf.keras.layers.Dense(self.vocab_size)
#         self.W1 = tf.keras.layers.Dense(self.units)

#     def call(self, x, features, hidden):
#         x = self.embedding(x)
#         x = tf.nn.tanh(x + tf.expand_dims(features, 1))
#         output, state = self.gru(x, hidden)
#         x = self.fc1(output)
#         x = tf.reshape(x, (-1, x.shape[2]))
#         x = self.fc2(x)
#         return x, state

#     @tf.function
#     def reset_state(self, batch_size):
#         return tf.zeros((batch_size, self.units))

#     def get_config(self):
#         return {
#             'units': self.units,
#             'embedding_dim': self.embedding_dim,
#             'vocab_size': self.vocab_size
#         }

#     @classmethod
#     def from_config(cls, config):
#         return cls(**config)


class Bahdanau_Attention(tf.keras.Model):
    def __init__(self, units):
        super(Bahdanau_Attention, self).__init__()
        self.W1 = tf.keras.layers.Dense(units)
        self.W2 = tf.keras.layers.Dense(units)
        self.V = tf.keras.layers.Dense(1)

    def call(self, features, hidden):
        hidden_with_time_axis = tf.expand_dims(hidden, 1)
        attention_hidden_layer = (
            tf.nn.tanh(self.W1(features) + self.W2(hidden_with_time_axis)))
        score = self.V(attention_hidden_layer)
        attention_weights = tf.nn.softmax(score, axis=1)
        context_vector = attention_weights * features
        context_vector = tf.reduce_sum(context_vector, axis=1)
        return context_vector, attention_weights


class RNN_Attention(tf.keras.Model):
    def __init__(self, embedding_dim, units, vocab_size):
        super(RNN_Attention, self).__init__()
        self.units = units
        self.embedding_dim = embedding_dim
        self.vocab_size = vocab_size
        self.embedding = tf.keras.layers.Embedding(self.vocab_size,
                                                   self.embedding_dim)
        self.gru = tf.keras.layers.GRU(self.units,
                                       return_sequences=True,
                                       return_state=True,
                                       recurrent_initializer='glorot_uniform')
        self.fc1 = tf.keras.layers.Dense(self.units)
        self.fc2 = tf.keras.layers.Dense(self.vocab_size)
        self.attention = Bahdanau_Attention(self.units)

    def call(self, x, features, hidden):
        context_vector, attention_weights = self.attention(features, hidden)
        x = self.embedding(x)
        x = tf.concat([tf.expand_dims(context_vector, 1), x], axis=-1)
        output, state = self.gru(x)
        x = self.fc1(output)
        x = tf.reshape(x, (-1, tf.shape(x)[2]))
        x = self.fc2(x)
        return x, state, attention_weights

    @tf.function(
        input_signature=[tf.TensorSpec(shape=None, dtype=tf.float32)]
    )
    def reset_state(self, batch_size):
        return tf.zeros((batch_size, self.units))

    def get_config(self):
        return {
            'units': self.units,
            'embedding_dim': self.embedding_dim,
            'vocab_size': self.vocab_size
        }

    @classmethod
    def from_config(cls, config):
        return cls(**config)

def rnn_attention(embedding_dim, units, vocab_size):
    return RNN_Attention(embedding_dim, units, vocab_size)


# def rnn(units, embedding_dim, vocab_size):
#     return RNN(embedding_dim, units, vocab_size)


def rnn_attention(embedding_dim, units, vocab_size):
    return RNN_Attention(embedding_dim, units, vocab_size)