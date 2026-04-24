import json
import shutil
import subprocess
import sys
import argparse
import os
import io
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

class Color:
    VERDE = '\\033[92m'
    AMARILLO = '\\033[93m'
    ROJO = '\\033[91m'
    CYAN = '\\033[96m'
    MAGENTA = '\\033[95m'
    RESET = '\\033[0m'

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ==========================================
# 1. PROMPTS EMBEBIDOS (Constantes)
# ==========================================

SYSTEM_PROMPT = """# 🤖 MANUAL DE USUARIO PARA AGENTE CÓDER (PROTEO)

Eres un agente de IA operando "Proteo", un framework de manipulación y auto-evolución de código local. 
Tu única forma de interactuar es generar un archivo JSON con operaciones.

## ⚠️ REGLAS ESTRICTAS PARA EL JSON
1. ESCAPE: En Windows, escapa doblemente barras invertidas (`C:\\\\ruta`) o usa barras normales (`C:/ruta`).
2. SALTOS DE LÍNEA: El código en campos `content`, `find` o `replace` debe tener los saltos codificados como `\\n`.
3. INDENTACIÓN: La acción `modify` busca texto EXACTO y LITERAL. Incluye espacios de indentación correctos en `"find"`.

## 🛠️ ACCIONES DE ARCHIVOS
- `create`: Crea un archivo. Requiere `path` y `content`.
- `append`: Agrega texto al final. Requiere `path` y `content`.
- `modify`: Reemplaza texto exacto. Requiere `path`, `find` y `replace`. (Genera un .bak automático).
- `delete_partial`: Elimina texto exacto. Requiere `path` y `find`.
- `delete_full`: Borra el archivo entero. Requiere `path`.\n- `read`: Lee y muestra el contenido de un archivo. Requiere `path`.

## 🧬 SISTEMA DE AUTO-EVOLUCIÓN (CLONACIÓN)
Puedes mejorar el código de Proteo iterativamente sin romper el núcleo original:
1. Usa la acción `"clone_self"`. No requiere `path`. El sistema generará automáticamente un clon con la fecha y hora (Ej: `proteo20260424083000.py`).
2. Usa `"modify"` para aplicar tus mejoras. ¿Cómo sabes el nombre del clon? No lo sabes. Usa `"path": "LAST_CLONE"`.
3. Usa `"execute"` pasando `"path": "LAST_CLONE"` para arrancar la nueva versión.

Si tu nueva versión falla, Proteo capturará el error de la terminal y generará un `CRASH_DUMP_...md`. Úsalo para reparar el error en tu siguiente ciclo.
"""

CRASH_DUMP_TEMPLATE = """# 🚨 REPARACIÓN REQUERIDA (CRASH DUMP)

Eres un Agent Coder. Has intentado ejecutar la versión evolucionada `{nombre_script}` y ha fallado.
Analiza el error y emite un nuevo JSON para corregir el código defectuoso.

## 🛑 TRACEBACK DEL ERROR:
```python
{error_trace}

🛠️ INSTRUCCIONES DE REPARACIÓN:

    Lee el Traceback. Localiza la línea exacta del fallo (SyntaxError, IndentationError, etc).

    Genera una acción modify para {nombre_script} aplicando la corrección.

    Si el archivo es irrecuperable, borralo y vuelve a clonar desde el inicio.
    """

# ==========================================
# 2. SISTEMAS DE SEGURIDAD
# ==========================================

LAST_CLONED_PATH: Path | None = None
DRY_RUN: bool = False

def asegurar_core_backup() -> None:
    core_path = Path("proteo_core_backup.py")
    script_actual = Path(__file__).resolve()
    if not core_path.exists() and script_actual.name != "proteo_core_backup.py":
        shutil.copy2(script_actual, core_path)
        print(f"[SISTEMA] Backup core inmutable creado en: {core_path}")

def crear_backup(ruta: Path) -> None:
    if ruta.exists():
        backup_path = ruta.with_suffix(ruta.suffix + '.bak')
        shutil.copy2(ruta, backup_path)
        print(f"[BACKUP] Creado {backup_path}")

def generar_crash_dump(ruta_script: Path, error_trace: str) -> None:
    dump_path = Path(f"CRASH_DUMP_{ruta_script.stem}.md")
    contenido = CRASH_DUMP_TEMPLATE.format(
        nombre_script=ruta_script.name,
        error_trace=error_trace.strip()
    )
    dump_path.write_text(contenido, encoding='utf-8')
    print(f"[CRÍTICO] Fallo en {ruta_script.name}. Dump de reparación: {dump_path}")

def resolver_ruta(ruta_str: str) -> Path | None:
    if ruta_str == "LAST_CLONE":
        if not LAST_CLONED_PATH:
            print("[ERROR] Se invocó 'LAST_CLONE' pero no se ha clonado nada en esta sesión.")
            return None
        return LAST_CLONED_PATH
    return Path(ruta_str)

# ==========================================
# 3. MOTOR DE ACCIONES
# ==========================================

def accion_create(op: dict[str, Any], ruta: Path) -> None:
    if DRY_RUN:
        print(f"{Color.MAGENTA}[DRY-RUN]{Color.RESET} Crearía archivo: {ruta}")
        return
    ruta.write_text(op.get('content', ''), encoding='utf-8')
    print(f"{Color.VERDE}[CREADO]{Color.RESET} {ruta}")

def accion_append(op: dict[str, Any], ruta: Path) -> None:
    with ruta.open('a', encoding='utf-8') as f:
        f.write(op.get('content', ''))
    print(f"[AGREGADO] Texto al final de {ruta}")

def accion_modify(op: dict[str, Any], ruta: Path) -> None:
    buscar = op.get('find', '')
    reemplazar = op.get('replace', '')
    if not buscar:
        return
    if DRY_RUN:
        print(f"{Color.MAGENTA}[DRY-RUN]{Color.RESET} Modificaría: {ruta}")
        return
    crear_backup(ruta)
    texto = ruta.read_text(encoding='utf-8')
    if buscar in texto:
        ruta.write_text(texto.replace(buscar, reemplazar), encoding='utf-8')
        print(f"{Color.VERDE}[MODIFICADO]{Color.RESET} {ruta}")
    else:
        print(f"{Color.AMARILLO}[AVISO]{Color.RESET} Texto a modificar no encontrado en {ruta}")

def accion_delete_partial(op: dict[str, Any], ruta: Path) -> None:
    accion_modify({'find': op.get('find', ''), 'replace': ''}, ruta)

def accion_delete_full(op: dict[str, Any], ruta: Path) -> None:
    if ruta.exists():
        ruta.unlink()
        print(f"{Color.ROJO}[ELIMINADO]{Color.RESET} {ruta}")

def limpiar_repositorio() -> None:
    """Mantiene solo los 3 últimos proteos en raíz y archiva el resto."""
    archivo_dir = Path("archive")
    if not DRY_RUN: archivo_dir.mkdir(exist_ok=True)
    
    proteos = sorted(list(Path(".").glob("proteo20[0-9]*.py")), key=os.path.getmtime, reverse=True)
    if len(proteos) > 3:
        para_archivar = proteos[3:]
        for p in para_archivar:
            if DRY_RUN:
                print(f"{Color.MAGENTA}[DRY-RUN]{Color.RESET} Archivaría: {p.name}")
                continue
            shutil.move(str(p), str(archivo_dir / p.name))
            print(f"{Color.AMARILLO}[LIMPIEZA]{Color.RESET} Movido a /archive: {p.name}")

    # Limpieza de /archive (Máx 50)
    historial = sorted(list(archivo_dir.glob("proteo*.py")), key=os.path.getmtime)
    while len(historial) > 50:
        viejo = historial.pop(0)
        if DRY_RUN:
            print(f"{Color.MAGENTA}[DRY-RUN]{Color.RESET} Borraría histórico: {viejo.name}")
            continue
        viejo.unlink()
        print(f"{Color.ROJO}[LIMPIEZA]{Color.RESET} Eliminado por antigüedad: {viejo.name}")

def accion_search(op: dict[str, Any], ruta: Path) -> None:
    import re
    pattern = op.get('pattern', '')
    if not pattern or not ruta.exists(): return
    texto = ruta.read_text(encoding='utf-8')
    matches = list(re.finditer(pattern, texto))
    print(f"\n{Color.CYAN}--- BÚSQUEDA EN {ruta.name} (Patrón: {pattern}) ---{Color.RESET}")
    for m in matches:
        linea = texto.count('\\n', 0, m.start()) + 1
        print(f" L{linea}: {m.group().strip()}")
    print(f"{Color.CYAN}--- TOTAL: {len(matches)} coincidencias ---{Color.RESET}\n")

def accion_read(op: dict[str, Any], ruta: Path) -> None:
    if ruta.exists():
        contenido = ruta.read_text(encoding='utf-8')
        print(f"\n{Color.CYAN}--- CONTENIDO DE {ruta.name} ---{Color.RESET}")
        print(contenido)
        print(f"{Color.CYAN}---------------------------------{Color.RESET}\n")
    else:
        print(f"{Color.ROJO}[ERROR]{Color.RESET} No se puede leer, no existe: {ruta}")

def accion_clone_self(op: dict[str, Any], ruta_dummy: Path) -> None:
    global LAST_CLONED_PATH
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ruta_destino = Path(f"proteo{timestamp}.py")
    script_actual = Path(__file__).resolve()
    shutil.copy2(script_actual, ruta_destino)
    LAST_CLONED_PATH = ruta_destino
    print(f"[CLON] Proteo auto-evolucionado hacia: {ruta_destino}")

def accion_execute(op: dict[str, Any], ruta: Path) -> None:
    if not ruta.exists():
        print(f"[ERROR] No se puede ejecutar, no existe: {ruta}")
        return

    print(f"[EJECUTANDO] Iniciando {ruta.name}...")
    try:
        args = op.get('argumento', '')
        cmd = [sys.executable, str(ruta)]
        if args:
            cmd.append(args)
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if resultado.returncode != 0:
            generar_crash_dump(ruta, resultado.stderr)
            # Auto-Rollback if .bak exists
            bak = ruta.with_suffix(ruta.suffix + '.bak')
            if bak.exists():
                shutil.copy2(bak, ruta)
                print(f"{Color.ROJO}[ROLLBACK]{Color.RESET} Restaurado {ruta.name} desde backup debido a fallo.")
        else:
            print(f"[ÉXITO] {ruta.name} finalizó correctamente.")
            if resultado.stdout:
                print("--- SALIDA ---")
                print(resultado.stdout.strip())
                print("--------------")
    except subprocess.TimeoutExpired:
        generar_crash_dump(ruta, "TimeoutExpired: El script tardó más de 30 segundos.")
    except Exception as e:
        generar_crash_dump(ruta, str(e))

ACCIONES: dict[str, Callable[[dict[str, Any], Path], None]] = {
    'create': accion_create,
    'append': accion_append,
    'modify': accion_modify,
    'delete_partial': accion_delete_partial,
    'delete_full': accion_delete_full,
    'read': accion_read,
    'search': accion_search,
    'clone_self': accion_clone_self,
    'execute': accion_execute
}

# ==========================================
# 4. CLI Y ORQUESTACIÓN
# ==========================================

def exportar_prompts() -> None:
    print("="*50)
    print("SYSTEM PROMPT:")
    print("="*50)
    print(SYSTEM_PROMPT)
    archivo_export = Path("LLM_SYSTEM_PROMPT.txt")
    archivo_export.write_text(SYSTEM_PROMPT, encoding='utf-8')
    print(f"\n[SISTEMA] Prompts exportados a {archivo_export}")

def procesar_json(json_path_str: str) -> None:
    json_path = Path(json_path_str)
    if not json_path.exists():
        print(f"[ERROR] No se encontró el archivo JSON: {json_path}")
        return

    try:
        data = json.loads(json_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON inválido: {e}")
        return

    asegurar_core_backup()
    limpiar_repositorio()

    for op in data.get('operations', []):
        accion = op.get('action')
        ruta_raw = op.get('path', '')
        
        if accion not in ACCIONES:
            print(f"[AVISO] Saltando acción no reconocida: '{accion}'")
            continue

        ruta = resolver_ruta(ruta_raw) if ruta_raw else Path(".")
        
        # clone_self no depende de ruta válida de entrada
        if not ruta and accion != 'clone_self': 
            continue

        try:
            ACCIONES[accion](op, ruta)  # type: ignore
        except PermissionError:
            print(f"[ERROR] Permiso denegado en: {ruta}")
        except Exception as e:
            print(f"[ERROR INESPERADO] {ruta}: {e}")

def mostrar_menu_json() -> str | None:
    json_files = list(Path(".").glob("*.json"))
    json_files = [f for f in json_files if f.name != "proteo_core_backup.py"]
    
    if not json_files:
        print("[AVISO] No se encontraron archivos JSON en la raíz.")
        return None
    
    print("\n--- ARCHIVOS JSON DISPONIBLES ---")
    for i, f in enumerate(json_files, 1):
        print(f"  {i}. {f.name}")
    print("--------------------------------\n")
    
    while True:
        try:
            opcion = input("Selecciona el número del JSON (0 para cancelar): ").strip()
            opcion = int(opcion)
            if opcion == 0:
                return None
            if 1 <= opcion <= len(json_files):
                return str(json_files[opcion - 1])
            print("[ERROR] Número inválido. Intenta de nuevo.")
        except ValueError:
            print("[ERROR] Debes ingresar un número.")

def menu_interactivo() -> None:
    try:
        entrada = input(" presiona Enter para continuar...")
    except (EOFError, KeyboardInterrupt):
        print("\n[AVISO] Ejecución no interactiva detectada. Usa --help para ver opciones.")
        return
    
    while True:
        print("\n" + "="*40)
        print("        PROTEO - Menú Principal")
        print("="*40)
        print("  1. Exportar Prompts (System Prompt)")
        print("  2. Ejecutar Archivo JSON")
        print("  3. Salir")
        print("="*40)
        
        try:
            opcion = input("\nElige una opción (1-3): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n¡Hasta luego!")
            break
        
        if opcion == "1":
            print()
            exportar_prompts()
        elif opcion == "2":
            json_path = mostrar_menu_json()
            if json_path:
                print()
                procesar_json(json_path)
        elif opcion == "3":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n[ERROR] Opción inválida. Elige 1, 2 o 3.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Proteo: Framework de Auto-Evolución y Manipulación de Archivos")
    parser.add_argument("--export-prompts", action="store_true", help="Exporta el System Prompt para el LLM y lo muestra en consola.")
    parser.add_argument("--execute-json", type=str, metavar="JSON_PATH", help="Ruta al archivo JSON a procesar.")
    parser.add_argument("--dry-run", action="store_true", help="Simula las acciones sin modificar archivos.")

    args = parser.parse_args()
    
    if args.dry_run:
        DRY_RUN = True
        print(f"{Color.MAGENTA}[MODO DRY-RUN ACTIVADO]{Color.RESET}")

    if args.export_prompts:
        exportar_prompts()
    elif args.execute_json:
        procesar_json(args.execute_json)
    else:
        menu_interactivo()