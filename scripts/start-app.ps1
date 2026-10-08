# Start the demo application only. Do not prepare or run the test environment.
$ErrorActionPreference = 'Stop'
$AppScript = Join-Path (Split-Path -Parent $PSScriptRoot) 'qa-demo-app\run.py'
[string[]]$AppArgs = @($args)

function Find-Python {
    $Candidates = @('py.exe', 'python.exe', 'python3.exe')
    $Candidates += @(Get-Command 'python3.*.exe' -CommandType Application -ErrorAction SilentlyContinue |
        Sort-Object Name -Descending | Select-Object -ExpandProperty Source)
    foreach ($Candidate in $Candidates) {
        foreach ($Resolved in @(Get-Command $Candidate -CommandType Application -All -ErrorAction SilentlyContinue)) {
            [string[]]$Prefix = if ($Resolved.Name -eq 'py.exe') { @('-3') } else { @() }
            try {
                & $Resolved.Source @Prefix -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' *> $null
                if ($LASTEXITCODE -eq 0) {
                    return [PSCustomObject]@{ Executable = $Resolved.Source; Prefix = $Prefix }
                }
            } catch {
                # Try the next installed interpreter.
            }
        }
    }
    throw 'Python 3.11+ was not found. Install Python and make its command available in PATH, then run start-app.cmd again.'
}

try {
    $Interpreter = Find-Python
    $Prefix = $Interpreter.Prefix
    & $Interpreter.Executable @Prefix -B -u $AppScript @AppArgs
    exit $LASTEXITCODE
} catch {
    [Console]::Error.WriteLine('ERROR: ' + $_.Exception.Message)
    exit 1
}
