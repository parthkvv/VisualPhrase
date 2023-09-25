import numpy as np
import tensorflow as tf


def evaluate(image, encoder, decoder, tokenizer, max_seq_length, attention_features_shape=64):
    features = encoder(tf.expand_dims(image[0], axis=0))

    attention_plot = np.zeros((max_seq_length, attention_features_shape))
    hidden = decoder.reset_state(batch_size=1)

    dec_input = tf.expand_dims([tokenizer.word_index['<start>']], 0)
    result = []

    for i in range(max_seq_length):
        predictions, hidden, attention_weights = decoder(dec_input,
                                                        features,
                                                        hidden)
        attention_plot[i] = tf.reshape(attention_weights, (-1, )).numpy()
        predicted_id = tf.random.categorical(predictions, 1)[0][0].numpy()
    
        result.append(tokenizer.index_word[predicted_id])
        
        if tokenizer.index_word[predicted_id] == '<end>':
            return result[:-1], attention_plot

        dec_input = tf.expand_dims([predicted_id], 0)

    attention_plot = attention_plot[:len(result), :]
    
    return result, attention_plot