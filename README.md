# SimFOOOF

This repository hosts code for testing [FOOOF]((https://github.com/fooof-tools/fooof)) with simulated data.

## Overview

The analyses in this repository were done for the paper
[`Parameterizing Neural Power Spectra`](https://doi.org/10.1101/299859).

This repository contains only simulation analyses. A guide to the paper's analyses, and where
each is described is available [here](https://github.com/fooof-tools/Paper).

## Guide

If you want to go through this analysis, you can work through everything in the `notebooks`.

## Requirements

This project was written in Python 3 and requires Python >= 3.7 to run.

In addition to general scientific Python packages (available in the [Anaconda](https://www.anaconda.com/distribution/) distribution) this analysis requires the following Python packages:

- [fooof](https://github.com/fooof-tools/fooof) >= 1.0.0
- [neurodsp](https://github.com/neurodsp-tools/neurodsp) >= 2.0.0

All required 3rd party packages are described in `requirements.txt`.

## Repository Layout

This project repository is set up in the following way:

- `code/` contains custom code for this analysis
- `notebooks/` is a collection of Jupyter notebooks perform the analsis and create the figures
