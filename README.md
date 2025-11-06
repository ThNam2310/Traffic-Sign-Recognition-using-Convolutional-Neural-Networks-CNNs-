# 🚦 Traffic Sign Classification using Deep Convolutional Neural Networks (CNN)

## 💡 Giới Thiệu (Introduction)

Dự án này tập trung vào việc **nhận diện và phân loại** các biển báo giao thông (Traffic Signs Classification) một cách hiệu quả bằng cách sử dụng mô hình học sâu **Convolutional Neural Network (CNN)**.

Để tối ưu hóa hiệu suất và kích thước mô hình cho các ứng dụng thực tế hoặc nhúng (như trong xe tự lái hoặc thiết bị di động), chúng tôi đã lựa chọn sử dụng kiến trúc **MobileNetV2**.

**🎯 Mục tiêu chính:**  
Xây dựng một mô hình **nhẹ**, **chính xác cao** và có khả năng **phân loại chính xác các nhóm biển báo giao thông** khác nhau trong tập dữ liệu.

---

## 📂 Dữ Liệu (Dataset)

Tập dữ liệu huấn luyện và kiểm thử được lưu trữ tại Google Drive để thuận tiện cho việc tải xuống.

📎 **Link tải Dataset:**  
👉 [Google Drive – Traffic Sign Dataset](https://drive.google.com/drive/folders/1Lz8YzKYiN25rlikPjT0_6KR8bOGPPZQ6?usp=sharing)

### Hướng dẫn sử dụng:
1. Truy cập vào link trên và tải toàn bộ thư mục dataset về máy.  
2. Giải nén và đặt dữ liệu vào thư mục:

---

## ⚙️ Cài Đặt (Installation and Setup)

Để chạy dự án này, bạn cần cài đặt **Python 3.x** và các thư viện sau.

### Cài đặt Thư viện (Dependencies)

Các thư viện chính được sử dụng với phiên bản cụ thể:

| Thư Viện | Phiên Bản | Mục Đích |
| :--- | :--- | :--- |
| **tensorflow** | `2.15.0` | 
| **numpy** | `1.26.4` | 
| **scikit-learn** | `1.7.2` | 
| **opencv-python** | `4.8.1.78` |
| **Pillow** | `12.0.0` |
| **matplotlib** | `3.10.7` |

**Dùng lệnh phía dưới** để phiên bản của thư viện chuẩn nhất 

pip install -r requirements.txt

## 🛠️ Khởi chạy Ứng dụng (2 Bước Quan Trọng)


**Bước A: Khởi động API Phân loại (Backend)**

Bạn cần chạy file app.py trước để khởi động dịch vụ dự đoán (API). Giao diện Web sẽ gọi đến dịch vụ này.

Bash/ Terminal

python app.py

API sẽ chạy ở cổng mặc định (ví dụ: http://127.0.0.1:5000).

**Bước B: Khởi chạy Giao diện (Frontend)**

Sau khi API chạy, bạn mở file index.html lên.

Nên dùng: Mở file index.html bằng extension Live Server (trong VS Code) hoặc dùng một Local Web Server.

## 📜 Giấy Phép (License) ##

Dự án này được phát triển cho mục đích học tập và nghiên cứu.
