from core import cv_masker as msk


model_path = 'models/yolov5/model.tflite'
labels_path = 'models/yolov5/labelmap.txt'

# Internal method =============================================================


def classify(img):
    return mask.classify(img)

# =============================================================================


def mask(session):
    global mask
    mask = msk.classifier(model_path, labels_path)
    # args = ['hey', 'hoo']
    session.cap.masking(classify)


def set_paths(model, labels):
    global model_path
    global labels_path

    model_path = model
    labels_path = labels
