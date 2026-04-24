# Proteo: Reglas y Lineamientos de Evolución (v1.2)

## 🎯 Propósito del Programa
Proteo es un framework de **auto-evolución segura**. Permite a agentes de IA manipular código local mediante un motor de acciones JSON, garantizando la integridad del sistema mediante clonación y backups automáticos.

---

## 💻 Entorno de Ejecución
Este programa está diseñado para ejecutarse en **Windows 11** utilizando **PowerShell**. 

### Comandos de Referencia
- **Ejecución Directa**: `python .\proteo_actual.py`
- **Con JSON**: `python .\proteo_actual.py --execute-json .\instrucciones.json`
- **Simulación**: `python .\proteo_actual.py --dry-run --execute-json .\instrucciones.json`
- **Listar archivos**: `ls`, `dir` o `Get-ChildItem`

---

## 🛡️ Principios de Diseño (Core Mandates)

1.  **Inmutabilidad**: Los cambios estructurales requieren `clone_self`. El archivo `proteo_core_backup.py` es intocable.
2.  **Surgical Edit**: Se prefiere `modify` (exact match) con generación automática de `.bak`.
3.  **Self-Healing**: Captura de errores y generación de `CRASH_DUMP` para reparación automática.
4.  **Auto-Rollback**: Si un script ejecutado falla, el sistema restaura el backup `.bak` automáticamente.

---

## 🛠️ Guía de Implementación y Testeo

### Cómo Probar Nuevas Funcionalidades
1.  **Dry Run First**: Siempre validar nuevos JSON con el flag `--dry-run`.
    ```bash
    python proteo_actual.py --dry-run --execute-json test.json
    ```
2.  **Validación de Salida**: Verificar que los colores ANSI coincidan con el estado esperado (Verde=Éxito, Rojo=Error, Magenta=DryRun).
3.  **Test de Rollback**: Forzar un error de sintaxis en un script y verificar que la versión anterior sea restaurada automáticamente.

---

## 🧹 Repo Hygiene (Mantenimiento de Orden)

Para evitar el desorden (clutter), Proteo implementa un recolector de basura automático en cada ejecución:

- **Raíz (Root)**: Solo se mantienen los **3 clones más recientes**.
- **Archivo (`/archive`)**:
    - Todos los clones antiguos se mueven aquí automáticamente.
    - Capacidad máxima: **50 archivos**.
    - Política **FIFO**: Al llegar a 51, se borra el más antiguo.
- **Backups**: Los archivos `.bak` deben limpiarse manualmente una vez confirmada la estabilidad de la versión.

---

## 🚀 Próximas Mejoras (Roadmap)

1.  **Integración Git**: Autocommit al finalizar exitosamente un ciclo de evolución.
2.  **Fuzzy Search**: Mejorar la acción `search` para soportar búsquedas aproximadas.
3.  **Web Interface**: Un panel simple en Flask/FastAPI para monitorear las evoluciones gráficamente.
4.  **Sandbox de Ejecución**: Ejecutar los scripts en un entorno aislado para mayor seguridad.

---
**Firmado por: Arquitectura Proteo**  
*Evolucionar sin destruir.*
