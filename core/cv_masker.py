import tensorflow.lite as tf
import cv2
import numpy as np


class classifier():
    def __init__(self, model_path, labels_path, img_path=None):
        self.img_path = img_path
        self.model_path = model_path
        self.labels_path = labels_path

        self.results = None

        self.classified = False

    def classify(self, img_path=None):
        if img_path:
            self.img_path = img_path
        if not self.img_path:
            print('ERROR - No image selected')
            return

        # Load TFLite model and allocate tensors.
        interpreter = tf.Interpreter(self.model_path)
        interpreter.allocate_tensors()

        # get input and output tensors
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        input_shape = input_details[0]['shape']

        # Read the image and decode to a tensor
        img = cv2.imread(self.img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_rgb = cv2.resize(
            img_rgb, (input_shape[1], input_shape[2]), cv2.INTER_AREA)
        img_rgb = img_rgb.reshape(input_shape)
        input_dtype = input_details[0]['dtype']
        img_rgb = img_rgb.astype(input_dtype)

        input_tensor = np.array(img_rgb, dtype=input_dtype)
        input_index = input_details[0]["index"]

        interpreter.set_tensor(input_index, input_tensor)
        # Run the inference
        interpreter.invoke()

        boxes = interpreter.get_tensor(output_details[0]['index'])[0]
        classes = interpreter.get_tensor(output_details[1]['index'])[0]
        scores = interpreter.get_tensor(output_details[2]['index'])[0]
        num = interpreter.get_tensor(output_details[3]['index'])[0]

        self.results = [boxes, classes, scores, num]
        self.classified = True
        return self.results

    def get_labels(self):
        if not self.classified:
            print("ERROR - Not yet classified. Run classify")
            return

        file = open(self.labels_path)
        category_index = {}
        for i, val in enumerate(file):
            if i == 0:
                val = val[:-1]
                blank = val.copy()
            else:
                val = val[:-1]
                if val != blank:
                    category_index.update({(i-1): {'id': (i-1), 'name': val}})

        file.close()


cl = classifier('../models/coco/model.tflite',
                '../models/coco/labelmap.txt')
cl.classify('../pictures/pic #1.png')
