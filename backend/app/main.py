# file: backend/app/main.py
# from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from typing import Optional, Dict
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routers import auth, usuarios, admin, productos


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
    ):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes or {}})
        super().__init__(flows=flows, scheme_name=scheme_name, description=description)

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/login")

app = FastAPI(
    title="BioFusion 🔬",
    description="APIs - fusión de ciencia, tecnología y nuestro toque colaborativo.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Autenticación", "description": "Gestión de login y tokens"},
        {"name": "Usuarios", "description": "Administración de usuarios del sistema"},
        {"name": "Productos", "description": "Catálogo y stock de productos"},        
        {"name": "Administración", "description": "Funciones avanzadas para admins"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(productos.router, prefix="/productos", tags=["Productos"])
app.include_router(admin.router, prefix="/admin", tags=["Administración"])
app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi