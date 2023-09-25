from flask import request

import model
from app import app

models = {
    "vision": {
        "EfficientNet B0": "efficientnetb0",
        "InceptionV3": "inceptionv3",
        # "ResNet50": "resnet50",
        "VGG16": "vgg16"
    },
    "language": {
        # "RNN": "rnn",
        "RNN with attention": "rnn_attention",
        # "BERT": "bert"
        "Transformer": "transformer"
    }
}


@app.route('/models', methods=['GET'])
def get_models():
    return {key: list(value.keys()) for key, value in models.items()}


@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()

    image_object = request.files['image']
    vision_model = models["vision"][data["vision"]]
    language_model = models["language"][data["language"]]

    caption, attention_array = model.predict(image_object, vision_model,
                                            language_model)
    if data["language"] == "Transformer":
        attention_array_list = [attention_array[i].tolist() for i in range(attention_array.shape[0])]
    else:  
        attention_array_list = [attention_array.tolist()]                                      

    return {
        "caption": caption,
        "attention": attention_array_list
    }
