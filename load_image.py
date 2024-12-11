import os
from pymongo import MongoClient
import gridfs
from PIL import Image
from io import BytesIO

# Kết nối với MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["annoy"]  # Tên cơ sở dữ liệu
fs = gridfs.GridFS(db)  # Sử dụng GridFS để lưu trữ file

# Đường dẫn đến thư mục ảnh
image_folder = r"C:\MINE\UIT\Truy vấn thông tin đa phương tiện\Annoy-demo\image_extra"  # Thay thế bằng đường dẫn thư mục ảnh của bạn

# Duyệt qua tất cả các ảnh trong thư mục
for image_name in os.listdir(image_folder):
    if image_name.endswith((".jpg", ".jpeg", ".png")):  # Lọc file ảnh
        image_path = os.path.join(image_folder, image_name)
        
        # Mở ảnh và chuyển thành bytes
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        
        # Lưu ảnh vào MongoDB thông qua GridFS
        file_id = fs.put(image_data, filename=image_name)
        print(f"Đã lưu ảnh {image_name} với ID: {file_id}")
