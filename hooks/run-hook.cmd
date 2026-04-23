@echo off
REM Windows launcher for hooks/session_start.py — invokes Python 3.11+ directly.
REM No Git Bash / WSL dependency per NFR-PORT-WIN-1.
python "%~dp0session_start.py" %*
