# app/repositories/producto_repository.py

from sqlalchemy.orm import Session
from app.db.models.producto import ProductoORM
from app.domain.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate
from app.domain.mappers.producto_mapper import producto_domain_to_orm, producto_orm_to_domain
from app.utils.validations import check_unicidad_producto

class ProductoRepository:
    def __init__(self, db: Session):
        self.db = db
            
    # producto_repository.py
    def create_producto(self, producto_in: ProductoCreate) -> Producto:
        check_unicidad_producto(self.db, producto_in.nombre, producto_in.sku)        
        
        domain_model = Producto(id=None, nombre=producto_in.nombre, sku=producto_in.sku, descripcion=producto_in.descripcion,
                                stock=producto_in.stock or 0,
                                stock_minimo=producto_in.stock_minimo or 0 )
        
        orm_obj = producto_domain_to_orm(domain_model)
        self.db.add(orm_obj)
        self.db.commit()
        self.db.refresh(orm_obj)
        return producto_orm_to_domain(orm_obj)

    def get_all_productos(self) -> list[Producto]:
        productos = self.db.query(ProductoORM).all()
        return [producto_orm_to_domain(p) for p in productos]

    def get_producto_by_id(self, id_: int) -> Producto | None:
        producto = self.db.query(ProductoORM).filter_by(id=id_).first()
        return producto_orm_to_domain(producto) if producto else None

    def update_producto(self, id_: int, producto_upd: ProductoUpdate) -> Producto | None:
        producto = self.db.query(ProductoORM).filter_by(id=id_).first()
        if not producto:
            return None

        if producto_upd.nombre and producto_upd.nombre != producto.nombre:
            check_unicidad_producto(self.db, producto_upd.nombre, None)
            producto.nombre = producto_upd.nombre
        if producto_upd.sku and producto_upd.sku != producto.sku:
            check_unicidad_producto(self.db, None, producto_upd.sku)
            producto.sku = producto_upd.sku
        if producto_upd.descripcion is not None:
            producto.descripcion = producto_upd.descripcion
        if producto_upd.stock is not None:
            producto.stock = producto_upd.stock

        self.db.commit()
        self.db.refresh(producto)
        return producto_orm_to_domain(producto)

    def delete_producto(self, id_: int) -> bool:
        producto = self.db.query(ProductoORM).filter_by(id=id_).first()
        if not producto:
            return False
        self.db.delete(producto)
        self.db.commit()
        return True

    def get_low_stock_products(self) -> list[Producto]:
        productos = self.db.query(ProductoORM).filter(ProductoORM.stock < ProductoORM.stock_minimo).all()
        return [producto_orm_to_domain(p) for p in productos]

    def seed_productos(self):
        if self.db.query(ProductoORM).count() > 0:
            print("La base de datos ya contiene productos. Seed cancelado.")
            return

        productos_demo = [
            ProductoCreate(nombre="Hamburguesa Vegetal", sku="BIO001", descripcion="Hamburguesa hecha con proteína vegetal, aceite de girasol y especias naturales"),
            ProductoCreate(nombre="Leche de Almendra", sku="BIO002", descripcion="Bebida vegetal a base de almendras orgánicas, agua y un toque de vainilla"),
            ProductoCreate(nombre="Tofu Orgánico", sku="BIO003", descripcion="Bloque de tofu fermentado, alto en proteína, bajo en sodio"),
            ProductoCreate(nombre="Snack de Lentejas", sku="BIO004", descripcion="Crujientes snacks hechos con lentejas y especias naturales"),
            ProductoCreate(nombre="Yogur de Coco", sku="BIO005", descripcion="Yogur fermentado a base de leche de coco, sin azúcar añadida"),
            ProductoCreate(nombre="Aceite de Semilla de Chía", sku="BIO006", descripcion="Aceite prensado en frío, rico en omega 3 y antioxidantes"),
            ProductoCreate(nombre="Barrita Energética Vegana", sku="BIO007", descripcion="Barrita con avena, frutos secos y proteína vegetal"),
            ProductoCreate(nombre="Helado de Plátano y Cacao", sku="BIO008", descripcion="Helado 100% vegetal, sin lácteos, sabor natural a plátano y cacao"),
            ProductoCreate(nombre="Queso Vegano", sku="BIO009", descripcion="Queso a base de anacardos fermentados, textura cremosa"),
            ProductoCreate(nombre="Bebida Fermentada de Kombucha", sku="BIO010", descripcion="Té fermentado con probióticos naturales, sabor a frutas"),
        ]

        for p in productos_demo:
            self.create_producto(p)

        print("Productos de prueba insertados correctamente.")
