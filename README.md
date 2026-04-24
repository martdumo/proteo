![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![License](https://img.shields.io/badge/License-Proprietary-gray)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue)

# Proteo Framework

**Proteo** is a sophisticated local code manipulation and auto-evolution framework designed to empower AI agents with the ability to interact with and improve their own source code and surrounding project structures. By utilizing a structured JSON-based instruction set, Proteo bridges the gap between high-level logic and low-level file system operations.

## 🚀 Key Features

- **JSON-Driven Engine**: Execute complex file operations through a standardized JSON schema.
- **Auto-Evolution (Cloning)**: Features a unique self-cloning mechanism that allows the system to evolve safely by creating timestamped versions of itself.
- **Self-Healing Loop**: Automatically captures execution failures and generates detailed `CRASH_DUMP` reports in Markdown format for immediate debugging and repair.
- **Robust File Management**: Supports `create`, `append`, `modify` (with exact text matching), and deletion operations.
- **Safety First**: Implements an immutable core backup system and automatic `.bak` generation for modified files.
- **Cross-Interface Support**: Features both a rich interactive CLI menu and a command-line interface for automated workflows.

## 🛠️ Core Operations

The framework operates on a set of atomic actions defined in a JSON file:

- **`create`**: Instantiates new files with specific content.
- **`modify`**: Performs surgical, exact-match text replacements.
- **`append`**: Adds content to the end of existing files.
- **`clone_self`**: Creates a new evolutionary branch of the Proteo core.
- **`execute`**: Runs scripts and monitors for errors, feeding failures back into the repair loop.

## 📋 Requirements

- **Python 3.11+**
- **Windows 10/11** (Optimized for Windows file paths and terminal encoding)

## 📖 Usage

### Interactive Mode
Simply run the script to enter the interactive menu:
```bash
python proteo.py
```

### Command Line
Export the System Prompt for LLM integration:
```bash
python proteo.py --export-prompts
```

Execute a specific instruction set:
```bash
python proteo.py --execute-json instructions.json
```

---

**Created by Martin Dumont (martdumo)**  
*Todos los derechos reservados.*
