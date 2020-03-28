import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mercari',
    version='0.0.5',
    author='marvinody',
    author_email='manny@sadpanda.moe',
    description='mercari api-like wrapper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/marvinody/mercari/',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.5",
    ]
)
