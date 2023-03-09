from setuptools import setup
  
setup(
    name='GPG Tool',
    version='beta',
    description='A GUI GPG tool',
    author='Mehdi GHazanfari',
    author_email='Mehdi Ghazanfari',
    packages=['ext'],
    install_requires=[
        'plyer',
        'colorama',
        'python-gnupg',
        'python-magic',
        'python-dateutil',
        'PySide6-Essentials',
        'PySide6-Addons',
        'PySide6',
    ],
)