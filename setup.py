import re
import ast
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('pytest_seldom/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setuptools.setup(
    name="pytest-seldom",
    version=version,
    author="bugmaster",
    author_email="fnngj@126.com",
    description="A pytest wrapper with fixtures for Seldom to automate web browsers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seldomQA/seldom-pytest",
    packages=["pytest_seldom"],
    include_package_data=True,
    install_requires=[
        "pytest-html>=3.0.0",
        "poium>=1.0.2",
        "pytest",
        "pytest-base-url",
        "webdriver-manager>=3.5.0",
    ],
    entry_points={"pytest11": ["seldom = pytest_seldom.pytest_seldom"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Framework :: Pytest",
    ],
    python_requires=">=3.7",
    setup_requires=["setuptools_scm"],
)
