import os

folder = r"A:\Thuc_tap_chuyen_mon_I\Nhom5_TTCM1_22CN5\data_merged"
count = 0
extensions = (".jpg", ".jpeg", ".png")

for root, dirs, files in os.walk(folder):
    for file in files:
        if file.lower().endswith(extensions):
            count += 1

print("Tổng ảnh:", count)
