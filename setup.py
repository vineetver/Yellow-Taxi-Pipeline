from pathlib import Path
from setuptools import find_namespace_packages, setup

BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

setup(
    name='YellowTaxiPipeline',
    version='0.1',
    description='Machine learning pipeline to analyze 1B+ NYC Taxi Trips',
    author='Vineet Verma',
    author_email='vineetver@hotmail.com',
    url="https://github.com/vineetver/Yellow-Taxi-Pipeline",
    python_requires='>=3.7',
    packages=find_namespace_packages(exclude=['test']),
    install_requires=[required_packages],
)
