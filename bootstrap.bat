@echo off
REM Windows cmd launcher — delegates to scripts\bootstrap.py.
REM Python 3.11+ is the only prerequisite.
python "%~dp0scripts\bootstrap.py" %*
