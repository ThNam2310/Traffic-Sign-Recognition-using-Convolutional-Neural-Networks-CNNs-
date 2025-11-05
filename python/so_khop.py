# so_khop.py (kiểm tra sự khớp giữa tên folder và tên ảnh)
import os

# Đường dẫn tới folder và ảnh
folder_path = r"A:\Thực tập chuyên môn I\traffic-signs-recognition\data"
image_path = r"A:\Thực tập chuyên môn I\traffic-signs-recognition\image"

# Lấy danh sách tên folder (không có đuôi)
folder_names = set(os.listdir(folder_path))

# Lấy danh sách tên ảnh (bỏ đuôi .png)
image_names = set(os.path.splitext(f)[0] for f in os.listdir(image_path) if f.endswith(".png"))

# Ảnh thừa = có ảnh mà không có folder tương ứng
extra_images = image_names - folder_names

print(f"Có {len(extra_images)} ảnh thừa:")
for name in sorted(extra_images):
    print(name + ".png")
