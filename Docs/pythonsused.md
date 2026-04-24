# Análisis Técnico de Proteo

Este documento describe la arquitectura interna, los módulos utilizados y la lógica de funcionamiento de `proteo.py`.

## 📦 Importaciones y su Propósito

El script utiliza exclusivamente la biblioteca estándar de Python para maximizar la compatibilidad y minimizar las dependencias externas.

| Módulo | Uso en Proteo |
| :--- | :--- |
| `json` | Procesamiento de los archivos de instrucciones que guían las acciones del agente. |
| `shutil` | Operaciones de alto nivel sobre archivos, específicamente para el sistema de backups y clonación (`copy2`). |
| `subprocess` | Ejecución de scripts externos y captura de sus flujos de salida (`stdout`, `stderr`) para el sistema de Crash Dumps. |
| `sys` | Configuración de la codificación de la consola (UTF-8) y acceso al ejecutable de Python. |
| `argparse` | Gestión de la interfaz de línea de comandos (CLI) y flags de ejecución. |
| `os` | Operaciones básicas del sistema operativo (aunque se prefiere `pathlib`). |
| `io` | Re-encapsulamiento de los flujos de salida para asegurar compatibilidad con caracteres especiales en Windows. |
| `datetime` | Generación de marcas de tiempo para los nombres de los clones evolutivos. |
| `pathlib` | Manipulación moderna y robusta de rutas de archivos (POO). |
| `typing` | Soporte para Type Hinting, mejorando la legibilidad y el mantenimiento del código. |

## ⚙️ Arquitectura Lógica

### 1. Sistema de Prompts Embebidos
El núcleo de Proteo contiene un `SYSTEM_PROMPT` que actúa como el manual de instrucciones para cualquier LLM que interactúe con el framework. Define las reglas de escape para Windows y la sintaxis del JSON.

### 2. Motor de Acciones (`ACCIONES`)
El script implementa un patrón de despacho mediante un diccionario llamado `ACCIONES`. Cada clave (`create`, `modify`, `execute`, etc.) mapea a una función específica que valida y ejecuta la operación sobre el sistema de archivos.

### 3. Ciclo de Auto-Evolución
La función `accion_clone_self` permite que el script se replique a sí mismo. Esto, combinado con `accion_execute`, permite al sistema:
1. Clonarse.
2. Modificar el clon (aplicar mejoras).
3. Ejecutar el clon.
4. Si el clon falla, el proceso padre captura el error y genera un `CRASH_DUMP_...md`.

### 4. Capa de Seguridad y Backups
- **Core Backup**: Al iniciar, el script asegura que exista una copia "inmutable" llamada `proteo_core_backup.py`.
- **Modificación Protegida**: Cada vez que se usa la acción `modify`, se genera automáticamente un archivo `.bak` de la versión anterior antes de aplicar el cambio.

### 5. Resolución de Rutas Dinámicas
Utiliza el concepto de `LAST_CLONE`. Si una operación JSON referencia a `LAST_CLONE` en su campo `path`, el motor resuelve automáticamente la ruta hacia el último archivo generado por `clone_self`, facilitando la iteración continua sin intervención humana manual.

---
**Documentación técnica para Proteo Framework**
