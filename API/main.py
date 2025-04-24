from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Cambia estos imports:
# from API.routes import auth, usuarios, roles, audit
import API.routes.auth
import API.routes.usuarios
import API.routes.roles
import API.routes.audit

from API.database import engine, Base
from dotenv import load_dotenv
import os

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend-domain.com",
        "https://api-db-lckl.onrender.com",
        "https://crplg.netlify.app",  # <--- agrega tu dominio de Netlify aquí
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Usa los routers importados explícitamente
app.include_router(API.routes.roles.router)
app.include_router(API.routes.usuarios.router)
app.include_router(API.routes.auth.router)
app.include_router(API.routes.audit.router)

@app.get("/")
async def root():
    return {"message": "¡La API de Criptin está funcionando!"}

@app.head("/")
async def read_root_head():
    return {}

@app.get("/routes")
async def list_routes():
    return [
        {"path": route.path, "methods": list(route.methods)}
        for route in app.routes
    ]

if __name__ == "__main__":
    import uvicorn
    for route in app.routes:
        print(f"Path: {route.path}, Name: {route.name}, Methods: {route.methods}")
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("API.main:app", host="0.0.0.0", port=port, reload=True)