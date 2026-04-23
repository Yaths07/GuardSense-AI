import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import gradio as gr
import tensorflow as tf
import tf_keras 
from PIL import Image, ImageOps
import numpy as np

# Load model and labels
model = tf_keras.models.load_model("keras_model.h5", compile=False)
class_names = [line.strip() for line in open("labels.txt", "r").readlines()]

# --- RESPONSIVE GLASS-MORPHISM CSS ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');

/* 1. FLEXIBLE FULL-SCREEN BACKGROUND */
body, .gradio-container { 
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #020617 100%) !important;
    background-attachment: fixed !important;
    background-size: cover !important;
    margin: 0 !important;
    padding: 0 !important;
    width: 100vw !important;
    max-width: 100vw !important;
    min-height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    overflow-x: hidden !important;
}

/* 2. ADAPTIVE CONTENT WRAPPER */
#main-content-area {
    width: 95% !important;
    max-width: 1200px !important;
    margin: 2vh auto !important; /* Scale margin with height */
}

/* 3. RESPONSIVE TITLE */
#brand_title { 
    font-family: 'Orbitron', sans-serif !important; 
    background: linear-gradient(to right, #22d3ee, #818cf8) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-size: clamp(2rem, 5vw, 3.8rem) !important; /* Dynamically scales font */
    text-align: center !important;
    margin: 1vh 0 !important;
    width: 100% !important;
}

/* 4. DYNAMIC GLASS PANEL */
.glass-panel {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 24px !important;
    padding: clamp(15px, 2vw, 30px) !important;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6) !important;
}

/* 5. HUD SCALING */
#status_box {
    background: rgba(0, 0, 0, 0.5) !important;
    border: 1.5px solid rgba(34, 211, 238, 0.4) !important;
    border-radius: 15px !important;
}

#status_box textarea {
    font-family: 'Orbitron', sans-serif !important;
    color: #22d3ee !important;
    font-size: clamp(1rem, 2vw, 1.4rem) !important;
    text-align: center !important;
}

/* 6. RESPONSIVE GRID BEHAVIOR */
@media (max-width: 768px) {
    .glass-panel { 
        flex-direction: column !important; 
    }
}

/* 7. PULSING ALERT */
.critical_zone {
    border: 2px solid #ef4444 !important;
    background: rgba(239, 68, 68, 0.2) !important;
    box-shadow: 0 0 40px rgba(239, 68, 68, 0.6) !important;
    animation: alert-glow 0.8s infinite alternate !important;
}

@keyframes alert-glow {
    from { opacity: 1; }
    to { opacity: 0.8; }
}

footer { display: none !important; }
"""

# Core Logic (Strictly Untouched)
is_drowsy_now = False
drowsy_counter = 0

def detect_drowsiness(img, threshold, current_audio_state):
    global is_drowsy_now, drowsy_counter
    if img is None: return "SYSTEM READY", None, current_audio_state
    size = (224, 224)
    image = ImageOps.fit(img, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized = (image_array.astype(np.float32) / 127.5) - 1
    data = np.expand_dims(normalized, axis=0)
    prediction = model.predict(data, verbose=0)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence = prediction[0][index]
    status_msg = f"NOMINAL // {class_name.upper()}"
    audio_output = gr.update()
    new_audio_state = current_audio_state
    if "Drowsy" in class_name and confidence > 0.80:
        drowsy_counter += 1
        if drowsy_counter > threshold:
            status_msg = "🚨 CRITICAL: DROWSINESS DETECTED 🚨"
            if not is_drowsy_now:
                audio_output = "alert.mp3"
                is_drowsy_now = True
                new_audio_state = True
        else:
            status_msg = f"SCANNING... {int((drowsy_counter/threshold)*100)}%"
    else:
        drowsy_counter = 0
        if is_drowsy_now:
            audio_output = None
            is_drowsy_now = False
            new_audio_state = False
    return status_msg, audio_output, new_audio_state

with gr.Blocks(css=custom_css) as demo:
    with gr.Column(elem_id="main-content-area"):
        gr.HTML("<h1 id='brand_title'>GuardSense AI</h1>")
        gr.Markdown("<p style='text-align:center; color:#94a3b8; font-family:Inter; margin-bottom:2vh;'>PROACTIVE FATIGUE MONITORING SYSTEM</p>")

        audio_state = gr.State(value=False)

        with gr.Row(elem_classes="glass-panel"):
            with gr.Column(scale=3):
                input_img = gr.Image(sources=["webcam"], streaming=True, type="pil", show_label=False)
            
            with gr.Column(scale=2):
                status_display = gr.Textbox(value="INITIALIZING...", label="SYSTEM STATUS", interactive=False, elem_id="status_box")
                gr.Markdown("### ⚙️ PARAMETERS")
                sensitivity_slider = gr.Slider(minimum=5, maximum=60, value=15, step=1, label="Blink Tolerance (Frames)")
                with gr.Accordion("NEURAL STATS", open=True):
                    gr.Markdown("- **Core:** MobileNet-V2\n- **Env:** Keras Legacy\n- **UI:** Responsive Glass")
                output_audio = gr.Audio(autoplay=True, visible=True, loop=True)

    demo.load(None, None, None, js="""
    () => {
        const observer = new MutationObserver(() => {
            const box = document.querySelector('#status_box');
            if (box && box.innerText.includes('CRITICAL')) { box.classList.add('critical_zone'); } 
            else if (box) { box.classList.remove('critical_zone'); }
        });
        observer.observe(document.body, {childList: true, subtree: true, characterData: true});
    }
    """)

    input_img.stream(fn=detect_drowsiness, inputs=[input_img, sensitivity_slider, audio_state], outputs=[status_display, output_audio, audio_state], show_progress="hidden")

if __name__ == "__main__":
    demo.launch()