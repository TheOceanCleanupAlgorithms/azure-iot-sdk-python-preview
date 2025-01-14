# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from setuptools import setup, find_packages
from io import open  # io.open needed for Python 2 compat

# azure v0.x is not compatible with this package
# azure v0.x used to have a __version__ attribute (newer versions don't)
try:
    import azure

    try:
        ver = azure.__version__
        raise Exception(
            "This package is incompatible with azure=={}. ".format(ver)
            + 'Uninstall it with "pip uninstall azure".'
        )
    except AttributeError:
        pass
except ImportError:
    pass


with open("README.md", "r") as fh:
    _long_description = fh.read()


setup(
    name="azure-iot-device",
    version="2.0.0-preview.8",
    description="Microsoft Azure IoT Device Library",
    license="MIT License",
    url="https://github.com/Azure/azure-iot-sdk-python-preview",
    author="Microsoft Corporation",
    author_email="opensource@microsoft.com",
    long_description=_long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        # Define sub-dependencies due to pip dependency resolution bug
        # https://github.com/pypa/pip/issues/988
        "urllib3>1.21.1,<1.25",
        # Actual project dependencies
        "six>=1.12.0,<2.0.0",
        "paho-mqtt>=1.4.0,<2.0.0",
        "transitions>=0.6.8,<1.0.0",
        "requests>=2.20.0,<3.0.0",
        "requests-unixsocket>=0.1.5,<1.0.0",
        "janus>=0.4.0,<1.0.0;python_version>='3.5'",
        "futures;python_version == '2.7'",
    ],
    extras_require={":python_version<'3.0'": ["azure-iot-nspkg>=1.0.1"]},
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3*, <4",
    packages=find_packages(
        exclude=[
            "tests",
            "samples",
            # Exclude packages that will be covered by PEP420 or nspkg
            "azure",
            "azure.iot",
        ]
    ),
    zip_safe=False,
)
