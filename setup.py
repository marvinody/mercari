import setuptools

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mercari',
    version='1.0.3',
    author='marvinody',
    author_email='manny@sadpanda.moe',
    description='mercari api-like wrapper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/marvinody/mercari/',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ]
)
