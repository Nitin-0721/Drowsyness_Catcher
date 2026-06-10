# 🚗 DrowsyGuard — Real-Time Driver Drowsiness Detection

A real-time drowsiness detection system that monitors driver alertness 
using facial landmarks, eye aspect ratio, and yawn detection.

## 🎯 Features
- Real-time eye closure detection using EAR formula
- Yawn detection using MAR formula
- Multi-level alert system (Awake → Warning → Danger → Critical)
- Sound alarm on drowsiness detection
- Live web dashboard built with Flask

## 🧠 How It Works
1. MediaPipe detects 468 facial landmarks in real time
2. EAR (Eye Aspect Ratio) measures eye openness
3. MAR (Mouth Aspect Ratio) detects yawning
4. Multi-level alert fires based on consecutive drowsy frames
5. Flask dashboard streams live video + stats

## 🛠 Tech Stack
- Python
- MediaPipe (facial landmark detection)
- OpenCV (real-time video processing)
- Flask (web dashboard)
- PyGame (alarm sound)
- NumPy (EAR/MAR calculations)

## 📁 Project Structure
```
DrowsyGuard/
├── utils/
│   ├── ear_calculator.py  # Eye Aspect Ratio
│   ├── mar_calculator.py  # Mouth Aspect Ratio
│   ├── detector.py        # Core detection logic
│   └── alarm.py           # Alert system
├── templates/
│   └── index.html         # Flask dashboard
├── alerts/                # Alarm sound
├── app.py                 # Flask entry point
└── realtime_test.py       # Test without Flask
```
## ⚙️ Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open in browser
http://localhost:5000
```

## 📊 Alert Levels
| Level | Status | Condition |
|-------|--------|-----------|
| 0 | ✅ AWAKE | EAR normal |
| 1 | ⚠️ WARNING | Eyes closing or 3+ yawns |
| 2 | 🔴 DANGER | Eyes closed 20+ frames |
| 3 | 🚨 CRITICAL | Eyes closed + yawning |