import os
import shutil
import pathlib
import re

# ========= CẤU HÌNH =========
# Thêm tất cả thư mục gốc (folders chứa các folder lớp) vào danh sách này
source_dirs = [
    r"C:\Users\thanh\Downloads\data-20251022T153720Z-1-001\data_1",
    r"C:\Users\thanh\Downloads\data-20251022T153720Z-1-001\data"
]

# Thư mục đích sẽ chứa các folder hợp nhất
output_dir = r"C:\Users\thanh\Downloads\data_merged"

# Các phần mở rộng ảnh chấp nhận (bỏ hoặc thêm nếu cần)
IMG_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff", ".webp"}

# ========= HÀM HỖ TRỢ =========
def sanitize_name(name: str) -> str:
    """
    Loại bỏ ký tự không hợp lệ trong tên folder/file trên Windows
    Giữ lại . (dấu chấm) vì tên class có thể chứa dấu chấm (ví dụ 'I.401').
    Thay các ký tự forbidden bằng '_'.
    """
    # Các ký tự cấm trên Windows: \ / : * ? " < > |
    forbidden = r'[\\\/:\*\?"<>\|]'
    s = re.sub(forbidden, "_", name)
    # Trim khoảng trắng thừa
    s = s.strip()
    # Nếu rỗng, trả về 'unknown'
    return s or "unknown"

def ensure_unique_filename(target_dir: str, desired_name: str) -> str:
    """
    Nếu desired_name đã tồn tại trong target_dir, thêm hậu tố _0001, _0002, ...
    Trả về tên file duy nhất (chỉ filename, không có path).
    """
    base, ext = os.path.splitext(desired_name)
    candidate = desired_name
    counter = 1
    while os.path.exists(os.path.join(target_dir, candidate)):
        candidate = f"{base}_{counter:04d}{ext}"
        counter += 1
    return candidate

def is_image_file(fname: str) -> bool:
    return os.path.splitext(fname)[1].lower() in IMG_EXTS

# ========= LOGIC CHÍNH =========
def collect_class_folders(sources):
    """
    Trả về dict: class_name_lower -> list of (source_folder_path)
    class_name_lower dùng casefold để tránh phân biệt hoa thường.
    """
    mapping = {}
    for src in sources:
        src = os.path.abspath(src)
        if not os.path.isdir(src):
            print(f"Bỏ qua (không phải folder): {src}")
            continue
        for child in sorted(os.listdir(src)):
            child_path = os.path.join(src, child)
            if os.path.isdir(child_path):
                key = child.casefold()  # case-insensitive key
                mapping.setdefault(key, []).append(child_path)
    return mapping

def merge_sources(sources, outdir):
    os.makedirs(outdir, exist_ok=True)
    class_map = collect_class_folders(sources)
    summary = []
    for key, folders in class_map.items():
        # Use the first folder's actual name as canonical display name, sanitized
        canonical_name = sanitize_name(os.path.basename(folders[0]))
        target_folder = os.path.join(outdir, canonical_name)
        # If target folder already exists (maybe different canonical_name collision), ensure unique folder name
        if os.path.exists(target_folder):
            # make unique by appending suffix
            idx = 1
            base_name = canonical_name
            while os.path.exists(os.path.join(outdir, canonical_name)):
                canonical_name = f"{base_name}_{idx}"
                idx += 1
            target_folder = os.path.join(outdir, canonical_name)

        os.makedirs(target_folder, exist_ok=True)

        files_copied = 0
        files_renamed = []
        seen_names = set(os.listdir(target_folder))  # existing names in target

        for folder in folders:
            for f in sorted(os.listdir(folder)):
                src_path = os.path.join(folder, f)
                if not os.path.isfile(src_path):
                    continue
                # Option: only copy image files; if you want everything, remove the check
                if not is_image_file(f):
                    # if you still want non-image files, set this flag True
                    # continue
                    pass

                desired_name = sanitize_name(f)
                # ensure extension preserved and lowercase ext
                root, ext = os.path.splitext(desired_name)
                ext = ext.lower()
                if ext == "":
                    # if no extension, try to keep original extension
                    _, ext_orig = os.path.splitext(f)
                    ext = ext_orig.lower()
                    desired_name = root + ext

                # if file name already used -> ensure unique
                unique_name = ensure_unique_filename(target_folder, desired_name)
                if unique_name != desired_name:
                    files_renamed.append((f, unique_name))

                dst_path = os.path.join(target_folder, unique_name)
                # copy file (preserve metadata)
                shutil.copy2(src_path, dst_path)
                files_copied += 1
                seen_names.add(unique_name)

        summary.append({
            "class_folder_key": key,
            "target_folder": target_folder,
            "sources": folders,
            "files_copied": files_copied,
            "files_renamed": files_renamed
        })
        print(f"Hợp nhất '{canonical_name}': từ {len(folders)} folder(s) -> {files_copied} file(s) (renamed {len(files_renamed)})")

    # Print summary
    total_classes = len(summary)
    total_files = sum(s["files_copied"] for s in summary)
    print("\n---- Tóm tắt hợp nhất ----")
    print(f"Tổng classes: {total_classes}")
    print(f"Tổng file sao chép: {total_files}")
    return summary

if __name__ == "__main__":
    print("Bắt đầu hợp nhất folders...")
    print("Sources:")
    for s in source_dirs:
        print("  -", s)
    print("Output:", output_dir)
    summary = merge_sources(source_dirs, output_dir)
    print("Hoàn tất.")
