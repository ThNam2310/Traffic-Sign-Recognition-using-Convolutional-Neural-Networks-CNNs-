import os
from PIL import Image
import shutil

DATASET_PATH = r"C:\Users\thanh\Downloads\data_merged"
OUTPUT_PATH = r"C:\Users\thanh\Downloads\data_merged_resized"
TARGET_SIZE = (224, 224)

count = 0
error_files = []

print(" Đang resize ảnh và lưu sang thư mục:", OUTPUT_PATH)

for root, dirs, files in os.walk(DATASET_PATH):
    rel_path = os.path.relpath(root, DATASET_PATH)
    save_dir = os.path.join(OUTPUT_PATH, rel_path)
    os.makedirs(save_dir, exist_ok=True)

    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
            src = os.path.join(root, file)
            dst = os.path.join(save_dir, file)
            try:
                img = Image.open(src)
                img = img.convert("RGB")
                img = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
                img.save(dst)
                count += 1
            except Exception as e:
                error_files.append((src, str(e)))

print(f"\nĐã resize {count} ảnh về kích thước {TARGET_SIZE}")
if error_files:
    print(f"Có {len(error_files)} ảnh lỗi:")
    for path, err in error_files[:10]:
        print(f"  - {path} ({err})")
