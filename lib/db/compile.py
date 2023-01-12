from __future__ import absolute_import, division, with_statement
"""
python complie.py build
rm -rf build
rm -rf __pycache__
"""
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from shutil import copyfile

ext_modules = [
    Extension("engine", ["engine.py"]),
    Extension("session", ["session.py"]),
    Extension("settings", ["settings.py"])
]

setup(
    name="db",
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)

import os

extensions = []
lib_dir_name = 'lib'
for dir in os.listdir('build'):
    if dir.startswith('lib.') and os.path.isdir(os.path.join('build', dir)):
        lib_dir_name = dir

for file in os.listdir(os.path.join('build', lib_dir_name)):
    new_file_name = file.split('.')[0]+'.'+file.split('.')[-1]
    copyfile(os.path.join('build', lib_dir_name, file), f'./{new_file_name}')

for file in os.listdir('./'):
    if file == '__init__.py':
        continue
    if file in extensions:
        continue
    if file.endswith('.py') or file.endswith('.pyc') or file.endswith('.c'):
        os.remove(file)
    if file.endswith('.so') or file.endswith('.pyd'):
        new_name = file.split('.')[0] + '.' + file.split('.')[-1]
        os.rename(file, new_name)
