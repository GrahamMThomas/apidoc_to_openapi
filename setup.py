import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apidoc_to_openapi",
    scripts=["bin/apidoc-to-openapi"],
    version="0.0.2",
    author="Graham Thomas",
    author_email="grahamthethomas@gmail.com",
    description="A python package which converts apidoc comments in various languages to OpenApi Spec .json files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GrahamMThomas/apidoc_to_openapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["colorama", "pyyaml"],
    python_requires=">=3.6",
)
