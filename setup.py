"""Module installing the Embiggen package."""
from setuptools import find_packages, setup
from codecs import open as copen
import os
import re

here = os.path.abspath(os.path.dirname(__file__))


def readme():
    with open('README.rst', encoding="utf8") as f:
        return f.read()


test_deps = [
    "codacy-coverage",
    "coveralls",
    'pytest',
    "pytest-cov",
    "validate_version_code",
    "pylint",
    "silence_tensorflow"
]


def read(*parts):
    with copen(os.path.join(here, *parts), 'r', encoding="utf8") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


__version__ = find_version("embiggen", "__version__.py")

# TODO: Authors add your emails!!!
authors = {
    "Vida Ravanmehr": "vida.ravanmehr@jax.org",
    "Peter Robinson": "peter.robinson@jax.org",
    "Luca Cappelletti": "luca.cappelletti1@unimi.it",
    "Tommaso Fontana": "tommaso.fontana@mail.polimi.it"
}

setup(
    name='embiggen',
    version=__version__,
    description='🍇 Embiggen is the Python Graph Representation learning, Prediction and Evaluation module processing submodule of the GRAPE library.',
    long_description=readme(),
    url='https://github.com/monarch-initiative/embiggen',
    keywords='Graph Representation Learning,LINE,TransE,Node2Vec,DeeWalk',
    author=", ".join(list(authors.keys())),
    author_email=", ".join(list(authors.values())),
    license='BSD3',
    python_requires='>=3.8.0',
    packages=find_packages(
        exclude=['contrib', 'docs', 'tests*', 'notebooks*']),
    install_requires=[
        'numpy',
        'pandas',
        "Jinja2",
        "tqdm",
        "humanize",
        "matplotlib>=3.9",
        "scikit-learn>=1.5",
        "dict_hash>=1.1.32",
        "userinput>=1.0.20",
        "ddd_subplots>=1.0.27",
        "sanitize_ml_labels>=1.0.50",
        "keras_mixed_sequence>=1.0.28",
        "ensmallen>=0.8.94",
        "environments_utils>=1.0.10",
        "compress_pickle>=2.1.0",
        "validate_version_code",
        "cache_decorator>=2.1.14",
        "threadpoolctl>=3.1.0",
        "pydot",
        "compress_pickle>=2.1.0",
        "packaging"
    ],
    tests_require=test_deps,
    include_package_data=True,
    extras_require={
        'test': test_deps,
    },
)
