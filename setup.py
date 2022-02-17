from setuptools import setup, find_packages

setup(
    name='pysvelte',
    version="1.0.0",
    packages=find_packages(),
    python_requires='>=3.9.0',
    install_requires=[
        'torch>=1.10.1',
        'einops>=0.3.2',
        'numpy>=1.21.2',
        "typeguard",    
    ]
)