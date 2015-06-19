import os, sys, inspect

CURRENT_DIR = os.path.dirname(
  os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, PARENT_DIR)

from pyscale import LoadPredictor
from pyscale import PredictionPlotter

def main():
    data1 = []
    with open(CURRENT_DIR+'/data/load1.dat') as stream:
        lines = stream.readlines()
        for line in lines:
            data1.append(int(line))
        predictor = LoadPredictor(data1)
        print predictor

        plotter = PredictionPlotter(predictor)
        plotter.xlabel('Load')
        plotter.ylabel('Probability')
        plotter.plot(CURRENT_DIR+'/plot1.png', 0.001, 0.00001)

    data2 = []
    with open(CURRENT_DIR+'/data/load2.dat') as stream:
        lines = stream.readlines()
        for line in lines:
            data2.append(int(line))
        predictor2 = LoadPredictor(data2)
        print predictor2

        plotter2 = PredictionPlotter(predictor2)
        plotter2.xlabel('Load')
        plotter2.ylabel('Probability')
        plotter2.plot(CURRENT_DIR+'/plot2.png', 0.001, 0.00001)

if __name__ == "__main__":
    main()
