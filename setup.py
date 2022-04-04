import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ReLoPr",
    version="0.0.1",
    author="Philipp Huismann",
    author_email="phil.huismann@gmail.com",
    description="Python lib to easily generate representative load profiles with python based on VDEW-Loadprofilese",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)