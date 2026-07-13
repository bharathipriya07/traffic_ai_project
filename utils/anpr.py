import cv2
import easyocr

reader = easyocr.Reader(['en'])

def read_number_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    results = reader.readtext(gray)

    for (bbox, text, prob) in results:
        if prob > 0.5:
            return text

    return None