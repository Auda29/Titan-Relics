param([switch]$SkipGeneration)
$ErrorActionPreference = 'Stop'
$projectPython = Get-Command python -ErrorAction SilentlyContinue
if ($projectPython) {
    $pythonExe = $projectPython.Source
} else {
    $bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (Test-Path -LiteralPath $bundledPython) {
        $pythonExe = $bundledPython
    } else {
        throw 'Python 3.11 oder neuer installieren und tools/build.py ausführen.'
    }
}
$buildArguments = @((Join-Path $PSScriptRoot 'tools\build.py'))
if ($SkipGeneration) { $buildArguments += '--skip-generation' }
& $pythonExe @buildArguments
exit $LASTEXITCODE
