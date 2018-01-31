from distutils.core import setup

description = '''This is an interface module for DC Power Supply GPD-3303S manufactured by Good
Will Instrument Co., Ltd.'''

setup(name='PyGPD3303S',
      version='1.1.3',
      description='Python Interface for DC power supply GPD-3303S',
      author='Akira Okumura',
      author_email='oxon@mac.com',
      license='BSD License',
      platforms=['MacOS :: MacOS X', 'POSIX', 'Windows'],
      url='https://sourceforge.net/p/pygpd3303s/',
      py_modules=['gpd3303s'],
      install_requires=['pyserial'],
      classifiers=['Topic :: Terminals :: Serial',
                   'Development Status :: 4 - Beta',
                   'Programming Language :: Python',
                   ],
      long_description=description
      )
