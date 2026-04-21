#!/usr/bin/env python3
"""
TradeStation SDK Setup Script

For backward compatibility. Prefer using pyproject.toml with:
    pip install -e .
"""

from pathlib import Path

from setuptools import find_packages, setup

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="tradestation-python-sdk",
    version="1.0.0",
    description="Unofficial Python SDK for TradeStation API v3 with full REST API and HTTP Streaming support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ben Laube",
    author_email="ben@example.com",
    url="https://github.com/benlaube/tradestation-python-sdk",
    project_urls={
        "Documentation": "https://github.com/benlaube/tradestation-python-sdk/tree/main/docs",
        "Source": "https://github.com/benlaube/tradestation-python-sdk",
        "Issues": "https://github.com/benlaube/tradestation-python-sdk/issues",
        "Changelog": "https://github.com/benlaube/tradestation-python-sdk/blob/main/CHANGELOG.md",
    },
    packages=find_packages(exclude=["tests*", "examples*", "docs*", "cli*"]),
    python_requires=">=3.10",
    install_requires=[
        "httpx>=0.27.2",
        "PyJWT>=2.8.0",
        "pydantic>=2.12.5",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
        ],
        "examples": [
            "jupyter>=1.0.0",
            "notebook>=7.0.0",
            "matplotlib>=3.7.0",
            "pandas>=2.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
    ],
    keywords="tradestation trading api sdk futures stocks options forex algorithmic-trading market-data order-execution",
    license="MIT",
    zip_safe=False,
)
