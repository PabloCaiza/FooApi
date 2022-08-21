import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging (1)
import pathlib
import tensorflow as tf
import cv2
import argparse

# Enable GPU dynamic memory allocation
# gpus = tf.config.experimental.list_physical_devices('GPU')
# for gpu in gpus:
#     tf.config.experimental.set_memory_growth(gpu, True)



# PROVIDE PATH TO MODEL DIRECTORY
PATH_TO_MODEL_DIR = 'my_model'

# PROVIDE PATH TO LABEL MAP
PATH_TO_LABELS = 'label_map.pbtxt'

# PROVIDE THE MINIMUM CONFIDENCE THRESHOLD
MIN_CONF_THRESH = float(0.60)

# LOAD THE MODEL


from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils

PATH_TO_SAVED_MODEL = "my_rccn_model/saved_model"

# LOAD SAVED MODEL AND BUILD DETECTION FUNCTION
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

# LOAD LABEL MAP DATA FOR PLOTTING

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,
                                                                    use_display_name=True)

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')  # Suppress Matplotlib warnings


def load_image_into_numpy_array(path):
    return np.array(Image.open(path))

def detectIngredients(image):
    image_np = load_image_into_numpy_array(image)
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]
    detections = detect_fn(input_tensor)
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
    indexItems = [index for index in range(len(detections['detection_scores'])) if
                  detections['detection_scores'][index] >= 0.6]
    categories = dict()
    for index in indexItems:
        if detections['detection_classes'][index] in categories:
            categories[detections['detection_classes'][index]] += 1
        else:
            categories[detections['detection_classes'][index]] = 1
    final_categories = dict()
    for c in categories:
        for ci in category_index:
            if c == category_index[ci]['id']:
                final_categories[category_index[ci]['name']] = categories[c]
    return final_categories



