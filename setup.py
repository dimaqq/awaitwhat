from distutils.core import setup, Extension

helper = Extension('what',
                    sources = ['what.c'])

setup (name = 'Await What?',
       version = '0.0',
       description = 'Await What?',
       ext_modules = [helper])
