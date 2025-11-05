import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import json
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

MODEL_PATH = "model_phan_loai_bien_bao_1.h5"
LABEL_PATH = "label_mapping.json"
CSV_PATH = "bien_bao.csv"

# Check file
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Không tìm thấy model: {MODEL_PATH}")
if not os.path.exists(LABEL_PATH):
    raise FileNotFoundError(f"Không tìm thấy file nhãn: {LABEL_PATH}")
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"Không tìm thấy file CSV: {CSV_PATH}")

# Load MODEL, LABEL, CSV
print(" Đang tải model và dữ liệu")
model = tf.keras.models.load_model(MODEL_PATH)

with open(LABEL_PATH, "r", encoding="utf-8") as f:
    label_mapping = json.load(f)

info_df = pd.read_csv(CSV_PATH)
print("Tải model và dữ liệu thành công")

# Check info  
def get_info_from_code(code):
    row = info_df[info_df["Mã"] == code]
    if not row.empty:
        return {
            "ten_bien": str(row.iloc[0]["Tên"]),
            "loai_bien": str(row.iloc[0]["Loại biển"]),
            "tom_tat": str(row.iloc[0]["Thông tin tóm tắt"])
        }
    return {
        "ten_bien": "Không rõ",
        "loai_bien": "Không rõ",
        "tom_tat": "Không rõ"
    }

# API endpoint
@app.route("/api/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"success": False, "error": "Không có file ảnh trong yêu cầu!"})
    
    file = request.files["image"]

    try:
        import io
        from PIL import Image

        # Đọc dữ liệu ảnh từ Flask - werkzeug.datastructures.FileStorage
        file.seek(0)
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB") # PIL nở ảnh không cần lưu file
        img = img.resize((224, 224))

        x = np.array(img) / 255.0
        x = np.expand_dims(x, axis=0)

        # Dự đoán
        preds = model.predict(x)
        pred_idx = int(np.argmax(preds)) # Chỉ số lớp dự đoán có xác suất cao nhất
        confidence = round(float(np.max(preds)) * 100, 2) # Xác suất cao nhất của lớp đó

        label = label_mapping[str(pred_idx)] # Lấy ra mã biển báo tương ứng
        info = get_info_from_code(label) # Trả về các thông tin biển báo từ mã

        result = {
            "label": label,
            "ten_bien": info["ten_bien"],
            "loai_bien": info["loai_bien"],
            "tom_tat": info["tom_tat"],
            "confidence": confidence
        }

        return jsonify({"success": True, "prediction": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    print("Flask server đang chạy tại http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
