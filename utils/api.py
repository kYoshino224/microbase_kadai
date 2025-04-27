import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import pandas as pd

def get_word_list(input_image_path):
    try:
        endpoint = os.environ["VISION_ENDPOINT"]
        key = os.environ["VISION_KEY"]
    except KeyError:
        print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
        print("Set them before running this sample.")
        exit()

    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    result = client.analyze(
        image_data=open(input_image_path, "rb"),
        visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ],
        gender_neutral_caption=True,
    )
    word_list_df = pd.DataFrame(columns=["word", "x", "y", "gradient", "region"])
    if result.read is not None:
        for line in result.read.blocks[0].lines:
            for word in line.words:
                x_center_left = (word.bounding_polygon[0]["x"] + word.bounding_polygon[3]["x"]) / 2
                x_center_right = (word.bounding_polygon[1]["x"] + word.bounding_polygon[2]["x"]) / 2
                y_center_left = (word.bounding_polygon[0]["y"] + word.bounding_polygon[3]["y"]) / 2
                y_center_right = (word.bounding_polygon[1]["y"] + word.bounding_polygon[2]["y"]) / 2
                x_center = int((x_center_left + x_center_right) / 2)
                y_center = int((y_center_left + y_center_right) / 2)
                gradient = (y_center_right - y_center_left) / (x_center_right - x_center_left) 
                new_word = pd.Series({
                    "word": word.text,
                    "x": x_center,
                    "y": y_center,
                    "gradient": gradient,
                    "region": 0
                })
                word_list_df = pd.concat([word_list_df, new_word.to_frame().T], ignore_index=True)
    return word_list_df