from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='crawlrice',
    version='1.0.0',
    author='Rice',
    description='Automatic IDOR/BAC scanner with Selenium-based crawling and Flask GUI.',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'crawlrice = Cli_Crawlrice.crawlrice:main',
        ],
    },
)