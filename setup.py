from distutils.core import setup

description = '''This is an interface module for DC Power Supply GPD-3303S manufactured by Good
Will Instrument Co., Ltd.'''

setup(name='PyGPD3303S',
      version='2.0.0',
      description='Python Interface for DC power supply GPD-3303S',
      author='Akira Okumura',
      author_email='oxon@mac.com',
      license='BSD License',
      platforms=['MacOS :: MacOS X', 'POSIX', 'Windows'],
      url='https://github.com/akira-okumura/PyGPD3303S',
      py_modules=['gpd3303s'],
      install_requires=['pyserial'],
      classifiers=['Topic :: Terminals :: Serial',
                   'Development Status :: 5 - Production/Stable',
                   'Programming Language :: Python',
                   ],
      long_description=description
      )
