import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from flask import current_app


def load_model():
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor


def get_image_features(model, processor, image_path=None, image=None):

    image = Image.open(image_path) if image_path else image
    inputs = processor(images=image, return_tensors="pt", padding=True)
    image_features = model.get_image_features(**inputs)
    return image_features


def get_text_features(model, processor, text):
    inputs = processor(text=text, return_tensors="pt", padding=True)
    text_features = model.get_text_features(**inputs)
    return text_features


def find_best_match(uploaded_image, gear_array, model=None, processor=None):
    if None in [model, processor]:
        model, processor = load_model()
    image_features = get_image_features(model, processor, image=uploaded_image)

    best_match = None
    highest_similarity = -1

    for item in gear_array:
        item_description = f"{item.name} {
            item.type} {item.description}"

        current_app.logger.info(item_description)
        text_features = get_text_features(model, processor, item_description)
        similarity = torch.nn.functional.cosine_similarity(
            image_features, text_features).item()

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = item

    return best_match, highest_similarity
