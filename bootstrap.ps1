# PowerShell launcher — delegates to scripts/bootstrap.py.
# Python 3.11+ is the only prerequisite.
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$scriptDir\scripts\bootstrap.py" $args
exit $LASTEXITCODE
