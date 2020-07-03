import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="solve_coding_challenge-HEDRICH", # Replace with your own username
    version="0.0.1",
    author="Kolja Hedrich",
    author_email="kolja.hedrich@gmx.de",
    description="Package contains the submission for the -msg Coding Challenge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hedrich9000/Coding_Challenge_msg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)