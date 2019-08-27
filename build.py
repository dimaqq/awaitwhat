from distutils.core import Extension
from distutils.command import build_ext

def build(setup_kwargs):
    setup_kwargs["ext_modules"] = [Extension("awaitwhat._what", ["what.c"])]
    setup_kwargs["cmdclass"] = build_ext
