from setuptools import setup

setup(
    name="gitshield",
    version="1.0.0",
    description="GitHub Security Scanner CLI",
    author="frizz",
    py_modules=[
        "cli",
        "scanner",
        "rules",
        "risk_score",
        "github_scanner"
    ],
    install_requires=[
        "requests>=2.0.0",
        "rich>=13.0.0"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "gitshield=cli:main",
            "GitShield=cli:main"
        ],
    },
)