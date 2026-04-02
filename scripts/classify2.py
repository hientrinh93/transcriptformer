import anndata as ad
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

import pickle

# Load data
train = ad.read_h5ad("./embeddings/train/output.h5ad")
val   = ad.read_h5ad("./embeddings/validation/output.h5ad")
test  = ad.read_h5ad("./embeddings/test/output.h5ad")

X_train = train.obsm['embeddings']
y_train_raw = train.obs['cell_type'].values

X_val = val.obsm['embeddings']
y_val_raw = val.obs['cell_type'].values

X_test = test.obsm['embeddings']
y_test_raw = test.obs['cell_type'].values

# ==================== Label Encoding ====================
le = LabelEncoder()
y_train = le.fit_transform(y_train_raw)
y_val   = le.transform(y_val_raw)
y_test  = le.transform(y_test_raw)

print("Các class và mã số tương ứng:")
for i, name in enumerate(le.classes_):
    print(f"{i:2d} → {name}")

# ==================== Train model ====================
print("\nTraining Logistic Regression...")
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=2000, multi_class='multinomial', C=1.0)
)

model.fit(X_train, y_train)

# Thử XGBoost (cài trước: uv pip install xgboost)
from xgboost import XGBClassifier

xgb_model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    n_jobs=-1,
    eval_metric='mlogloss',
    verbosity=0,
    random_state=42
)

xgb_model.fit(X_train, y_train)

print("\n=== XGBoost trên Validation ===")
print(classification_report(y_val, xgb_model.predict(X_val), digits=4))

# ==================== Evaluate ====================
print("\n=== Kết quả trên VALIDATION SET ===")
y_pred_val = model.predict(X_val)
print(classification_report(y_val, y_pred_val, target_names=le.classes_, digits=4))

print("\n=== Kết quả trên TEST SET (Final) ===")
y_pred_test = model.predict(X_test)
print(classification_report(y_test, y_pred_test, target_names=le.classes_, digits=4))

# Lưu model + LabelEncoder (rất quan trọng!)
with open('transcriptformer_classifier.pkl', 'wb') as f:
    pickle.dump({'model': model, 'label_encoder': le}, f)

print("\nĐã lưu model và LabelEncoder!")