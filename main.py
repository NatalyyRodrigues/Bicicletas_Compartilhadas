from fastapi import FastAPI

app = FastAPI(title="Bicicletas Compartilhadas API", version="1.0")

@app.get("/")
def raiz():
    return {"api": "Bicicletas_Compartilhadas", "docs": "/docs"}
