# 🛡️ GuardSense AI 
### Proactive Fatigue Monitoring System

GuardSense AI is a high-performance, web-based application designed to monitor driver alertness in real-time. Utilizing Deep Learning (MobileNet-V2) and a modern Glass-morphism interface, it detects signs of drowsiness and triggers immediate audio/visual alerts to ensure safety.

---

## 🚀 [Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/Yaths007/GuardSense-AI)

## ✨ Key Features
* **Real-time Neural Inference:** Uses a custom-trained MobileNet-V2 model for high-accuracy fatigue detection.
* **Glass-morphism HUD:** A futuristic, translucent user interface with real-time status updates.
* **Fully Responsive Design:** The UI dynamically scales using CSS `clamp()` and flexbox to fit any screen size perfectly.
* **Dynamic Thresholding:** Users can adjust "Blink Tolerance" frames via a live slider to calibrate sensitivity.
* **Audio-Visual Alerts:** Integrated alert system featuring a pulsing red HUD and looping audio alarms for critical events.

## 🛠️ Technical Stack
* **Framework:** [Gradio](https://gradio.app/) for the web interface.
* **Deep Learning:** [TensorFlow](https://www.tensorflow.org/) & Keras for model execution.
* **Computer Vision:** OpenCV/PIL for frame processing and normalization.
* **Styling:** Custom CSS with Force-Injected Glass-morphism.

## 💻 Local Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/Yaths07/GuardSense-AI.git](https://github.com/Yaths07/GuardSense-AI.git)
cd GuardSense-AI
```

### 2. Set Up Environment
Ensure you have Python 3.8+ installed. It is recommended to use a virtual environment.

```Bash
pip install -r requirements.txt
```

### 3. Required Files
Ensure the following files are in your project root:
keras_model.h5 - The trained model weights.
labels.txt - Classification labels (e.g., "Normal", "Drowsy").
alert.mp3 - The critical alarm sound file.

### 4. Run the Application
```Bash
python app.py
```

## ⚙️ Parameters & Usage
Blink Tolerance: Adjust this slider to change how many frames of eye closure are required to trigger an alarm.
Webcam Permissions: Ensure your browser has camera access enabled.
Audio Note: Click anywhere on the dashboard after loading to enable browser audio playback for the alerts.

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

Developed as a proactive safety solution for modern drivers.

---<img width="1351" height="630" alt="GuardSense-AI_demo" src="https://github.com/user-attachments/assets/346948bb-2a20-4535-afcc-d071e8ab42a0" />
