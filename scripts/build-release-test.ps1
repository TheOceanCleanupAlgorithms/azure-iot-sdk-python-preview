$ErrorActionPreference = 'Stop'

$env:nspkg_version_part = "patch"
$env:sources = "D:\pypi\azure-iot-sdk-python-preview"
$env:dist = "D:\dist"

. $(Join-Path $PSScriptRoot build-release.ps1)

function BumpVersion($part) {
    # disabled
}

 function PipInstall {
    # disabled
 }
 
 function PythonSetup {
    # disabled
 }
 
 function Python2x {
    # disabled
 }

# Write-Host GetPython2x

Build