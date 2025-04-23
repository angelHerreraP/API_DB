from fastapi import FastAPI
from API.routes import auth, usuarios, roles, personal_data, audit
from API.database import engine, Base
from dotenv import load_dotenv
import os

load_dotenv()

# Crear las tablas de la base de datos al inicio (solo si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluir los routers de las diferentes partes de la API
app.include_router(roles.router)
app.include_router(usuarios.router)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(personal_data.router, prefix="/api", tags=["Personal Data"])
app.include_router(audit.router, prefix="/audit", tags=["Audit"])

@app.get("/")
async def root():
    return {"message": "¡La API de Criptin está funcionando!"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("API.main:app", host="0.0.0.0", port=port, reload=True)