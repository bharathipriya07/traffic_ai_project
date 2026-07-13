# Traffic AI Project

A Python-based traffic violation detection system that uses computer vision and machine learning to detect vehicles, helmets, and number plates from video input.

## Features
- Detects vehicles from video footage
- Detects helmet usage for motorcycle riders
- Reads number plates using OCR
- Stores violation records in a SQLite database
- Provides a simple Flask dashboard to view violations

## Project Structure
- app.py - Flask web dashboard
- main.py - Video processing and detection pipeline
- database.py - SQLite database operations
- utils/anpr.py - Number plate recognition using EasyOCR
- templates/ - HTML templates for the dashboard
- static/violations/ - Saved violation images

  demo website -https://traffic-ai-project-2.onrender.com0

## Requirements
Install the dependencies using:

```bash
pip install -r requirements.txt
```

## Run the Project
1. Start the Flask dashboard:
   ```bash
   python app.py
   ```
2. Run the detection pipeline:
   ```bash
   python main.py
   ```

## Notes
- The project expects video input files such as video.mp4 in the project root.
- The trained model files yolov8n.pt and helmet.pt should be available in the project root.
- The application uses SQLite, so no additional database server is required.
