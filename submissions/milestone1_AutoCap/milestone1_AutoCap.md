# Milestone 1
Group: AutoCap

Project: Caption this image

## Team members
- Brendan O'Leary
- Luke Sagers
- Kamran Ahmed

## Problem definition
The advancements in computer vision, natural language processing, and computing have led to complicated and sophistocated models. These models are large and require a lot of data and training. However, once trained, these models can be leveraged for other tasks, a concept known as transfer learning. Image captioning is a task that can use both pre-trained image and NLP models. One use case for image captioning is for automatic alternate text generation for people with visual impairments that heavily rely on screen readers to access the interent through audio (Yesilada et al 2004). Accessibilty, photo album indexing, and automatic social media captioning and filtering are just some of the many applications that make accurate automatic image captioning an important priority. 

Ultimately, obtaining accurate image captions from a model will benefit both specialized and generalized fields. In a specialized field, like healthcare, image captioning could bring down the high cost of data annotation (Willemink et al 2020) and aid in improving the interpretation of medical images (while potentially giving more interpretability than a simple classification model). On the general side, automatic captioning can be used to create large labeled datasets from any image source and can also lead to improvements for models such as semi-supervised learning models. 

## Proposed solution
The objective of this model is to take an image as an input and produce a sequence of text that serves as the caption of the image. We can achieve this with a deep learning, encoder-decoder model, where the image is encoded into features that are then decoded into a sequence of text. The encoder is a CNN feature extractor model and the decoder is a sequential language model with attention. There are several possible models to use as the image feature extractor and language model. We plan to consider all of these models and propose a final model that performs best at image captioning. 

## Project scope
- The deliverable is an AI app that produces captions for an input image. 
- This app has an underlying image + NLP model that has been trained using one or several of the datasets listed below. We will also produce statistics on the model training, such as model error and generalization gap between train and test data.
- The app will include a simple user interface that will allow a user to easily input images, return the caption, and optionally try again for a new caption. 

## Timeline and components
1. Collect and download image and caption data. Explore range of captions. Determine what pre-processing steps are necessary for both the images and the captions.
2. Create container and infrastructure for development.
2. Use potential models listed below as starting points for model exploration and selection. Compress model before deployment. Create a mock-up of app design.
3. Use mock-up to build AI web app. Possible advanced app features if time permits:
    - Create visualization interface to highlight the image features that are driving the caption prediction.
    - Build a functionality where user can edit the caption which could be used to update our model.
    - Allow for captions to be produced using different models in parallel.
4. Create infrastructure for deployment. Provisioning, deploying, and monitoring model and data.

## Datasets
- MS-COCO (Common objects in context): 330k images with at least 5 captions per image
- Flickr8k: 8k images each with five different image captions

## Potential models
### Computer Vision
- Pretrained image model to use as feature extractors. Possible models are VGG16 and VGG19, InceptionV3, and ResNet, which have been trained to classify image objects.
### Language
 - Pretrained word embeddings (GloVe, word2vec)
 - Caption text created by a sequential decoder model, such as an RNN/LSTM. Possible to also use BERT or other pre-trained transformer models.

## References
Willemink, M. J., Koszek, W. A., Hardell, C., Wu, J., Fleischmann, D., Harvey, H., Folio, L. R., Summers, R. M., Rubin, D. L., & Lungren, M. P. (2020). Preparing Medical Imaging Data for Machine Learning. Radiology, 295(1), 4–15. https://doi.org/10.1148/radiol.2020192224

Yesilada Y., Harper S., Goble C., Stevens R. (2004) Screen Readers Cannot See. In: Koch N., Fraternali P., Wirsing M. (eds) Web Engineering. ICWE 2004. Lecture Notes in Computer Science, vol 3140. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-540-27834-4_55
