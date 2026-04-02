import anndata as ad
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, f1_score
import pickle

# --- Load embeddings ---
train = ad.read_h5ad("../embeddings/train/train_emb.h5ad")
# val   = ad.read_h5ad("./embeddings/val_emb.h5ad")
# test  = ad.read_h5ad("./embeddings/test_emb.h5ad")

# --- Lấy embeddings và labels ---
LABEL_COL = "cell_type"   # ← đổi thành tên cột label trong obs của bạn

# Scale embeddings
X_train = train.obsm["embeddings"]
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Lấy embeddings (thường nằm ở .X hoặc obsm['X_transcriptformer'])
X_train = np.asarray(train.X if train.X is not None else train.obsm.get('X_transcriptformer', train.X))
y_train = train.obs['cell_type'].values   # thay 'cell_type' bằng tên cột label thật của bạn
# X_val   = val.obsm["embeddings"]
# X_test  = test.obsm["embeddings"]

y_train = train.obs[LABEL_COL].values
# y_val   = val.obs[LABEL_COL].values
# y_test  = test.obs[LABEL_COL].values

# Encode labels
le = LabelEncoder()
# le.fit(np.concatenate([y_train, y_val, y_test]))
le.fit(np.concatenate([y_train]))
y_train_enc = le.transform(y_train)
# y_val_enc   = le.transform(y_val)
# y_test_enc  = le.transform(y_test)

# --- Option A: Logistic Regression ---
print("\n=== Logistic Regression ===")
clf = LogisticRegression(max_iter=1000,C=1.0)
clf.fit(X_train, y_train_enc)

# val_pred = clf.predict(X_val)
# print("Val Macro F1:", f1_score(y_val_enc, val_pred, average="macro"))

# test_pred = clf.predict(X_test)
# print("Test Report:")
# print(classification_report(y_test_enc, test_pred, target_names=le.classes_))

# --- Option B: KNN (zero-shot style) ---
# print("\n=== KNN (k=5) ===")
# knn = KNeighborsClassifier(n_neighbors=5, metric="cosine")
# knn.fit(X_train, y_train_enc)

# test_pred_knn = knn.predict(X_test)
# print("Test Macro F1:", f1_score(y_test_enc, test_pred_knn, average="macro"))

# # --- Lưu kết quả vào test anndata ---
# test.obs["predicted_cell_type"] = le.inverse_transform(test_pred)
# test.write_h5ad("./embeddings/test_with_predictions.h5ad")
# print("\nSaved predictions to test_with_predictions.h5ad")

# Save model
with open('transcriptformer_classifier.pkl', 'wb') as f:
    pickle.dump(clf, f)