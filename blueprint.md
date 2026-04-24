# Blueprint: Proteo Evolutionary Framework

## Architecture Overview
Proteo is designed as a self-modifying engine that abstracts file system operations into a JSON-based protocol. This allows AI agents to operate within a controlled environment while maintaining the ability to improve the environment itself.

### Core Components
1.  **Instruction Engine**: Parses JSON operations (`create`, `modify`, `append`, `delete`, `read`, `clone_self`, `execute`).
2.  **Surgical Modifier**: Uses exact string matching to apply changes to source code, ensuring high precision.
3.  **Self-Cloning Mechanism**: Creates timestamped versions of the core script, enabling non-destructive evolution.
4.  **Feedback Loop (Crash Dumps)**: Automatically generates diagnostic reports in Markdown when an evolved script fails.
5.  **Safety Layer**: Automatic `.bak` creation and an immutable core backup (`proteo_core_backup.py`).

## Evolutionary Path (Current Session)
- **Base Version**: Standard file operations and CLI.
- **Evolved Version (v1.1)**:
    - Added `Color` class for ANSI terminal feedback.
    - Added `read` action for content inspection.
    - Integrated visual feedback (Green for Success, Red for Errors, Yellow for Warnings).
    - Updated internal `SYSTEM_PROMPT` to reflect new capabilities.

## Data Structures
- **Operations JSON**: `{ "operations": [ { "action": "...", "path": "...", ... } ] }`
- **Actions Dictionary**: Mapping of strings to Python callables for extensible command handling.
