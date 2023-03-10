from setuptools import setup,find_packages
with open('README.md','r')as f:
    long_description = f.read()
setup(
    name='easyGPG',
    version='0.2.2',
    include_package_data=True,
    description='A GUI GPG tool application',
    long_description = long_description,
    author='Mehdi Ghazanfari',
    author_email='mehdirexon@gmail.com',
    url = 'https://github.com/MehdiREXON/easyGPG',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.1",
        "Operating System :: POSIX :: Linux",
        "Topic :: Security :: Cryptography"
    ],
    install_requires=[
        'plyer',
        'colorama',
        'python-gnupg',
        'python-magic',
        'python-dateutil',
        'PySide6'
    ],
    python_requires = ">=3.10"
)