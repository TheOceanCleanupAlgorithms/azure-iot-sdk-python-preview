#$WhatIfPreference = $true

function Install-Bumpversion {
    pip install bumpversion
    pip install wheel
}

function Update-Version($part) {
    bumpversion.exe $part --config-file .\.bumpverion.cfg --allow-dirty .\setup.py
}

function Invoke-Python {
    python setup.py sdist
    python setup.py bdist_wheel
}

function Invoke-Python2x {
    pip install virtualenvwrapper-win
    $py2 = "C:\Python27amd64\python.exe"
    mkvirtualenv --python=$py2 python2-64
    workon python2-64
    python setup.py bdist_wheel
    rmvirtualenv python2-64
}

function Build {

    $sourceFiles = $env:sources  # sdk repo top folder
    $dist = $env:dist  # release artifacts top folder

    # hashset key is package folder name in repo

    $packages = @{ }
    $packages["azure-iot-device"] = $env:device_version_part
    $packages["azure-iot-nspkg"] = $env:nspkg_version_part
    # TODO add new packages to this list

    New-Item $dist -Force -ItemType Directory
    Install-Bumpversion

    foreach ($key in $packages.Keys) {

        $part = $packages[$key]

        if ($part -and $part -ne "") {

            $packageFolder = $(Join-Path $sourceFiles $key)

            Write-Output "Increment '$part' version for '$key' "
            Write-Output "Package folder: $packageFolder"
            
            Set-Location $packageFolder
            Update-Version $part
            Invoke-Python

            if ($packages["azure-iot-nspkg"] -ne "") {

                Invoke-Python2x # this is an extra step required only for this package
            }

            $distfld = Join-Path $packageFolder "dist"
            $files = Get-ChildItem $distfld

            if ($files.Count -lt 1) {
                throw "$key : expected to find release artifacts"
            }

            $packagefld = Join-Path $dist $key
            New-Item $packagefld -Force -ItemType Directory
            Write-Output "Copying ($($files.Count)) package files to output folder"

            foreach ($file in $files) {

                $target = $(Join-Path $packagefld $file.Name)
                Write-Output "$($file.FullName) >> $target"
                Copy-Item $file.FullName $target
            }
        }
        else {
            Write-Output "no version bump for package '$key'"
        }
    }
}