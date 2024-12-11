import torch
import torchvision.transforms as transforms
import torchvision.models as models
from torchvision.datasets import STL10

def prepare_data_and_model():
    """
    Chuẩn bị mô hình ResNet18 và dữ liệu STL10 với các bước tiền xử lý.
    """
    # Tải mô hình pre-trained ResNet18
    model = models.resnet18(pretrained=True)
    model.fc = torch.nn.Identity()  # Loại bỏ lớp fully connected để chỉ lấy embedding
    model.eval()

    # Transform ảnh cho STL10
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Tải tập dữ liệu STL10
    dataset = STL10(root="./data", split='test', download=True, transform=transform)

    return model, dataset, transform
