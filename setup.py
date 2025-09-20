from setuptools import setup, find_packages

setup(
    name="chizhevsky_ai",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=2.0.0",
        "requests==2.31.0",
        "cryptography==41.0.7",
        "python-telegram-bot==20.7",
        "pyyaml>=6.0"
    ],
    entry_points={
        'console_scripts': [
            'chizhevsky-ai=chizhevsky_ai.__main__:main',
        ],
    },
)
