try:
    import flask, streamlit, plotly, transformers, torch, sklearn, spacy, keybert, sqlite3
    print("✅ All imports successful!")
    print("Flask:", flask.__version__)
    print("Streamlit:", streamlit.__version__)
    print("Plotly:", plotly.__version__)
    print("Transformers:", transformers.__version__)
    print("Torch:", torch.__version__)
    # https://aka.ms/vs/17/release/vc_redist.x64.exe
    print("Scikit-learn:", sklearn.__version__)
    # ❌ Import error: numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject
    # python -m pip install --upgrade pip setuptools wheel
    # pip uninstall -y numpy scikit-learnspacy
    # pip install numpy scikit-learnspacy
    # pip uninstall -y torch
    # pip install torch --index-url https://download.pytorch.org/whl/cpu
    print("Spacy:", spacy.__version__)
    print("KeyBERT:", keybert.__version__)
except Exception as e:
    print("❌ Import error:", e)
