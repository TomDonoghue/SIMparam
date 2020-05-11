# SimFOOOF

Project repository, part of the `Parameterizing Neural Power Spectra` project. 

This reposisotry tests the power spectrum parameterization algorithm on simulated data.

[![Preprint](https://img.shields.io/badge/preprint-10.1101/299859-informational.svg)](https://doi.org/10.1101/299859)

## Overview

This repository tests the [FOOOF](https://github.com/fooof-tools/fooof) algorithm on simulated data.

Simulation tests include:
- testing performance on reconstructing individual periodic and aperiodic parameters
- testing performance with global measures such as the number of fit peaks and model reconstruction error
- testing how sensitive the algorithm is to model assumptions and violations of these assumptions

## Guide

You can follow along with this project by looking through everything in the `notebooks`.

## Reference

The analyses in this repository were done as part of the
[`Parameterizing Neural Power Spectra`](https://doi.org/10.1101/299859) paper.

A guide to all the analyses included in this paper is available
[here](https://github.com/fooof-tools/Paper).

## Requirements

This project was written in Python 3 and requires Python >= 3.7 to run.

In addition to general scientific Python packages (available in the [Anaconda](https://www.anaconda.com/distribution/) distribution) this analysis requires the following Python packages:

- [fooof](https://github.com/fooof-tools/fooof) >= 1.0.0
- [neurodsp](https://github.com/neurodsp-tools/neurodsp) >= 2.0.0

All required 3rd party packages are described in `requirements.txt`.

## Repository Layout

This project repository is set up in the following way:

- `code/` contains custom code for this analysis
- `figures/` contains the figures produced during these analyses
- `notebooks/` is a collection of Jupyter notebooks that perform the analyses and create figures
