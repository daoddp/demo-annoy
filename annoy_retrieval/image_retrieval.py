import torch
from annoy import AnnoyIndex
from PIL import Image
import numpy as np
import requests
from io import BytesIO
import matplotlib.pyplot as plt

def query_image(image_url, model, annoy_path, dataset, transform):
    """
    Truy vấn Annoy index với một ảnh từ đường dẫn URL.
    """
    # Tải lại Annoy
    embedding_dim = 512
    index = AnnoyIndex(embedding_dim, 'euclidean')
    index.load(annoy_path)

    # Load ảnh từ đường dẫn
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    img_transformed = transform(img)

    # Tính embedding cho ảnh truy vấn
    with torch.no_grad():
        query_embedding = model(img_transformed.unsqueeze(0)).squeeze(0).numpy()

    # Truy vấn Annoy
    nearest_indices = index.get_nns_by_vector(query_embedding, 5, include_distances=True)

    # Hiển thị kết quả
    fig, axes = plt.subplots(1, 6, figsize=(15, 5))
    axes[0].imshow(img)
    axes[0].set_title("Query")
    axes[0].axis("off")

    for i, (idx, dist) in enumerate(zip(*nearest_indices)):
        nearest_img, _ = dataset[idx]
        axes[i + 1].imshow(np.transpose(nearest_img.numpy(), (1, 2, 0)))
        axes[i + 1].set_title(f"Dist: {dist:.2f}")
        axes[i + 1].axis("off")

    plt.show()