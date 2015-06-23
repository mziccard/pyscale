# PyScale

A workload prediction library for Python. 
PyScale can be used to estimate future loads 
(in terms of traffic/CPU load/memory usage) of your 
web application/service to help you scale up/out 
proactively. 

## Load Prediction

PyScale uses Extreme Value Analysis (EVA) to predict the workload 
of your deployed services. 
To predict workload peaks, PySCale feds to Extreme Value 
Analysis a time serie representing a history of loads. 
This technique can be applied to different metrics as, for instance, 
traffic load, memory consumption or CPU usage. 
EVA fits to the provided data a 
continous probability distribution. 
From the 
corresponding survival function (1 - cumulative distribution function) 
it is possible to extract values that are only exceeded 
with arbitrarily low probabilities.  

For instance, let's pick from the survival function computed via EVA 
a probability _p = 0.001_ and its corresponding 
load value _x_ 
(where _x_ indicates either traffic load, memory requirements or CPU usage). 
We now not only have a prediction of future load but we also know the 
probability that this prediction is exceeded. 
Scaling up/out our service so that is can handle a load of _x_ 
means knowing that the probability of overloading the service is 
_p = 0.001_. That is, _99.9%_ of uptime.

## Usage

To predict a load peak at a given probability 
you can instantiate an object of the class `LoadPredictor` as:

```python
from pyscale import LoadPredictor

load_data = [ 4352, 4472, 3847, 4915, 4969, 4333, 4381, 4091, 4135, 4160,
              3534, 4598, 4086, 3788, 4038, 3396, 4118, 3822, 4333, 4034 ]
predictor = LoadPredictor(load_data)
load_peak = predict_load(0.001)
```

You can also produce a plot of the survival function by istantiating an 
object of the class `PredictionPlotter`: 

```python
from pyscale import LoadPredictor

load_data = [ 4352, 4472, 3847, 4915, 4969, 4333, 4381, 4091, 4135, 4160,
              3534, 4598, 4086, 3788, 4038, 3396, 4118, 3822, 4333, 4034 ]
predictor = LoadPredictor(load_data)
plotter   = PredictionPlotter(predictor)
plotter.xlabel('Requests')
plotter.ylabel('Probability')
plotter.plot("plot.png", 0.001)
```

## Example

After cloning the repository you can move to the root of the 
project and run the example with:

```bash
python examples/example1.py
```

This example takes input data from two files in `examples/data` and produces 
in `examples` two plots representing load prediction made starting from 
the time series in the two data files.
