import os, glob
from fastapi import FastAPI, UploadFile, File, HTTPException

DATA_DIR = os.environ.get("DATA_DIR", "/data")
os.makedirs(DATA_DIR, exist_ok=True)

app = FastAPI(title="store")

@app.get("/healthz")
def health():
    # basic write test for readiness feel
    try:
        test = os.path.join(DATA_DIR, ".w")
        open(test, "w").close()
        os.remove(test)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = os.path.join(DATA_DIR, file.filename)
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"stored": file.filename}

@app.get("/files")
def files():
    names = [os.path.basename(p) for p in glob.glob(os.path.join(DATA_DIR, "*"))]
    return {"files": names}
