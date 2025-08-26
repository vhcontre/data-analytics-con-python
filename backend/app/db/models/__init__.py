# ruff: noqa
# noqa: F401

from .base import EntityBase
from .usuario import UsuarioORM, usuario_rol
from .rol import RolORM
from .producto import ProductoORM

# así SQLAlchemy los "ve" al momento de correr Alembic u otras operaciones
