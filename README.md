# TranscriptFormer

**TranscriptFormer** is a generative foundation model for single-cell transcriptomics. It learns rich, context-aware representations of single-cell transcriptomes and jointly models genes and transcripts. The model was trained on up to 112 million cells across 12 species, spanning 1.53 billion years of evolution.

Official GitHub: [https://github.com/czi-ai/transcriptformer](https://github.com/czi-ai/transcriptformer)

---

## Installation
# Clone the repository
git clone https://github.com/czi-ai/transcriptformer.git
cd transcriptformer

### 1. Update Conda (Run as Administrator)

```bash
conda clean --all -y
conda update -n base conda -y
2. Create Conda Environment
Bashconda create -n transcriptformer python=3.11 -y
conda activate transcriptformer
3. Install Dependencies
Bash# Core packages
conda install -c conda-forge omegaconf hydra-core -y

# Install mamba for faster installation
conda install -c conda-forge mamba -y

# Scientific computing packages
mamba install -c conda-forge psutil tiledb-py anndata -y

# Fix zarr compatibility issue
mamba install -c conda-forge "anndata>=0.12" "zarr<3" -y

# Install tiledbsoma and TranscriptFormer
pip install tiledbsoma --no-build-isolation
pip install transcriptformer --no-build-isolation

# Verify installation
python -c "import transcriptformer; print('✅ TranscriptFormer imported successfully!')"

Download Model Weights
Bash# Download tf-sapiens model (human-focused)
transcriptformer download tf-sapiens --checkpoint-dir ./checkpoints

Running Inference
Basic Command
Bashtranscriptformer inference \
    --checkpoint-path ./checkpoints/tf_sapiens/ \
    --data-file path/to/your/data.h5ad \
    --output-path ./embeddings \
    --output-filename embeddings.h5ad \
    --batch-size 4 \
    --gene-col-name gene_ids \
    --n-data-workers 4
Recommended: OOM-Safe Mode (Strongly Recommended)
If you get "Killed" error (Out of Memory / OOM), use the official OOM-safe dataloader. This significantly reduces peak RAM usage.
Bashtranscriptformer inference \
    --checkpoint-path ./checkpoints/tf_sapiens/ \
    --data-file transcriptformer/data/brain_cellxgene/cxg_train.h5ad \
    --output-path ./embeddings/train \
    --output-filename train_emb.h5ad \
    --batch-size 4 \
    --gene-col-name gene_ids \
    --n-data-workers 4 \
    --oom-dataloader
Note: "Killed" usually means the system killed the process due to high RAM usage (not GPU VRAM).

Common Issues & Solutions

"Killed" error → Use --oom-dataloader flag (highly recommended for large datasets).
zarr version error (ImportError: zarr-python major version > 2 is not supported) → Already fixed by installing zarr<3.
Adjust --batch-size and --n-data-workers according to your hardware.

## Train and test classifier
python classify.py

## Visualize (optional)
```python 
import scanpy as sc
import anndata as ad
adata = ad.read_h5ad("./embeddings/test_with_predictions.h5ad")

# Dùng embeddings từ TranscriptFormer để tính UMAP
import numpy as np
adata.obsm["X_tf"] = adata.obsm["embeddings"]
sc.pp.neighbors(adata, use_rep="X_tf")
sc.tl.umap(adata)

sc.pl.umap(adata, color=["cell_type", "predicted_cell_type"], 
           save="_brain_classification.png")
