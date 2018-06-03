import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import time
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from io import BytesIO
from PIL import Image
from object_detection.utils import ops as utils_ops

if tf.__version__ < '1.4.0':
  raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')

from object_detection.utils import label_map_util

from object_detection.utils import visualization_utils as vis_util


import requests
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import parser_classes
try:
    from django.utils import simplejson as json
except ImportError:
    import json

# What model to download.
MODEL_NAME = 'backend/apps/object_detection_api/model-nets/ssd_mobilenet_v1_coco_2017_11_17'
MODEL_FILE = MODEL_NAME + '.tar.gz'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = 'backend/apps/object_detection_api/model-nets/mscoco_label_map.pbtxt'

NUM_CLASSES = 90


tar_file = tarfile.open(MODEL_FILE)
for file in tar_file.getmembers():
  file_name = os.path.basename(file.name)
  if 'frozen_inference_graph.pb' in file_name:
    tar_file.extract(file, os.getcwd())

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


def run_inference_for_single_image(image, graph):
    start_time = time.time()
    with graph.as_default():
        with tf.Session() as sess:
            # Get handles to input and output tensors
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in [
                'num_detections', 'detection_boxes', 'detection_scores',
                'detection_classes', 'detection_masks'
            ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                        tensor_name)
            if 'detection_masks' in tensor_dict:
                # The following processing is only for single image
                detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                    detection_masks, detection_boxes, image.shape[0], image.shape[1])
                detection_masks_reframed = tf.cast(
                    tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                # Follow the convention by adding back the batch dimension
                tensor_dict['detection_masks'] = tf.expand_dims(
                    detection_masks_reframed, 0)
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
            # Run inference
            output_dict = sess.run(tensor_dict,
                                   feed_dict={image_tensor: np.expand_dims(image, 0)})
            # all outputs are float32 numpy arrays, so convert types as appropriate
            output_dict['num_detections'] = int(output_dict['num_detections'][0])

            output_dict['detection_classes'] = output_dict[
                'detection_classes'][0].astype(np.uint8)
            output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
            output_dict['detection_scores'] = output_dict['detection_scores'][0]
            if 'detection_masks' in output_dict:
                output_dict['detection_masks'] = output_dict['detection_masks'][0]
        print(time.time() - start_time)
    return output_dict


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
@parser_classes((JSONParser,))
def object_detection_api(request):
    print("Request for detection, let's detect!")
    data = {"success": False}

    if request.method == "GET": 
        url = request.GET.get('image')
        print(url)
        response =  requests.get("http://" + url)
        image = Image.open(BytesIO(response.content))
        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        image_np = load_image_into_numpy_array(image)
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        # Actual detection.
        output_dict = run_inference_for_single_image(image_np, detection_graph)

        data["success"] = True
        data["result"] = []
        data["classes"] = []
        for index in range(len(output_dict['detection_scores'])-1):
             if output_dict['detection_scores'][index] > 0.15:
                 if (output_dict['detection_classes'][index] != 1) or (output_dict['detection_classes'][index] == 1 and output_dict['detection_scores'][index] > 0.55):
                     data["classes"].append(category_index[output_dict['detection_classes'][index]]['name'])
                     data["result"].append({"class": category_index[output_dict['detection_classes'][index]]['name'], "score": output_dict['detection_scores'][index]})
        print("Image scanned, object recognition done")
        print(data)
    return Response(data)

""" 
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
@parser_classes((JSONParser,))
def object_detection_api(request):
    print("usa san u post")
    data = {"success": False}
    print(request.query_params['image'])
    url = request.query_params['image']
    print(url)

    response = requests.get("http://" + url)
    image = Image.open(BytesIO(response.content))
    # the array based representation of the image will be used later in order to prepare the
    # result image with boxes and labels on it.
    image_np = load_image_into_numpy_array(image)
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    # Actual detection.
    output_dict = run_inference_for_single_image(image_np, detection_graph)

    data["success"] = True
    data["result"] = []
    data["classes"] = []
    for index in range(len(output_dict['detection_scores'])-1):
        if output_dict['detection_scores'][index] > 0.15:
            if (output_dict['detection_classes'][index] != 1) or (output_dict['detection_classes'][index] == 1 and output_dict['detection_scores'][index] > 0.55):
                data["classes"].append(category_index[output_dict['detection_classes'][index]]['name'])
                data["result"].append({"class": category_index[output_dict['detection_classes'][index]]['name'], "score": output_dict['detection_scores'][index]})
    print("Image scanned, object recognition done")
    print(data)
    return Response(data)
 """