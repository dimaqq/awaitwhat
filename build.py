from distutils.core import Extension

def build(setup_kwargs):
    setup_kwargs["ext_modules"] = [Extension("awaitwhat._what", ["awaitwhat/what.c"])]
