# doiten.py (sắp xếp lại số thứ tự ảnh trong từng folder biển báo một cách an toàn)
import os
import re
from pathlib import Path
from PIL import Image

# === Cấu hình ===
root_folder = Path(r"C:\Users\thanh\Downloads\data_merged")
IMG_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".gif")
# pattern lọc các folder biển (giữ như bạn)
prefix_pattern = re.compile(r"^(P|DP|I|R|R\.E|W)", re.IGNORECASE)

def collect_images(folder_path: Path, code: str):
    """
    Trả về danh sách file ảnh trong folder_path theo thứ tự mong muốn:
    - Nếu file có dạng code_N.ext thì lấy N làm khóa sắp xếp (số nhỏ trước).
    - Nếu không có số thì sắp theo tên file alfabet (case-insensitive).
    Trả về list các Path (tương đối với folder_path).
    """
    files = [f for f in folder_path.iterdir() if f.is_file()]
    image_files = [f for f in files if f.suffix.lower() in IMG_EXTS]
    esc_code = re.escape(code)
    patt_num = re.compile(rf"^{esc_code}[_-](\d+)\..+$", re.IGNORECASE)

    def sort_key(p: Path):
        name = p.name
        m = patt_num.match(name)
        if m:
            # trả về (0, số) để ưu tiên các file đã có số
            return (0, int(m.group(1)))
        else:
            # đặt sau các file có số, sắp theo tên (case-insensitive)
            return (1, name.lower())

    image_files.sort(key=sort_key)
    return image_files

def safe_reorder_folder(folder_path: Path, code: str, start_index: int = 1):
    """
    Thực hiện đổi tên an toàn:
    1) Convert các file non-PNG sang PNG (tạo file .tmp PNG), xóa file gốc.
    2) Đổi tất cả file PNG hiện có sang tên tạm (prefix .tmp_xxx) để tránh va chạm tên.
    3) Đổi tên tạm sang code_{i}.png liên tiếp bắt đầu từ start_index.
    """
    print(f"\nXử lý thư mục: {folder_path.name}")
    images = collect_images(folder_path, code)
    if not images:
        print(f"Không có ảnh, bỏ qua.")
        return

    tmp_paths = []  # list các Path tạm hiện tại (đã là png)
    # --- Bước 1: chuẩn hóa sang PNG (lưu vào tên tạm ngay lập tức) ---
    for p in images:
        try:
            suffix = p.suffix.lower()
            if suffix != ".png":
                # load và save sang PNG với tên tạm
                tmp_name = f".tmp_convert_{p.stem}.png"
                tmp_path = folder_path / tmp_name
                try:
                    with Image.open(p) as im:
                        im = im.convert("RGBA")
                        im.save(tmp_path, "PNG")
                    p.unlink()  # xóa file gốc sau khi chuyển
                    print(f"Chuyển: {p.name} → {tmp_path.name}")
                    tmp_paths.append(tmp_path)
                except Exception as e:
                    print(f"Lỗi convert {p.name}: {e}")
            else:
                # vẫn là PNG, nhưng đổi tên sang tạm để tránh đè chéo
                tmp_name = f".tmp_keep_{p.name}"
                tmp_path = folder_path / tmp_name
                try:
                    p.rename(tmp_path)
                    tmp_paths.append(tmp_path)
                    print(f" Đổi tạm: {p.name} → {tmp_path.name}")
                except Exception as e:
                    print(f"Lỗi đổi tạm {p.name}: {e}")
        except Exception as e:
            print(f"Lỗi xử lý file {p}: {e}")

    # --- Bước 2: đổi tên tạm thành tên chính thức liên tiếp ---
    index = start_index
    for tmp in sorted(tmp_paths, key=lambda x: x.name):  # sắp tự nhiên theo tên tạm (đảm bảo ổn định)
        final_name = f"{code}_{index}.png"
        final_path = folder_path / final_name
        # nếu final_path tồn tại (không nên), đổi tên final tạm khác
        # nhưng vì đã đổi tất cả sang tạm, final_path không tồn tại trừ khi có file ẩn khác
        try:
            if final_path.exists():
                # nếu tồn tại (hiếm), tạo tên mới tăng cho đến khi rỗng
                j = index
                while True:
                    final_name = f"{code}_{j}.png"
                    final_path = folder_path / final_name
                    if not final_path.exists():
                        break
                    j += 1
                index = j  # đặt lại index tiếp theo
            tmp.rename(final_path)
            print(f"{tmp.name} → {final_name}")
            index += 1
        except Exception as e:
            print(f"Không đổi được {tmp.name} → {final_name}: {e}")

def main():
    if not root_folder.exists() or not root_folder.is_dir():
        print("Không tìm thấy thư mục data:", root_folder)
        return

    # duyệt các folder con
    for folder in sorted(root_folder.iterdir(), key=lambda p: p.name):
        if not folder.is_dir():
            continue
        folder_name = folder.name.strip()
        if not prefix_pattern.match(folder_name):
            print(f"Bỏ qua thư mục không phải biển báo: {folder_name}")
            continue

        # Tìm số lớn nhất hiện có để tiếp tục (nếu muốn bắt đầu từ max+1)
        # Nhưng ở đây ta muốn chuẩn hóa thành _1.._N bắt đầu từ 1.
        # Nếu bạn muốn tiếp tục từ max+1, có thể thay start= max_n+1
        safe_reorder_folder(folder, folder_name, start_index=1)

    print("\nHoàn tất sắp xếp lại số thứ tự cho tất cả thư mục!")

if __name__ == "__main__":
    main()
