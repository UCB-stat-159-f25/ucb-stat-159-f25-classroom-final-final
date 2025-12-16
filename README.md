[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/sSkqmNLf)

# Group 25 Final Project

## Analyzing and predicting trends in natural disasters across the world 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/UCB-stat-159-f25/final-group25/HEAD)

## Overview

This analysis conducts some EDA and hypothesis testing to observe the trends in natural disasters, including relationships between factors such as economic loss, total days to recover, the severity of the disaster, etc. Later in the analysis, we will be constructing a Multiple Linear Regression model to help us find out the effects of the different factors involving a natural disaster on the days to recover, in addition to helping us predict how many days a country takes to recover given the magnitude of these factors.

## Data Source

Our data was sourced from this [online kaggle dataset](https://www.kaggle.com/datasets/zubairdhuddi/global-daset/data), containing about 50,000 rows and 12 columns.

## Website

Here is a link to our Project Website: [https://ucb-stat-159-f25.github.io/final-group25/](https://ucb-stat-159-f25.github.io/final-group25/)

## Repository Structure

Our repository follows this structure:

* `data/`: Contains the csv file that our project uses to load in the data
* `figures/`: Contains generated plots and other figures
* `utilities/`: Module containing the functions that were used during this project. This module also includes tests that you can run in the terminal
* `main.ipynb`: Our main commentary notebook, detailing the analysis at a high level. This notebook goes over some of the motivations, processes, and conclusions during our analysis.
* `Predicting recovery days.ipynb`: Notebook containing code required to process and visualize data for later use in Multiple Linear Regression, in addition to actually constructing our model step by step.
* `environment.yml`: File containing required packages for creating and using the environment
* `Makefile`: Makefile to run all notebuilds and create the environment.
* `exploratory_data_analysis.ipynb`: Conducts some exploratory data analysis of the dataset in addition to hypothesis testing

## Testing and creating the environment

You can run tests by running the following command in the terminal after having initialized the environment:

	pytest utilities

You can create the environment by just running:

	make env

Then create the environment by running:

	conda activate final-group25

Finally, install the ipython kernel by running:

	python -m ipykernel install --user --name final-group25 --display-name "IPython - final-group25" 

You can also clean the repository by running:

	make clean










