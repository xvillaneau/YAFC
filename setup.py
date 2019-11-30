
import setuptools

setuptools.setup(
    name="YAFC",
    version="0.1",
    description="Basic (an somewhat restricted) calculator for Factorio",
    author="Xavier Villaneau",
    author_email="xvillaneau@gmail.com",
    license="MIT",
    packages=["yafc", "libyafc"],
    install_requires=["pyYAML", "marshmallow"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['yafc = yafc.__main__:main']
    },
)
