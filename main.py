import os
import cv2
from ultralytics import YOLO
from utils.anpr import read_number_plate
from database import create_table, insert_challan

# 🔥 Load models
vehicle_model = YOLO("yolov8n.pt")
helmet_model = YOLO("helmet.pt")

cap = cv2.VideoCapture("video.mp4")

create_table()

# 🔥 Create folder for saving images
os.makedirs("static/violations", exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = vehicle_model(frame)
    vehicle_count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # 🚗 VEHICLE DETECTION
            if cls in [2, 3, 5, 7]:
                vehicle_count += 1
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

                vehicle_crop = frame[y1:y2, x1:x2]
                plate_text = read_number_plate(vehicle_crop)

                if plate_text:
                    cv2.putText(frame, plate_text, (x1, y1-40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

            # 🚶 PERSON
            if cls == 0:
                cv2.putText(frame, "Person", (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

            # 🏍️ MOTORCYCLE
            if cls == 3:
                cv2.putText(frame, "Bike", (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

                bike_crop = frame[y1:y2, x1:x2]

                # 🔥 Helmet detection
                helmet_results = helmet_model(bike_crop)
                helmet_detected = False

                for hr in helmet_results:
                    for hbox in hr.boxes:
                        hcls = int(hbox.cls[0])
                        if hcls == 0:
                            helmet_detected = True

                plate_text = read_number_plate(bike_crop)

                if helmet_detected:
                    cv2.putText(frame, "Helmet ✅", (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                else:
                    cv2.putText(frame, "No Helmet ❌", (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

                    vehicle_no = plate_text if plate_text else "Unknown"

                    # 🔥 Save violation image
                    image_path = f"static/violations/{vehicle_no}_{x1}.jpg"
                    cv2.imwrite(image_path, frame)

                    # 🔥 Store in DB (with image path)
                    insert_challan(vehicle_no, "No Helmet", 500, image_path)

                    print("🚨 Violation Saved with Image")
                    print("Vehicle:", vehicle_no)
                    print("------------------")

    # 🚦 Traffic Density
    if vehicle_count < 10:
        density = "LOW"
    elif vehicle_count < 30:
        density = "MEDIUM"
    else:
        density = "HIGH"

    cv2.putText(frame, f"Vehicles: {vehicle_count}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    cv2.putText(frame, f"Traffic: {density}", (20,80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("Traffic AI System", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()