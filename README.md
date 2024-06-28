# Bistable Auxetic Studio

![Image_1](Resources/Image_1.png)

## Overview:

A lightweight application to create Bistable Auxetic Surfaces, programmed in pure python, with an intuitive Graphical User Interface (GUI). Patterns can be exported as .SVG files for lasercutting and take the form of .baux files.

## Notes:

- [ ] There is a bug which makes the application crash about every 1 in 8 times, due to a Python GIL error.
- [ ] I am currently investigating FEM simulations to visualise and predict the deployed state.
- [ ] The data from FEM could be fed into a CNN (Convolutional Neural Network) to efficiently predict the deployed state.

## Progress:

- [x] Previously, cells took any positive Thickness and Theta value, regardless of whether it is realistic or not. Now, Thickness must be between 0 to 30% of Cell Size, while Theta can range between 0 to 60 degrees.

## Credits:

This program is based off the paper: ['Bistable Auxetic Surface Structures'](https://www.julianpanetta.com/pdf/bistable_auxetics.pdf) by Tian Chen, Julian Panetta, Max Schnaubelt and Mark Pauly, though there is no personal or professional affiliation with them.
