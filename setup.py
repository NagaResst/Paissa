from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="paissa",
    version="1.0.0",
    author="夕山菀",
    author_email="your-email@example.com",
    description="FF14国服市场价格查询和成本计算工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NagaResst/Paissa",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "PyQt5>=5.15.0",
    ],
    entry_points={
        "console_scripts": [
            "paissa=main:main",
        ],
    },
    package_data={
        "Data": ["*.Pdt", "*.py", "*.json"],
        "UI": ["*.ui", "*.py"],
    },
    include_package_data=True,
)