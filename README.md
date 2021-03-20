# SIM - Spectral Parameterization

Project repository, part of the `parameterizing neural power spectra` project.

This repository applies spectral parameterization to simulated data.

[![Paper](https://img.shields.io/badge/Paper-nn10.1038-informational.svg)](https://doi.org/10.1038/s41593-020-00744-x)

## Overview

This repository tests the [spectral parameterization](https://github.com/fooof-tools/fooof) algorithm on simulated data.

Simulation tests include:
- testing performance on reconstructing individual periodic and aperiodic parameters
- testing performance with global measures such as the number of fit peaks and model reconstruction error
- testing how sensitive the algorithm is to model assumptions and violations of these assumptions
- testing the algorithm in comparison to other related methods

## Guide

You can follow along with this project by looking through everything in the `notebooks`.

## Reference

The analyses in this repository were done as part of the
[`parameterizing neural power spectra`](https://doi.org/10.1038/s41593-020-00744-x) paper.

A guide to all the analyses included in this paper is available
[here](https://github.com/fooof-tools/Paper).

## Requirements

This project was written in Python 3 and requires Python >= 3.7 to run.

In addition to general scientific Python packages (available in the [Anaconda](https://www.anaconda.com/distribution/) distribution) this analysis requires the following Python packages:

- [fooof](https://github.com/fooof-tools/fooof) == 1.0.0
- [neurodsp](https://github.com/neurodsp-tools/neurodsp) >= 2.1.0

All required 3rd party packages are described in `requirements.txt`.

## Repository Layout

This project repository is set up in the following way:

- `code/` contains custom code for this analysis
- `notebooks/` is a collection of Jupyter notebooks that perform the analyses and create figures
