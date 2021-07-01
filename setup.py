# type: ignore

from setuptools import setup

__version__ = "1.1.0"

setup(
    name="flake8_loopy",
    version=__version__,
    description="flake8 plugin to check code quality in loops",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    author="Benjamin Scharf",
    author_email="benjamin.d.scharf@gmail.com",
    url="https://github.com/bdscharf/flake8_loopy",
    project_urls={
        "Documentation": "https://github.com/bdscharf/flake8_loopy/blob/main/README.md",
        "Source": "https://github.com/bdscharf/flake8_loopy",
        "Tracker": "https://github.com/bdscharf/flake8_loopy/issues",
    },
    download_url=f"https://github.com/bdscharf/flake8_loopy/archive/refs/tags/v{__version__}.tar.gz",
    classifiers=[
        "Framework :: Flake8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    keywords="flake8",
    py_modules=[
        "flake8_loopy",
        "flake8_loopy.defs",
        "flake8_loopy.visitor",
        "flake8_loopy.error_codes",
    ],
    install_requires=["flake8>=3.0.0"],
    entry_points={"flake8.extension": ["LPY = flake8_loopy:LoopyPlugin"]},
)
