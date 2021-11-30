from setuptools import setup, find_packages

setup(
    name='sorunlib',
    version="v0.1.0",
    description='OCS Control Programs for running the observatory.',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
