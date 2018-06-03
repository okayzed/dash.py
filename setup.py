from distutils.core import setup

setup(
    name='dashdoc',
    version='0.0.1',
    author='okay',
    author_email='okay.zed+dashdo@gmail.com',
    packages= ["dashdoc", "dashdoc.lib"],
    package_dir={'dashdoc': 'src/', 'dashdoc.lib' : 'src/lib' },
    scripts=['bin/dashdoc'],
    url='http://github.com/okayzed/dashdoc',
    license='MIT',
    description='a CLI for dash',
    long_description=open('README').read(),
    )

