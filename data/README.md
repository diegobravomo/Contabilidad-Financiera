# 📁 Carpeta de Datos

Esta carpeta es donde debes colocar tus documentos PDF de contabilidad financiera para que sean procesados por el sistema.

## 📚 Tipos de Documentos Recomendados

- **NIIF** (Normas Internacionales de Información Financiera)
- **NIC** (Normas Internacionales de Contabilidad)
- **Libros de texto** de contabilidad financiera
- **Apuntes de clase** sobre contabilidad
- **Guías de estudio**
- **Casos prácticos**
- **Material de referencia contable**

## 📝 Instrucciones

1. **Coloca tus PDFs aquí**: Simplemente copia los archivos PDF a esta carpeta
2. **Organización opcional**: Puedes crear subdirectorios si lo deseas (ej: `niif/`, `libros/`, `apuntes/`)
3. **Ejecuta la ingesta**: Corre `python ingest.py` desde la raíz del proyecto
4. **Espera el procesamiento**: El sistema procesará todos los PDFs automáticamente

## 🎯 Ejemplo de Estructura

```
data/
├── niif/
│   ├── NIIF_9_Instrumentos_Financieros.pdf
│   ├── NIIF_15_Ingresos.pdf
│   └── NIC_16_Propiedades_Planta_Equipo.pdf
├── libros/
│   ├── Contabilidad_Basica.pdf
│   └── Estados_Financieros_Avanzados.pdf
└── apuntes/
    ├── Clase_01_Introduccion.pdf
    └── Clase_02_Activos.pdf
```

## ⚠️ Notas Importantes

- **Formato**: Solo PDFs son soportados actualmente
- **Tamaño**: No hay límite estricto, pero PDFs muy grandes tardarán más en procesarse
- **Calidad**: Asegúrate de que los PDFs tengan texto extraíble (no solo imágenes)
- **Idioma**: El sistema funciona mejor con documentos en español
- **Copyright**: Asegúrate de tener los derechos para usar los documentos

## 🔄 Re-procesamiento

Si añades nuevos documentos:
1. Colócalos en esta carpeta
2. Ejecuta `python ingest.py` nuevamente
3. Los nuevos documentos se añadirán a la base de datos existente

Para recrear completamente la base de datos:
```bash
python ingest.py --force-recreate
```

## 📊 Rendimiento

- **Documentos pequeños** (< 50 páginas): ~1-2 minutos
- **Documentos medianos** (50-200 páginas): ~3-10 minutos
- **Documentos grandes** (> 200 páginas): ~10-30 minutos

El tiempo depende de:
- Tamaño del documento
- Velocidad de la API de OpenAI
- Conexión a internet

## 🚫 Archivos .gitignore

Por defecto, los PDFs en esta carpeta **NO** se suben a Git para:
- Respetar derechos de autor
- Mantener el repositorio ligero
- Proteger material privado

Si quieres versionar algunos PDFs específicos, modifica el `.gitignore`.
