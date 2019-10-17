#!/usr/bin/env python3

"""Setup script"""

from setuptools import setup

from library_manager import __version__

setup(name='library_manager',
      version=__version__,
      description='Manage Library database',
      author='Daniele Fucini',
      author_email='dfucini@gmail.com',
      license='GPL3',
      url='https://github.com/Fuxino/library_manager',
      packages=['library_manager'],
      data_files=[('share/icons/hicolor/32x32/apps', ['library_manager/icons/library_manager.png']),
                  ('share/applications', ['library_manager.desktop']),
                 ],
      entry_points={
          'gui_scripts':[
              'library_manager=library_manager.__main__:main'
          ],
      },
      )
