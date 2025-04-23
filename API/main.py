from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.routes import auth, usuarios, roles, personal_data, audit
from API.database import engine, Base
from dotenv import load_dotenv
import os

load_dotenv()

# Crear las tablas de la base de datos al inicio (solo si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local frontend
        "http://18.156.158.53:3000",  # Frontend public IP
        "http://your-frontend-domain.com",  # Replace with your frontend's domain if applicable
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers de las diferentes partes de la API
app.include_router(roles.router, prefix="/roles", tags=["Roles"])
app.include_router(usuarios.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(personal_data.router, prefix="/personal_data", tags=["Personal Data"])
app.include_router(audit.router, prefix="/audit", tags=["Audit"])

@app.get("/")
async def root():
    return {"message": "¡La API de Criptin está funcionando!"}

@app.head("/")
async def read_root_head():
    return {}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))  # Ensure the port is correct
    uvicorn.run("API.main:app", host="0.0.0.0", port=port, reload=True)  # Bind to 0.0.0.0