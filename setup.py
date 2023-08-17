from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()
setup(
    name='easyGPGTool',
    version='0.2',
    packages=['easyGPGTool'],
    include_package_data=True,
    long_description_content_type='text/x-rst',
    description='A GUI GPG tool application',
    long_description=long_description,
    author='Mehdi Ghazanfari',
    author_email='mehdirexon@gmail.com',
    url='https://github.com/MehdiREXON/easyGPGTool',
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
    python_requires=">=3.10"
)
