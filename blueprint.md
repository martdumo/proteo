# Blueprint: Proteo Evolutionary Framework (v1.3)

## Architecture Overview
Proteo v1.3 is an autonomous, self-modifying engine that abstracts the development lifecycle into a secure JSON protocol. It is specifically optimized for high-integrity environments where AI agents must maintain and evolve code without human intervention.

### Core Systems
1.  **Validation Layer**: Uses Python's `ast` module to verify code integrity *before* writing to disk.
2.  **State Management**: 
    - **LAST_CLONE**: Dynamic path resolution for iterative evolution.
    - **DRY_RUN**: Global state for non-destructive simulation.
3.  **Resilience Engine**: 
    - **Auto-Rollback**: Immediate restoration of `.bak` files on subprocess failure.
    - **Crash Dumps**: Markdown-based diagnostic logs for self-repair.
4.  **Maintenance (Hygienic Collector)**: Automatic rotation of core files and cleanup of associated backups.
5.  **Persistence**: Seamless Git integration for immutable history tracking.

## Technical Specifications
- **Host OS**: Windows 11 / PowerShell.
- **Protocol**: JSON-based operations with atomic actions.
- **Modality**: Surgical String Replacement (Exact Match) for source code evolution.

## Evolution History (Current State)
- **v1.1**: Added Colors and `read` action.
- **v1.2**: Added `Dry-Run`, `search`, and `Repo Hygiene`.
- **v1.3**: Added `Syntax Validation`, `rename` action, `Auto-Rollback`, and `Git Integration`.

---
**Architectural Blueprint**  
*Evolucionar sin destruir.*
