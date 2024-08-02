# setup.py

from setuptools import setup, find_packages

setup(
    name='mjolnir_arq',
    version='0.0.4',
    description='A simple example package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Marlon Andres Leon Leon',
    author_email='dandresleon64@gmail.com',
    url='https://github.com/dandres10/mjolnir_arq',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'mj=mjolnir_arq.module:main',  
        ],
    },
)
