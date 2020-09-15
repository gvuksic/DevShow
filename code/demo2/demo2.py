import cv2
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

credentials = ApiKeyCredentials(in_headers={"Prediction-key": "<PREDICTION_KEY>"})
predictor = CustomVisionPredictionClient("<ENDPOINT_URL>", credentials)

ret, image = camera.read()
cv2.imwrite('capture.png', image)

with open("capture.png", mode="rb") as captured_image:
    results = predictor.detect_image("<PROJECT_ID>", "<ITERATION_NAME>", captured_image)

for prediction in results.predictions:
    if prediction.probability > 0.9:
        bbox = prediction.bounding_box
        result_image = cv2.rectangle(image, (int(bbox.left * 640), int(bbox.top * 480)), (int((bbox.left + bbox.width) * 640), int((bbox.top + bbox.height) * 480)), (0, 255, 0), 3)
        cv2.imwrite('result.png', result_image)

camera.release()