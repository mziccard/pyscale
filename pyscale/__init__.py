"""
PyScale: A workload prediction library for Python
=================================================


Contents
--------
PyScale provides two classes
  1. `LoadPredictor` - Allows to predict load peaks given
  a time serie representing recent load history

  2. `PredictionPlotter` - Allows to output a plot of the
  input data and the load prediction function

How to use the documentation
----------------------------
Documentation is available in the docstrings. 
Code snippets are indicated by three greater-than signs

  >>> x = 42
  >>> x = x + 1
"""
from .load_predictor import LoadPredictor
from .prediction_plotter import PredictionPlotter
