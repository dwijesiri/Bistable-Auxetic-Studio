# Bistable Auxetic Studio

![Image_1](Resources/Image_1.png)

## Overview:

A lightweight application to create Bistable Auxetic Surfaces, programmed in pure python, with an intuitive Graphical User Interface (GUI). Patterns can be exported as .SVG files for lasercutting and take the form of .baux files.

## Notes:

There is a bug which makes the application crash about every 1 in 8 times, due to a Python GIL error, and cells will currently take any positive Thickness and Theta value, regardless of whether it is realistic or not (should be fixed in 1 - 2 months). I am currently investigating FEM simulations to visualise and predict the deployed state.

## Credits:

This program is based off the paper: ['Bistable Auxetic Surface Structures'](https://www.julianpanetta.com/pdf/bistable_auxetics.pdf) by Tian Chen, Julian Panetta, Max Schnaubelt and Mark Pauly, though there is no personal or professional affiliation with them.
