from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("bot_core.py", compiler_directives={'language_level': "3"})
)
