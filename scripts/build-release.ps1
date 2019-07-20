function PipInstall {
    pip install bumpversion
    pip install wheel
}

function Update-Version($part) {
    bumpversion.exe $part --config-file .\.bumpverion.cfg --allow-dirty .\setup.py
}

function Build-Python {
    python setup.py sdist
    python setup.py bdist_wheel
}

function Build-Python2x {
    pip install virtualenvwrapper-win
    mkvirtualenv --python=$(Get-Python2x) python2-64
    workon python2-64
    python setup.py bdist_wheel
    rmvirtualenv python2-64
}

function Get-Python2x {
    return $(python -c "import sys; print sys.executable")
}

function Build {

    $sourceFiles = $env:sources  # sdk repo top folder
    $dist = $env:dist  # release artifacts top folder

    # hashset key is package folder name in repo

    $packages = @{ }
    $packages["azure-iot-device"] = $env:device_version_part
    $packages["azure-iot-nspkg"] = $env:nspkg_version_part

    New-Item $dist -Force -ItemType Directory

    PipInstall

    foreach ($key in $packages.Keys) {

        $part = $packages[$key]

        Write-Host "package '$key' version '$part'"

        if ($part -and $part -ne "") {
            Write-Host "version part: $part"

            $packageFolder = $(Join-Path $sourceFiles $key)

            Write-Host "package folder: $packageFolder"

            Set-Location $packageFolder
            Update-Version $part
        
            Build-Python

            if ($packages["azure-iot-nspkg"] -ne "") {

                # this is an extra step required only for this package
                Build-Python2x
            }

            $distfld = Join-Path $packageFolder "dist"
            $files = Get-ChildItem $distfld

            if ($files.Count -lt 1) {
                throw "$key : expected to find release artifacts"
            }

            $packagefld = Join-Path $dist $key
            New-Item $packagefld -Force -ItemType Directory

            foreach ($file in $files) {
                Copy-Item $file.FullName $(Join-Path $packagefld $file.Name)
            }
        }
        else {
            Write-Host "no version bump for package '$key'"
        }
    }
}