# Smart Home — AI-Powered Face Recognition Access Control System

> **A full-stack smart home system with CNN-based face recognition for automated door access, sensor-driven security, and homeowner-controlled face database management**

---

## 📋 Project Overview

This is a **large-scale team project** building a complete smart home system that integrates **AI-powered face recognition**, **embedded microcontroller control**, **PCB hardware design**, and a **desktop GUI** into a unified home automation platform.

The system's core feature is a **CNN-based face recognition access control system** that:
- Detects faces at the door using a camera
- Identifies known residents using a **ResNet-based face encoding model**
- Automatically unlocks the door (via servo motor) for recognized people
- Alerts the homeowner for unknown visitors via a GUI dashboard
- Allows the homeowner to **add new faces** to the authorized database in real-time

---

## 🎯 My Role: Face Recognition System

I was responsible for designing and implementing the **entire face recognition pipeline** — from face detection and encoding to identity matching and database management.

### Face Recognition Pipeline

```
┌──────────────┐
│   Camera      │
│  (Webcam at   │
│   door)       │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  CNN Face Detector   │
│  (MMOD — dlib)       │
│  mmod_human_face_    │
│  detector.dat        │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  68-Point Facial     │
│  Landmark Predictor  │
│  (shape_predictor_   │
│  68_face_landmarks)  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Face Encoding       │
│  (ResNet — dlib)     │
│  128-dim face vector │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Compare against     │
│  known face database │
│  (Euclidean dist.)   │
└──────┬───────────────┘
       │
       ├── Known face → Unlock door (Arduino → Servo)
       │
       └── Unknown face → Alert homeowner (GUI)
                            → Option: Add to database
```

### Technical Details

| Component | Implementation |
|-----------|----------------|
| **Face Detection** | CNN-based MMOD (Max-Margin Object Detection) from dlib — more robust than HOG under varying angles and lighting |
| **Facial Landmarks** | 68-point landmark predictor for face alignment and normalization |
| **Face Encoding** | ResNet-based model (`dlib_face_recognition_resnet_model_v1`) producing **128-dimensional face embeddings** |
| **Identity Matching** | Euclidean distance between face encodings — threshold-tuned for security vs. convenience |
| **Database** | File-based storage of known face encodings with associated names |
| **Preprocessing** | Image normalization, contrast enhancement for robustness under varying lighting conditions |
| **Communication** | Python ↔ Arduino via serial (UART) — sends unlock/lock commands based on recognition result |

### Key Design Decisions

- **CNN (MMOD) over HOG detector:** The CNN-based detector is significantly more accurate at detecting faces at angles and under poor lighting — critical for a door-mounted camera where visitors may approach from different directions.
- **128-dim ResNet embeddings:** Each face is encoded as a 128-dimensional vector. Two encodings with Euclidean distance below the threshold are considered the same person. This approach is **invariant to lighting, expression, and minor pose changes**.
- **Real-time database updates:** The homeowner can add new authorized faces through the GUI — the system captures multiple face encodings of the new person for improved recognition accuracy.

### Files I Developed

| File | Purpose |
|------|---------|
| `initialize.py` | System initialization — loads models, sets up camera, loads face database |
| `gui.py` / `gui1.py` | Desktop GUI for homeowner control — view camera feed, manage face database, receive alerts |
| `dataset/` | Face image database — organized by person name for training/registration |
| Face model files | `dlib_face_recognition_resnet_model_v1.dat`, `mmod_human_face_detector.dat`, `shape_predictor_68_face_landmarks.dat` |

---

## 🏠 Full System Architecture (Team Project)

### Hardware Layer

| Component | Description |
|-----------|-------------|
| **Microcontroller** | Arduino-based — controls all physical actuators and reads sensor data |
| **Servo Motor** | Door lock mechanism — actuated when face is recognized |
| **PIR Sensor** | Motion detection for security monitoring |
| **Camera** | Webcam mounted at door for face capture |
| **PCB Design** | Custom PCB designed in **Altium Designer** — integrates microcontroller, motor driver, and sensor interfaces |
| **Motor Driver** | Custom motor integrated library for servo and DC motor control |

### Software Layer

| Component | Description |
|-----------|-------------|
| **Face Recognition (Python)** | CNN detection + ResNet encoding + identity matching |
| **Arduino Firmware (C++)** | Receives serial commands from Python, controls servo/sensors |
| **GUI (Python/Tkinter)** | Homeowner dashboard — camera feed, face database management, alerts |
| **Serial Communication** | Python-Arduino bridge for command/response protocol |

### Simulation

- **Proteus** circuit simulation for validating the hardware design before PCB fabrication

---

## 🗂 Repository Structure

```
smart_home/
├── Final_arduino2/                          # Final Arduino firmware
│   └── Final_arduino.ino                    # Microcontroller code (serial command handler)
├── dataset/                                 # Face recognition database (images by person)
├── motor_integrated_library/                # Motor driver library for Arduino
├── smart home sch/                          # Altium schematic files
├── __pycache__/                             # Python cache
│
├── gui.py / gui1.py                         # Homeowner GUI (camera feed + face management)
├── initialize.py                            # System initialization (model loading, setup)
├── arduinotest.py                           # Arduino serial communication testing
├── Final_arduino.ino                        # Arduino firmware (earlier version)
├── cody_sep6a.ino                           # Arduino code (development iteration)
│
├── dlib_face_recognition_resnet_model_v1.dat  # ResNet face encoding model
├── mmod_human_face_detector.dat               # CNN face detector model
├── shape_predictor_68_face_landmarks.dat      # 68-point landmark model
│
├── Final Proteus File.pdsprj                # Proteus simulation file
├── smart home sch.PrjPcb                    # Altium PCB project
├── Altium.zip / Altium Last.zip             # PCB design archives
├── servo.LibPkg                             # Servo library for Altium
└── PIR Sensor Library for Proteus.rar       # PIR sensor simulation library
```

---

## 🛠 Technologies &amp; Libraries

| Layer | Tools |
|-------|-------|
| **Face Recognition** | dlib (CNN detector, ResNet encoder, 68-landmark predictor), OpenCV |
| **GUI** | Python, Tkinter/PyQt |
| **Microcontroller** | Arduino (C++), Serial (UART) communication |
| **Hardware Design** | Altium Designer (schematic + PCB layout) |
| **Simulation** | Proteus |
| **Motor Control** | Servo motors, custom motor driver library |
| **Sensors** | PIR motion sensor, webcam camera |

---

## 🚀 Usage

### Prerequisites

```bash
pip install dlib opencv-python numpy
```

### Run the System

```bash
# 1. Initialize the system (loads models, starts camera)
python initialize.py

# 2. Launch the GUI
python gui.py

# 3. Upload Arduino firmware
# Open Final_arduino2/Final_arduino.ino in Arduino IDE and upload
```

### System Operation

1. **Camera activates** and continuously monitors for faces
2. **Face detected** → CNN extracts 128-dim encoding
3. **Encoding compared** against database of known faces
4. **Match found** → Arduino receives "unlock" command → servo opens door
5. **No match** → GUI alerts homeowner → option to register new face

---

## 🔗 Related Projects

| Repository | Description |
|------------|-------------|
| [hand_landmarkers_detection](https://github.com/heba266/hand_landmarkers_detection) | MediaPipe hand gesture control for robotic arm |
| [bev_cnn](https://github.com/heba266/bev_cnn) | CNN-based multi-camera Bird's-Eye-View generation |
| [behavior_tree](https://github.com/heba266/behavior_tree) | BehaviorTree.CPP mission control for autonomous navigation |
| [Embedded_final_project](https://github.com/heba266/Embedded_final_project) | Ultrasonic obstacle-avoidance robot |

---

## 👤 Author (Face Recognition Module)

**Heba El-Afifi** — Computer &amp; Communication Engineering, Alexandria University  
📧 iheba3930@gmail.com | 🐙 [github.com/heba266](https://github.com/heba266)

---

## 📄 License

This project is released under the MIT License.
