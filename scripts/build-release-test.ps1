$ErrorActionPreference = 'Stop'

$env:nspkg_version_part = "patch"
$env:sources = "D:\pypi\azure-iot-sdk-python-preview"
$env:dist = "D:\dist"

. $(Join-Path $PSScriptRoot build-release.ps1)

function Update-Version($part) {
    # disabled
}

 function Install-Bumpversion {
    # disabled
 }
 
 function Invoke-Python {
    # disabled
 }
 
 function Invoke-Python2x {
    # disabled
 }

Build