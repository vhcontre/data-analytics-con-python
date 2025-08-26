# 📦 CHANGELOG

Todas las versiones y mejoras del sistema de inventario.
---

## [v0.10.0] - 2025-06-27

## ⚙️ Dockerización del proyecto

### ✅ Backend dockerizado
- Se creó un `Dockerfile` para la aplicación FastAPI.
- La imagen construye el entorno virtual, instala dependencias y expone el servicio en el puerto 8000.
- Se utiliza `uvicorn` como servidor ASGI para producción.

### ✅ Base de datos PostgreSQL integrada con Docker
- Se incorporó una instancia de PostgreSQL mediante `docker-compose.yml`.
- Las variables de entorno y credenciales se gestionan con un archivo `.env`.
- El servicio de base de datos expone el puerto 5432, accesible por la app backend.

### ✅ Docker Compose para orquestación
- Se creó un archivo `docker-compose.yml` que levanta:
  - Backend (FastAPI)
  - Base de datos PostgreSQL
- Los servicios están conectados por una red interna `backend-network`.
- Se agregó volumen persistente para los datos de PostgreSQL.

## 📁 Archivos nuevos

- `Dockerfile`: Imagen del backend
- `docker-compose.yml`: Orquestación de servicios
- `.env`: Variables sensibles (usuario/contraseña DB, host, puerto, etc.)
- `.dockerignore`: Evita copiar archivos innecesarios al build (por ejemplo, `venv`, `__pycache__`, etc.)

## 🧪 Verificaciones realizadas

- Se ejecutó `docker-compose up` y la aplicación fue accesible en `http://localhost:8000`.
- Se probó el acceso a la base de datos con los datos montados.
- Se verificó que las rutas web `/web/productos`, `/web/movimientos`, y el alta de datos funcionan correctamente bajo contenedores.

---

📅 **Fecha de cierre**: Semana 10  
🧪 **Ambiente validado**: Docker + PostgreSQL  
🚀 **Ejecución final**: `docker-compose up --build`  
🌍 **App disponible en**: [http://localhost:8000](http://localhost:8000)



---
## [v0.9.0] - 2025-06-27

## ✨ Nuevas funcionalidades

- **Reporte de productos con stock bajo**  
  Se agregó una vista HTML que lista todos los productos cuyo stock actual es inferior al stock mínimo.  
  Ruta: `/web/alerta-stock`

- **Vista de movimientos recientes**  
  Se implementó una ruta que muestra los 10 movimientos más recientes del sistema, ordenados por fecha.  
  Ruta: `/web/movimientos-recientes`

- **Exportación de movimientos en CSV**  
  Se desarrolló un endpoint que permite descargar los movimientos como archivo CSV.  
  Ruta: `/web/movimientos/exportar-csv`

## 🌐 Navegación entre vistas

- Se mejoró la interfaz web incluyendo enlaces visibles para navegar entre:
  - Productos
  - Movimientos
  - Registrar nuevo movimiento
  - Ver alertas de stock
  - Descargar CSV

## 🌿 Flujo Git

- Se trabajó en la rama `semana-9` con el siguiente flujo:
  - Issues creados y asignados a un *milestone*
  - Commits con referencia al issue (`fixes #xx`)
  - Pull request con integración validada por GitHub Actions
  - Fusión al `main` luego de aprobar PR

## 🧪 Pruebas

- Se mantuvo compatibilidad con las pruebas existentes.
- Se verificó que los módulos nuevos no rompan el flujo de carga o lectura de datos.
- Se reintentaron ejecuciones de GitHub Actions tras correcciones en la rama de trabajo.

---

📅 **Fecha de cierre**: Semana 9  
🔁 **Rama de desarrollo**: `semana-9`  
📥 **Pull Request integrado**: ✔️

---

## [v0.8.0] - 2025-06-25

### Nuevas funcionalidades
- Implementación del formulario web para registrar movimientos (ingreso, egreso, traslado).
- Integración de formulario con backend FastAPI para crear movimientos y actualizar stock.
- Validaciones en backend para controlar existencia de producto, stock suficiente y campos obligatorios.
- Manejo de errores en la interfaz web para mostrar mensajes sin perder datos ingresados.
- Redirección automática tras registro exitoso hacia el listado de productos.
- Uso de plantillas Jinja2 para la presentación de formularios y mensajes de error.
- Mejora en la experiencia de usuario con persistencia de datos en formularios al fallar validaciones.

### Correcciones y mejoras
- Ajustes en el repositorio `MovimientoRepository` para lógica completa de alta con control de stock.
- Eliminación de recarga total de formulario en caso de error, mostrando feedback claro.
- Estructura del proyecto mantenida con rutas organizadas y dependencias correctamente gestionadas.

### Pendientes para próximas semanas
- Ampliar interfaz web con listados dinámicos de movimientos.
- Incorporar paginación y filtros en listados.
- Mejorar diseño UI/UX con CSS o frameworks frontend.

## [v0.7.0] - 2025-06-25

## 🎯 Objetivos alcanzados

- 🌐 Integración de Jinja2 como motor de plantillas web en FastAPI
- 📄 Creación de vistas HTML para mostrar productos
- 🧱 Uso de base.html como plantilla base para layout común
- 🧭 Navegación web básica entre secciones
- 📊 Visualización dinámica del stock de productos desde base de datos

---

## 📁 Estructura y cambios clave

- `app/main.py`: se agregó soporte para plantillas (`Jinja2Templates`)
- `app/routers/web_interface.py`: nuevas rutas tipo `GET /web/...`
- `app/templates/base.html`: plantilla base reutilizable
- `app/templates/productos.html`: tabla con productos usando Jinja2
- `app/static/`: carpeta creada para incluir archivos CSS en el futuro
- `requirements.txt`: se agregó `python-multipart` como dependencia requerida

---

## ✅ Pruebas realizadas

- Navegación por `/web/productos` desde el navegador
- Renderización de tabla con datos reales desde base de datos
- Verificación de diseño base y navegación
- Tests funcionales pasando localmente (`pytest`)
- GitHub Actions corregido tras agregar dependencias

---

## [v0.6.0] - 2025-06-20

🔒 Versión estable al cierre de **Semana 6**

### 🆕 Features
- Autenticación con JWT (login de usuarios)
- Middleware de autorización por roles (admin / operador)
- Endpoints protegidos según permisos

### 📦 Backend
- CRUD de productos, depósitos y movimientos
- Reglas de negocio de stock mínimo y trazabilidad

### 📄 Documentación
- Swagger generado automáticamente (`/docs` y `/redoc`)
- Esquemas Pydantic actualizados

### ✅ Tests
- Test unitarios para modelos, esquemas y repositorios
- Test de integración completo (login → crear producto → entrada → salida)
- Cobertura de seguridad con roles

### 🔧 DevOps
- Configuración de **GitHub Actions**
  - Ejecución automática de `pytest`
  - Linter Python (`ruff`)
  - Corrección de problemas en pipelines

---

## [v0.5.0] - 2025-06-13

✔️ Semana 5: Inicio de autenticación, creación de modelos `Usuario` y `Rol`.

## [v0.4.0] - 2025-06-06

✔️ Semana 4: Entrada y salida de stock, validación y trazabilidad de movimientos.

## [v0.3.0] - 2025-05-30

✔️ Semana 3: Validación y listados con paginación desde consola.

## [v0.2.0] - 2025-05-24

✔️ Semana 2: Creación de base de datos, modelos iniciales y arquitectura de capas.

## [v0.1.0] - 2025-05-17

🔧 Semana 1: Análisis, diseño del sistema y control de versiones inicial.
