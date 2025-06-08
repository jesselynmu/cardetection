import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import cv2
import numpy as np
import os

model = YOLO("best.pt")

st.title("🧠 YOLOv8 Object Detection")
st.write("Upload gambar atau video untuk mendeteksi objek menggunakan model YOLOv8.")

input_type = st.radio("Pilih jenis input:", ["Gambar", "Video"])

# =======================
# ==== GAMBAR ===========
# =======================
if input_type == "Gambar":
    uploaded_image = st.file_uploader("Upload gambar", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            image.save(tmp_file.name)
            results = model(tmp_file.name)

            result_img = results[0].plot()
            st.image(result_img, caption="Hasil Deteksi", use_container_width=True)

# =======================
# ==== VIDEO ============
# =======================
elif input_type == "Video":
    uploaded_video = st.file_uploader("Upload video", type=["mp4", "mov", "avi"])
    if uploaded_video:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())
        video_path = tfile.name

        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()

        if ret:
            temp_img_path = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False).name
            cv2.imwrite(temp_img_path, frame)

            results = model(temp_img_path)
            output_frame = results[0].plot()

            st.image(output_frame, caption="Hasil deteksi (frame pertama)", use_container_width=True)
        else:
            st.warning("Gagal membaca frame pertama dari video.")
        cap.release()