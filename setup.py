# _*_ coding: utf-8 _*_
"""
Time:     2023/5/18 16:38
Author:   刘征昊(£·)
Version:  V 1.1
File:     setup.py
Describe: 
"""

import setuptools
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="liuzh594Crypto",
    version="5.9.4.99.9",
    author="Liuzhenghao",
    author_email="liuzh594@qq.com",
    description="my crypto python package in 2023",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lzh594/liuzh594Crypto",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
