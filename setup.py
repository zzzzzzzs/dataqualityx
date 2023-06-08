import os
import platform
import shlex
import shutil
import subprocess

from setuptools import find_packages, setup

from dataqualityx import NAME, VERSION

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    author="zzzzzzzs",
    author_email="1443539042@qq.com",
    description="data quality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zzzzzzzs/dataqualityx",
    packages=find_packages(exclude=("task",)),
    include_package_data=True,
    entry_points={"console_scripts": ["dataqualityx = dataqualityx.app:main"]},
)
