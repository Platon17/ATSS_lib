from setuptools import setup, find_packages

setup(
    name="atss",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'atss=atss.cli:main',
        ],
    },
    author="platon17",
    description="Library for analyzing acrostic texts for hidden messages",
)
