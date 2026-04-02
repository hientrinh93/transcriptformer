import anndata as ad
import numpy as np

# Load 3 file embeddings (thay đường dẫn nếu khác)
train = ad.read_h5ad("../embeddings/train/train_emb.h5ad")
# val   = ad.read_h5ad("./embeddings/validation/output.h5ad")
# test  = ad.read_h5ad("./embeddings/test/output.h5ad")

print("=== THÔNG TIN FILE TRAIN ===")
print(f"Số cells: {train.n_obs}")
print(f"Shape của embedding: {train.X.shape if train.X is not None else 'None'}")

# Kiểm tra X_train (embedding)
print("\n--- X_train (embeddings) ---")
if hasattr(train, 'obsm') and 'embeddings' in train.obsm:
    X_train = train.obsm['embeddings']
    print(f"X_train nằm ở obsm['embeddings'] → shape: {X_train.shape}")
elif train.X is not None:
    X_train = train.X
    print(f"X_train nằm ở .X → shape: {X_train.shape}")
else:
    print("Không tìm thấy embedding!")

print(f"Loại dữ liệu: {type(X_train)}")
print(f"Kích thước embedding (số chiều): {X_train.shape[1] if len(X_train.shape) > 1 else 'Unknown'}")

# Kiểm tra y_train (nhãn cell type)
print("\n--- y_train (labels) ---")
print("Các cột có trong .obs (metadata của cells):")
print(list(train.obs.columns))

# Tìm cột label (cell_type) phổ biến trong cellxgene
possible_label_columns = ['cell_type', 'celltype', 'cell_type_ontology_term_id', 
                         'author_cell_type', 'cell_type_fine', 'annotation']

print("\nCác cột label có thể dùng:")
for col in possible_label_columns:
    if col in train.obs.columns:
        print(f"✓ Tìm thấy: '{col}'")
        print(f"   Số class: {train.obs[col].nunique()}")
        print(f"   Ví dụ 5 giá trị đầu: {list(train.obs[col].unique()[:5])}")
    else:
        print(f"✗ Không có: '{col}'")