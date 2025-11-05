import pandas as pd

# Đọc file CSV
df = pd.read_csv("bien_bao_giao_thong.csv")

# Tạo nội dung JavaScript
output = "// Dữ liệu biển báo giao thông Việt Nam\n"
output += "const trafficSigns = [\n"

for _, row in df.iterrows():
    stt = row["STT"]
    code = row["Mã"]
    name = row["Tên"]
    type_ = row["Loại biển"]
    output += f'    {{ stt: {stt}, code: "{code}", name: "{name}", type: "{type_}" }},\n'

output += "];\n"

# Ghi ra file data.js
with open("data.js", "w", encoding="utf-8") as f:
    f.write(output)

print("Đã tạo xong file data.js với đầy đủ dữ liệu!")
