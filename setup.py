from setuptools import setup, find_packages

setup(
    name='sorunlib',
    version="v0.1.0",
    description='OCS Control Programs for running the observatory.',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        'ocs',
    ],
    extras_require={
        "tests": ["pytest", "pytest-cov"],
        "docs": ["sphinx==4.2.0", "sphinx_rtd_theme==1.0.0"],
    },
)
