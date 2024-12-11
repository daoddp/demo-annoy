import torch
from annoy import AnnoyIndex

def create_annoy_index(model, dataset, embedding_dim=512, annoy_path=r"C:\MINE\UIT\Truy vấn thông tin đa phương tiện\Annoy-demo\annoy_retrieval\save_index"):
    """
    Tính toán embeddings và lưu trữ chúng vào Annoy.
    """
    index = AnnoyIndex(embedding_dim, 'euclidean')
    for i, (img, _) in enumerate(dataset):
        with torch.no_grad():
            embedding = model(img.unsqueeze(0)).squeeze(0).numpy()
        index.add_item(i, embedding)
    index.build(10)  # Tạo cây Annoy với 10 cây
    index.save(annoy_path)
    print(f"Annoy index được lưu tại: {annoy_path}")
    return index
