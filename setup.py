from setuptools import setup, find_packages

setup(
    name='sfCrime',
    version="0.1",
    packages=['sfCrime'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    scripts=['run.py'],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'sfCrime': ['*.msg'],
    },

    author="Kyle Irwin",
    author_email="Kyleairwin@gmail.com",
    description="A Data App",
    license="PSF",
    keywords="Machine Learning Data world example examples",
    url="",
)