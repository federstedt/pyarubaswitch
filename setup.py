import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyarubaswitch",
    version="0.0.1",
    author="Daniel Federstedt",
    author_email="dfederstedt@gmail.com",
    description="python requests based REST-API-Client for aruba switches",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/federstedt/pyarubaswitch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
