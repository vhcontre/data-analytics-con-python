@echo off
REM ===============================
REM Setup Python environment & run dataset script
REM ===============================

REM Crear entorno virtual
py -3.11 -m venv .venv

REM Activar entorno virtual
call .venv\Scripts\activate.bat

REM Actualizar pip
python.exe -m pip install --upgrade pip

REM Instalar dependencias
pip install -r requirements.txt

REM Verificar instalación de librerías
python -c "import numpy, pandas; print('OK', numpy.__version__, pandas.__version__)"

REM Ejecutar script para generar dataset de productos
@REM python -m app.scripts.create_product_dataset
@REM python -m app.scripts.check_dataset_integrity

pause
