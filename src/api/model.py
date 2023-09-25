import numpy as np
import tensorflow as tf
import pickle
from transformer import Transformer, create_masks_decoder, create_padding_mask, create_look_ahead_mask
import json
import os

model_dict = {}


def build_models(vision_model, language_model):
    if vision_model + "_" + language_model in model_dict:
        encoder, decoder, tokenizer = model_dict[vision_model + "_" + language_model]
    else:
        root = "models/" + vision_model + "_" + language_model + "/"

        encoder = tf.keras.models.load_model(root + "encoder")
        decoder = tf.keras.models.load_model(root + "decoder")
        tokenizer = load_tokenizer(root)

        model_dict[vision_model + "_" + language_model] = (encoder, decoder, tokenizer)

    return encoder, decoder, tokenizer


def build_models_transformer(vision_model, language_model):
    if vision_model + "_" + language_model in model_dict:
        transformer, tokenizer, model_config = model_dict[vision_model + "_" + language_model]
    else:
        root = "models/" + vision_model + "_" + language_model + "/"

        # get model configuration
        with open(os.path.join(root, 'model_config.json')) as json_file:
            model_config = json.load(json_file)

        # initialize transformer model
        # transformer = tf.keras.models.load_model(root + "transformer")
        transformer = Transformer(image_model=model_config["image_model"],
                                  input_shape=model_config["input_shape"],
                                  num_layers=model_config["num_layers"],
                                  embedding_dim=model_config["embedding_dim"],
                                  num_heads=model_config["num_heads"],
                                  dff=model_config["dff"],
                                  row_size=model_config["row_size"],
                                  col_size=model_config["col_size"],
                                  target_vocab_size=model_config["target_vocab_size"],
                                  max_pos_encoding=model_config["max_pos_encoding"],
                                  rate=model_config["rate"])
        # load transformer weights
        transformer.load_weights(os.path.join(root,'transformer_weights'))
        # load tokenizer                      
        tokenizer = load_tokenizer(root)

        model_dict[vision_model + "_" + language_model] = (transformer, tokenizer, model_config)

    return transformer, tokenizer, model_config


def load_tokenizer(path):
    tokenizer_path = path + "tokenizer.pickle"

    with open(tokenizer_path, "rb") as handle:
        tokenizer = pickle.load(handle)

    return tokenizer


def preprocess_image(image_object, vision_model, language_model):
    if vision_model == "efficientnetb0":
        image_width = 224
        image_height = 224
        preprocess_input = tf.keras.applications.mobilenet_v3.preprocess_input
    elif vision_model == "inceptionv3":
        image_width = 299
        image_height = 299
        preprocess_input = tf.keras.applications.inception_v3.preprocess_input
    elif vision_model == "vgg16":
        if language_model == "transformer":
            image_width = 224
            image_height = 224
        else:
            image_width = 299
            image_height = 299
        preprocess_input = tf.keras.applications.vgg16.preprocess_input
    else:
        raise Exception(f"Invalid vision model: {vision_model}")
    
    num_channels = 3

    def load_image(image_object):
        image = image_object.read()
        image = tf.io.decode_image(image, channels=num_channels, expand_animations=False)
        image = tf.image.resize(image, (image_height, image_width))
        image = preprocess_input(image)
        return image

    image = load_image(image_object)
    return image


def evaluate(image, encoder, decoder, tokenizer, *, max_seq_length=52, attention_features_shape=64):
    features = encoder(tf.expand_dims(image, axis=0))

    attention_array = np.zeros((max_seq_length, attention_features_shape))
    hidden = decoder.reset_state(batch_size=1)

    dec_input = tf.expand_dims([tokenizer.word_index['<start>']], 0)
    result = []

    for i in range(max_seq_length):
        predictions, hidden, attention_weights = decoder(dec_input, features, hidden)
        attention_array[i] = tf.reshape(attention_weights, (-1, )).numpy()
        predicted_id = tf.random.categorical(predictions, 1)[0][0].numpy()
    
        result.append(tokenizer.index_word[predicted_id])
        
        if tokenizer.index_word[predicted_id] == '<end>':
            break

        dec_input = tf.expand_dims([predicted_id], 0)

    result = result[:-1]
    num_words = len(result)
    attention_array = attention_array[:num_words]

    max = np.max(attention_array, axis=1, keepdims=True)
    min = np.min(attention_array, axis=1, keepdims=True)
    attention_array = (attention_array - min) / (max - min)
    
    length = int(np.sqrt(attention_features_shape))
    attention_array = attention_array.reshape(-1,  length, length)

    return result, attention_array


def evaluate_transformer(image, transformer, tokenizer, *, max_seq_length=52, attention_features_shape=64, attention_num_heads=4):
    temp_input = tf.expand_dims(image, axis=0)

    #attention_array = np.zeros((attention_num_heads, max_seq_length, attention_features_shape))

    start_token = tokenizer.word_index['<start>']
    end_token = tokenizer.word_index['<end>']
    decoder_input = [start_token]
    output = tf.expand_dims(decoder_input, 0)

    result = []

    for i in range(max_seq_length):
        dec_mask = create_masks_decoder(output)
        predictions, attention_weights = transformer(temp_input, output, False, dec_mask)
        #attention_array[i] = tf.reshape(attention_weights, (-1, )).numpy()

        predictions = predictions[: ,-1:, :]  # (batch_size, 1, vocab_size)
        predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)
        result.append(tokenizer.index_word[int(predicted_id)])
        if predicted_id == end_token:
            #return result,tf.squeeze(output, axis=0), attention_weights
            break
        
        output = tf.concat([output, predicted_id], axis=-1)

    #return result,tf.squeeze(output, axis=0), attention_weights

    result = result[:-1]
    num_words = len(result)
    #attention_array = attention_array[:num_words]
    #attention_array = tf.reshape(attention_weights, (-1, )).numpy()

    # Brendan: this needs to be changed!!!!!!! I only include first attention head to fit with react code
    if False:
        attention_array = attention_weights[0,:,:num_words,:].numpy()
        max = np.max(attention_array, axis=2, keepdims=True)
        min = np.min(attention_array, axis=2, keepdims=True)
    attention_array = attention_weights['decoder_layer2_block2']
    attention_array = attention_array[0,:,:num_words,:].numpy()
    max = np.max(attention_array, axis=2, keepdims=True)
    min = np.min(attention_array, axis=2, keepdims=True)
    attention_array = (attention_array - min) / (max - min)
    
    length = int(np.sqrt(attention_features_shape))
    # Brendan: this also needs to be changed
    if False:
        attention_array = attention_array.reshape(-1, attention_num_heads,length, length)
    #attention_array = attention_array.reshape(-1,length, length)
    attention_array = attention_array.reshape(attention_num_heads, num_words, length, length)

    return result, attention_array


def predict(image_object, vision_model, language_model):
    image = preprocess_image(image_object, vision_model, language_model)
    
    if language_model == "transformer":
        transformer, tokenizer, model_config = build_models_transformer(vision_model, language_model)
        attention_features_shape = model_config["row_size"]*model_config["col_size"]
        attention_num_heads = model_config["num_heads"]
    else:
        encoder, decoder, tokenizer = build_models(vision_model, language_model)
    
        if vision_model == "efficientnetb0":
            attention_features_shape = 7 * 7
        elif vision_model == "vgg16":
            attention_features_shape = 9 * 9
        else:
            attention_features_shape = 8 * 8

    if language_model == "transformer":
        caption, attention_array = evaluate_transformer(
        image,
        transformer,
        tokenizer,
        attention_features_shape=attention_features_shape,
        attention_num_heads=attention_num_heads
    )
    else:
        caption, attention_array = evaluate(
            image,
            encoder,
            decoder,
            tokenizer,
            attention_features_shape=attention_features_shape
        )

    caption = " ".join(caption)

    return caption, attention_array