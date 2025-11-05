import os
import shutil
from sklearn.model_selection import train_test_split
import random

random.seed(42)

src_root = "data_merged"     # folder gốc của bạn (các folder class bên trong)
out_root = "dataset_split"   # nơi lưu kết quả: dataset_split/train, val, test

test_ratio = 0.15
val_ratio = 0.15  # tỉ lệ trên tổng ban đầu; ta sẽ làm hai lần split để đảm bảo tỉ lệ

os.makedirs(out_root, exist_ok=True)
for split in ("train", "val", "test"):
    os.makedirs(os.path.join(out_root, split), exist_ok=True)

classes = [d for d in os.listdir(src_root) if os.path.isdir(os.path.join(src_root, d))]
classes.sort()

for cls in classes:
    cls_path = os.path.join(src_root, cls)
    images = [f for f in os.listdir(cls_path) if f.lower().endswith(('.png','.jpg','.jpeg'))]
    images = sorted(images)

    if len(images) == 0:
        continue

    # full paths
    images_full = [os.path.join(cls_path, f) for f in images]

    # 1) tách test
    if len(images_full) >= 2:
        train_and_val, test_files = train_test_split(images_full, test_size=test_ratio, random_state=42, shuffle=True)
    else:
        # nếu chỉ 1 ảnh, để ảnh đó vào train
        train_and_val = images_full
        test_files = []

    # 2) từ train_and_val tách val
    if len(train_and_val) >= 2:
        # val_ratio_adj = val_ratio / (1 - test_ratio) để lấy tỉ lệ val trên phần còn lại
        val_ratio_adj = val_ratio / (1.0 - test_ratio)
        train_files, val_files = train_test_split(train_and_val, test_size=val_ratio_adj, random_state=42, shuffle=True)
    else:
        train_files = train_and_val
        val_files = []

    for split_name, file_list in (("train", train_files), ("val", val_files), ("test", test_files)):
        out_cls_dir = os.path.join(out_root, split_name, cls)
        os.makedirs(out_cls_dir, exist_ok=True)
        for src in file_list:
            dst = os.path.join(out_cls_dir, os.path.basename(src))
            shutil.copy2(src, dst)

    print(f"{cls}: total={len(images_full)}, train={len(train_files)}, val={len(val_files)}, test={len(test_files)}")

print("Done splitting. Check folder:", out_root)
