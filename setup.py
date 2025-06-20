from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sorunlib',
    version='v0.1.24',
    description='OCS Control Programs for running the observatory.',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    url="https://github.com/simonsobs/sorunlib",
    project_urls={
        "Source Code": "https://github.com/simonsobs/sorunlib",
        "Documentation": "https://sorunlib.readthedocs.io",
        "Bug Tracker": "https://github.com/simonsobs/sorunlib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    python_requires=">=3.9",
    install_requires=[
        'ocs==0.11.3',
        'pyyaml',
    ],
    extras_require={
        "tests": ["pytest>=7.0.0", "pytest-cov>=3.0.0", "pytest-mock>=3.12.0"],
        "docs": ["sphinx>=5.3.0", "sphinx_rtd_theme>=1.1.1"],
    },
)
