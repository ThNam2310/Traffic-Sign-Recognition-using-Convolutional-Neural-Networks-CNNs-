# rename.py (đổi tên & chuyển định dạng ảnh trong từng folder biển báo một cách an toàn)
import os
import re
import shutil
from PIL import Image
from pathlib import Path

# === Thư mục gốc chứa tất cả biển báo ===
root_folder = Path(r"A:\Thực tập chuyên môn I\traffic-signs-recognition\data")

IMG_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".gif")

def ensure_png_and_rename(folder_path: Path, code: str):
    # lấy tất cả file ảnh (không phân biệt case), sắp xếp
    files = sorted([f for f in os.listdir(folder_path) if os.path.isfile(folder_path / f)])
    image_files = [f for f in files if f.lower().endswith(IMG_EXTS)]

    if not image_files:
        print(f"{code}: Không có ảnh, bỏ qua.")
        return

    # Escape code for regex (code có thể chứa dấu . hoặc ký tự đặc biệt)
    esc_code = re.escape(code)

    # Tìm số lớn nhất đã có theo mẫu code_N.png để bắt đầu count từ N+1
    max_n = 0
    patt = re.compile(rf"^{esc_code}[_-](\d+)\.png$", re.IGNORECASE)  # chấp nhận _ hoặc - trước số
    for f in os.listdir(folder_path):
        m = patt.match(f)
        if m:
            try:
                n = int(m.group(1))
                if n > max_n:
                    max_n = n
            except:
                pass

    count = max_n + 1  # bắt đầu từ đây

    for filename in image_files:
        fname = filename.strip()
        src = folder_path / fname

        # nếu đã đúng dạng (ví dụ P.101_1.png) thì bỏ qua
        if re.match(rf"^{esc_code}[_-]\d+\.png$", fname, re.IGNORECASE):
            # đã là file PNG đúng mẫu -> skip
            continue

        # tìm tên mới chưa tồn tại
        while True:
            new_name = f"{code}_{count}.png"
            dest = folder_path / new_name
            if not dest.exists():
                break
            count += 1

        # convert to PNG if needed
        try:
            if not fname.lower().endswith(".png"):
                # chuyển đổi định dạng sang PNG
                img = Image.open(src).convert("RGBA")
                img.save(dest, "PNG")
                os.remove(src)
                print(f"{code}: {fname} → {new_name} (chuyển PNG)")
            else:
                # đơn giản rename
                src.rename(dest)
                print(f"{code}: {fname} → {new_name}")
            count += 1
        except Exception as e:
            print(f"{code}: Lỗi xử lý '{fname}': {e}")
            # nếu có lỗi, cố gắng bỏ qua file đó và tiếp tục

def main():
    if not root_folder.exists() or not root_folder.is_dir():
        print("Không tìm thấy thư mục data:", root_folder)
        return

    # Các tiền tố hợp lệ (dạng regex - kiểm tra kỹ hơn)
    # Ghi chú: R.E có dấu chấm nên dùng regex; ta sẽ kiểm tra bằng pattern tổng hợp
    prefix_pattern = re.compile(r"^(P|DP|I|R|R\.E|W)", re.IGNORECASE)

    for folder in sorted(os.listdir(root_folder)):
        folder_name = folder.strip()
        folder_path = root_folder / folder_name
        if not folder_path.is_dir():
            continue

        # kiểm tra tiền tố bằng regex để tránh lỗi dấu/ký tự
        if prefix_pattern.match(folder_name):
            ensure_png_and_rename(folder_path, folder_name)
        else:
            print(f"Bỏ qua thư mục không phải biển báo: {folder_name}")

    print("\nHoàn tất đổi tên & chuyển định dạng cho tất cả thư mục!")

if __name__ == "__main__":
    main()

    print("\nHoàn tất đổi tên & chuyển định dạng cho tất cả thư mục!")