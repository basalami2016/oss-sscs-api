from setuptools import setup

setup(
    name='software-supply-chain-security',
    version='0.1.0',
    py_modules=['ossapi', 'ado.boards', 'azure-devops'],   
    entry_points={
        'console_scripts': ['software-supply-chain-security=ossapi:main']
    },
)
