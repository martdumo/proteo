![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![License](https://img.shields.io/badge/License-Proprietary-gray)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue)

# Proteo Framework v1.3

**Proteo** is a sophisticated local code manipulation and auto-evolution framework designed for Windows 11 and PowerShell. It empowers AI agents to interact with, improve, and evolve their own source code through a secure, surgical, and self-healing JSON-driven engine.

## 🚀 Key Features

- **Auto-Evolution (Cloning)**: Safely improves its own core through timestamped versioning.
- **Safety First**: Includes a **Dry-Run mode** for simulations, automatic **Syntax Validation** (via `ast`), and **Auto-Rollback** on execution failure.
- **Self-Healing Loop**: Generates detailed `CRASH_DUMP` reports for automatic bug repair.
- **Repo Hygiene**: Automated garbage collection that keeps only the 3 most recent clones in the root and archives up to 50 older versions in `/archive`.
- **Git Integration**: Automatically commits successful evolutionary cycles to maintain a perfect project history.
- **Visual Feedback**: Rich ANSI color-coded terminal output for instant status recognition.

## 🛠️ Core Operations (JSON Engine)

- **`create` / `modify`**: Surgical file operations with built-in Python syntax checking.
- **`rename`**: Native file relocation and renaming.
- **`read` / `search`**: Advanced inspection tools (supports Regex search).
- **`execute`**: Run scripts with monitored output and automatic recovery.
- **`clone_self`**: Generate the next evolutionary branch of the framework.

## 📋 Requirements

- **Python 3.11+**
- **Windows 11 & PowerShell** (Optimized for CRLF and UTF-8 encoding)

## 📖 Usage

### Simulation (Recommended)
```powershell
python .\proteo_actual.py --dry-run --execute-json .\instructions.json
```

### Direct Evolution
```powershell
python .\proteo_actual.py --execute-json .\instructions.json
```

---

**Created by Martin Dumont (martdumo)**  
*Todos los derechos reservados.*
