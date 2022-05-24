from setuptools import setup, find_packages

setup(
    name='Yellow_Taxi_Pipeline',
    version='0.1',
    description='This package contains the code for the Yellow Taxi Pipeline',
    author='Vineet Verma',
    author_email='vineetver@hotmail.com',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'scikit-learn',
        'gcsfs',
        'pyarrow',
        'requests',
        'jupyter',
        'seaborn',
        'pyspark'],
    entry_points={
        'console_scripts': [
            'preprocess_data = main.preprocess:main',
            'feature_engineering = main.feature_engineering:main',
            'train_model = main.train_model:main',
        ],
    }
)
