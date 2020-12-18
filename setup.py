from pathlib import Path

from setuptools import setup

from pyinstaller_extractor.version import VERSION

HERE = Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name='pyinstaller_extractor',
    version=VERSION,
    description='Pyinstaller Extractor',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/khiemdoan/pyinstaller_extractor',
    author='Khiem Doan',
    author_email='doankhiem.crazy@gmail.com',
    license='LGPL-2.1 License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
    ],
    packages=['pyinstaller_extractor'],
    include_package_data=True,
    install_requires=['pyinstaller', 'uncompyle6', 'xdis'],
    entry_points={
        'console_scripts': [
            'pyinstaller_extractor=pyinstaller_extractor.__main__:main',
        ]
    },
)
