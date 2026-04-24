# Proteo: Reglas y Lineamientos de Evolución

Este documento establece los principios fundamentales y las directrices técnicas que deben regir cualquier implementación futura o mejora del framework Proteo.

## 🎯 Propósito del Programa
Proteo no es solo una herramienta de edición; es un **entorno de auto-evolución segura**. Su propósito es permitir que agentes de IA operen sobre código fuente local de manera quirúrgica, minimizando el riesgo de corrupción de datos y permitiendo la mejora continua del propio sistema.

---

## 🛡️ Principios de Diseño (Core Mandates)

### 1. Inmutabilidad del Núcleo
- Cualquier cambio estructural debe realizarse mediante el mecanismo de `clone_self`.
- Nunca se debe modificar directamente el script en ejecución si existe un riesgo de romper la lógica actual.
- El archivo `proteo_core_backup.py` debe permanecer intacto como última línea de defensa.

### 2. Modificación Quirúrgica
- Se prefiere el reemplazo de texto exacto (`find`/`replace`) sobre la sobreescritura total.
- Cada modificación debe ser lo más pequeña y específica posible.
- Siempre se debe generar un archivo `.bak` antes de una operación `modify`.

### 3. Retroalimentación de Fallos (Self-Healing)
- Todo error de ejecución debe ser capturado.
- El sistema debe priorizar la generación de un `CRASH_DUMP` informativo para que el agente pueda auto-corregirse en el siguiente ciclo.

---

## 🛠️ Guía para Futuras Implementaciones

### Estándares de Código
- **Dependencias Cero**: Proteo debe depender exclusivamente de la biblioteca estándar de Python para garantizar portabilidad inmediata.
- **Tipado Estricto**: Se deben usar `Type Hints` en todas las nuevas funciones para facilitar el análisis estático.
- **Codificación**: Todo manejo de archivos debe forzar `encoding='utf-8'`.

### Nuevas Acciones
Para añadir una acción al motor:
1. Crear una función `accion_nombre` que acepte `(op: dict, ruta: Path)`.
2. Registrar la función en el diccionario `ACCIONES`.
3. Documentar la nueva sintaxis en el `SYSTEM_PROMPT` embebido.

### Interfaz de Usuario
- Mantener el sistema de colores ANSI para feedback visual inmediato.
- El menú interactivo debe ser intuitivo y permitir la salida limpia del programa en cualquier punto.

---

## 🚫 Restricciones (Anti-Patterns)
- **No borrar backups**: Los archivos `.bak` son sagrados durante una sesión de evolución.
- **No rutas absolutas**: Siempre que sea posible, utilizar rutas relativas o el resolvedor `LAST_CLONE`.
- **No ejecución silenciosa**: Cada acción que afecte al sistema de archivos debe imprimir una confirmación en consola.

---
**Firmado por: Arquitectura Proteo**  
*Evolucionar sin destruir.*
