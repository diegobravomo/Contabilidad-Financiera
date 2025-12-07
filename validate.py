"""
Script de Validación del Sistema

Este script verifica que todos los componentes estén correctamente instalados
y configurados antes de usar la aplicación.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Verifica la versión de Python."""
    print("Verificando versión de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Se requiere 3.8+)")
        return False

def check_dependencies():
    """Verifica que las dependencias estén instaladas."""
    print("\nVerificando dependencias...")
    required = [
        'langchain',
        'chromadb',
        'streamlit',
        'pandas',
        'openai',
        'dotenv',
        'pypdf'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (faltante)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️ Dependencias faltantes: {', '.join(missing)}")
        print("Ejecuta: pip install -r requirements.txt")
        return False
    return True

def check_environment():
    """Verifica variables de entorno."""
    print("\nVerificando configuración...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️ Archivo .env no encontrado")
        print("  Crea uno basado en .env.example")
        return False
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY no configurada en .env")
        return False
    elif api_key == "tu-clave-de-api-aqui":
        print("✗ OPENAI_API_KEY no ha sido actualizada (valor por defecto)")
        return False
    else:
        print(f"✓ OPENAI_API_KEY configurada ({api_key[:8]}...)")
        return True

def check_structure():
    """Verifica la estructura de directorios."""
    print("\nVerificando estructura de directorios...")
    required_dirs = ['src', 'config', 'data', 'tests']
    
    all_ok = True
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✓ {dir_name}/")
        else:
            print(f"✗ {dir_name}/ (faltante)")
            all_ok = False
    
    return all_ok

def check_modules():
    """Verifica que los módulos propios se puedan importar."""
    print("\nVerificando módulos del sistema...")
    
    try:
        from src import (
            DocumentProcessor,
            VectorStore,
            ChatEngine,
            SummaryGenerator,
            QuizGenerator
        )
        print("✓ Todos los módulos se importan correctamente")
        return True
    except ImportError as e:
        print(f"✗ Error al importar módulos: {e}")
        return False

def check_data_directory():
    """Verifica que haya PDFs en el directorio data."""
    print("\nVerificando documentos...")
    data_dir = Path("data")
    
    if not data_dir.exists():
        print("✗ Directorio data/ no existe")
        return False
    
    pdf_files = list(data_dir.glob("**/*.pdf"))
    if pdf_files:
        print(f"✓ {len(pdf_files)} archivo(s) PDF encontrado(s)")
        for pdf in pdf_files[:5]:  # Mostrar máximo 5
            print(f"  • {pdf.name}")
        if len(pdf_files) > 5:
            print(f"  ... y {len(pdf_files) - 5} más")
        return True
    else:
        print("⚠️ No se encontraron archivos PDF en data/")
        print("  Coloca tus documentos en data/ antes de ejecutar ingest.py")
        return False

def main():
    """Función principal."""
    print("="*60)
    print("VALIDACIÓN DEL SISTEMA DE ESTUDIO DE CONTABILIDAD")
    print("="*60)
    
    checks = {
        "Python": check_python_version(),
        "Dependencias": check_dependencies(),
        "Estructura": check_structure(),
        "Módulos": check_modules(),
        "Variables de entorno": check_environment(),
        "Documentos": check_data_directory()
    }
    
    print("\n" + "="*60)
    print("RESUMEN DE VALIDACIÓN")
    print("="*60)
    
    for name, result in checks.items():
        status = "✓ OK" if result else "✗ FALLO"
        print(f"{name:.<40} {status}")
    
    print("="*60)
    
    all_passed = all(checks.values())
    
    if all_passed:
        print("\n✓ TODAS LAS VERIFICACIONES PASARON")
        print("\nPróximos pasos:")
        print("1. Si no has procesado documentos: python ingest.py")
        print("2. Para iniciar la aplicación: streamlit run app.py")
        return 0
    else:
        print("\n✗ ALGUNAS VERIFICACIONES FALLARON")
        print("\nRevisa los mensajes arriba y corrige los problemas.")
        
        # Verificar casos críticos
        if not checks["Dependencias"]:
            print("\nAcción requerida:")
            print("  pip install -r requirements.txt")
        
        if not checks["Variables de entorno"]:
            print("\nAcción requerida:")
            print("  1. Copia .env.example a .env")
            print("  2. Edita .env y añade tu OPENAI_API_KEY")
        
        if not checks["Documentos"]:
            print("\nAcción sugerida:")
            print("  Coloca archivos PDF en la carpeta data/")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
