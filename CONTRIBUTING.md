# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al Sistema de Estudio de Contabilidad Financiera!

## 🌟 Cómo Contribuir

### Reportar Bugs

Si encuentras un bug:
1. Busca en los [issues existentes](https://github.com/diegobravomo/Contabilidad-Financiera/issues)
2. Si no existe, crea uno nuevo con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs actual
   - Versiones (Python, sistema operativo, etc.)
   - Logs relevantes

### Sugerir Mejoras

Para nuevas características:
1. Abre un issue describiendo:
   - El problema que resuelve
   - Cómo funcionaría
   - Por qué sería útil
2. Espera feedback antes de implementar

### Contribuir Código

1. **Fork el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/Contabilidad-Financiera.git
   ```

2. **Crear una rama**
   ```bash
   git checkout -b feature/mi-nueva-caracteristica
   # o
   git checkout -b fix/correccion-de-bug
   ```

3. **Hacer cambios**
   - Sigue el estilo de código existente
   - Añade comentarios educativos (especialmente sobre contabilidad)
   - Actualiza documentación si es necesario

4. **Probar cambios**
   ```bash
   python validate.py
   # Probar manualmente la funcionalidad
   ```

5. **Commit**
   ```bash
   git add .
   git commit -m "feat: descripción clara del cambio"
   ```

6. **Push y Pull Request**
   ```bash
   git push origin feature/mi-nueva-caracteristica
   ```
   Luego abre un Pull Request en GitHub

## 📝 Estándares de Código

### Python

- **PEP 8**: Seguir guía de estilo de Python
- **Docstrings**: Documentar todas las clases y funciones
- **Type hints**: Usar anotaciones de tipo cuando sea apropiado
- **Comentarios**: Explicar lógica compleja, especialmente conceptos contables

Ejemplo:
```python
def calculate_depreciation(
    asset_cost: float,
    useful_life: int,
    method: str = "straight-line"
) -> float:
    """
    Calcula la depreciación de un activo.
    
    Concepto Contable:
        La depreciación distribuye el costo de un activo a lo largo
        de su vida útil según el principio de asociación.
    
    Args:
        asset_cost: Costo inicial del activo
        useful_life: Vida útil en años
        method: Método de depreciación
        
    Returns:
        Depreciación anual
    """
    if method == "straight-line":
        return asset_cost / useful_life
    # ... más lógica
```

### Estructura de Commits

Usar [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva característica
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formato, sin cambio de lógica
- `refactor:` Refactorización de código
- `test:` Añadir o modificar tests
- `chore:` Cambios en build, dependencias, etc.

Ejemplos:
```
feat: añadir soporte para Excel además de PDF
fix: corregir error al procesar PDFs grandes
docs: actualizar README con nuevas instrucciones
refactor: mejorar estructura del ChatEngine
```

## 🧪 Testing

Si añades funcionalidad nueva:
1. Añade tests en `tests/`
2. Asegura que tests existentes pasen
3. Apunta a >80% de cobertura

```bash
# Ejecutar tests
pytest tests/

# Con cobertura
pytest --cov=src tests/
```

## 📚 Documentación

Actualiza documentación cuando:
- Añades nueva funcionalidad
- Cambias comportamiento existente
- Modificas API pública

Archivos a actualizar:
- `README.md` - Documentación principal
- `QUICKSTART.md` - Si afecta inicio rápido
- Docstrings en código
- Comentarios inline

## 🎓 Conceptos Educativos

Este proyecto tiene un enfoque educativo. Al contribuir:

1. **Explica conceptos contables** en comentarios
2. **Usa analogías** entre código y contabilidad
3. **Documenta el "por qué"**, no solo el "qué"
4. **Mantén legibilidad** - estudiantes leerán el código

Ejemplo:
```python
# Concepto Contable:
# El retriever busca información como un contador busca
# transacciones en registros contables: por fecha, cuenta,
# o concepto relacionado.
retriever = vector_store.as_retriever(search_kwargs={"k": 4})
```

## 🔍 Proceso de Revisión

Los Pull Requests serán revisados considerando:
- ✅ Funcionalidad correcta
- ✅ Código limpio y legible
- ✅ Documentación adecuada
- ✅ Tests (si aplica)
- ✅ Sin breaking changes (o bien justificados)
- ✅ Comentarios educativos sobre contabilidad

## 🚫 Qué NO Hacer

- ❌ Hacer commits directos a `main`
- ❌ Pull Requests demasiado grandes (dividir en menores)
- ❌ Cambios sin descripción o tests
- ❌ Código copiado sin atribución
- ❌ Romper compatibilidad sin discusión previa
- ❌ Incluir claves API o datos sensibles

## 💬 Comunicación

- **Issues**: Para bugs y sugerencias
- **Pull Requests**: Para código
- **Discussions**: Para preguntas generales

## 🎁 Reconocimiento

Todos los contribuidores serán reconocidos en:
- Comentarios de commit
- Lista de contribuidores de GitHub
- Menciones en releases

## 📄 Licencia

Al contribuir, aceptas que tu código se publique bajo la licencia MIT del proyecto.

## ❓ Preguntas

Si tienes dudas:
1. Revisa [README.md](README.md)
2. Busca en issues/discussions existentes
3. Crea una nueva discussion
4. Contacta a los mantenedores

---

**¡Gracias por ayudar a mejorar la educación en contabilidad! 🎓**
