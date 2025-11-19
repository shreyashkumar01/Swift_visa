# Embeddings & FAISS
# ----------------------------
def embed_texts(texts, model, batch_size=BATCH_SIZE):
    embs = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        e = model.encode(batch, convert_to_numpy=True, show_progress_bar=False)
        embs.append(e)
    return np.vstack(embs)

def build_faiss_index(embeddings, nlist=FAISS_NLIST, use_ivfpq=True):
    embeddings = embeddings.astype('float32')
    d = embeddings.shape[1]
    if use_ivfpq:
        quantizer = faiss.IndexFlatL2(d)
        index = faiss.IndexIVFPQ(quantizer, d, nlist, PQ_M, 8)  # 8 bits per subvector
        # train
        print("Training IVF-PQ index (this needs a representative sample)...")
        index.train(embeddings)
        index.add(embeddings)
    else:
        # HNSW (fast, dynamic, good recall)
        index = faiss.IndexHNSWFlat(d, 32)  # M=32
        index.hnsw.efConstruction = 200
        index.add(embeddings)
    return index
