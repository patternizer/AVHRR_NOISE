![image](http://www.fiduceo.eu/sites/default/files/FIDUCEO-logo.png)

[![Build Status](https://travis-ci.org/patternizer/AVHRR_NOISE.svg?branch=master)](https://travis-ci.org/patternizer/AVHRR_NOISE)
[![Build status](https://ci.appveyor.com/api/projects/status/AVHRR_NOISE/branch/master?svg=true)](https://ci.appveyor.com/project/patternizer/AVHRR_NOISE-core)
[![codecov.io](https://codecov.io/github/patternizer/AVHRR_NOISE/coverage.svg?branch=master)](https://codecov.io/github/patternizer/AVHRR_NOISE?branch=master)
[![Documentation Status](https://readthedocs.org/projects/AVHRR_NOISE/badge/?version=latest)](http://AVHRR_NOISE.readthedocs.io/en/latest/?badge=latest)

# AVHRR_NOISE

Development code for creation of timeseries of AVHRR noise parameters.

## Getting started

To get started with AVHRR_NOISE, it is necessary to first retrieve the ASCII data from elastic tape, run the scripts to generate compressed netCDFs of the sensor/year/ concatenated summaries.

After installation, command-line utilities include:

    plot_noise_parameters.py

## Development

### Contributors

Thanks go to the members of the [FIDUCEO project consortium](http://www.fiduceo.eu/partners) for making the data required available. 

### Unit-testing

Unit testing will be performed using `pytest` and its coverage plugin `pytest-cov`.

To run the unit-tests with coverage, type

    $ export NUMBA_DISABLE_JIT=1
    $ py.test --cov=AVHRR_NOISE test
    
We need to set environment variable `NUMBA_DISABLE_JIT` to disable JIT compilation by `numba`, so that 
coverage reaches the actual Python code. We use Numba's JIT compilation to speed up numeric Python 
number crunching code.

### Generating the Documentation

The documentation will be generated with the [Sphinx](http://www.sphinx-doc.org/en/stable/rest.html) tool to create
a [ReadTheDocs](http://AVHRR_NOISE.readthedocs.io/en/latest/?badge=latest). 
If there is a need to build the docs locally, some 
additional software packages are required:

    $ conda install sphinx sphinx_rtd_theme mock
    $ conda install -c conda-forge sphinx-argparse
    $ pip install sphinx_autodoc_annotation

To regenerate the HTML docs, type    
    
    $ cd doc
    $ make html

## License

The code is distributed under terms and conditions of the [MIT license](https://opensource.org/licenses/MIT).

## Contact information

* [Michael Taylor] (https://patternizer.github.io)

