from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.stats import gumbel_r as gumbel
import numpy as np

class PredictionPlotter(object):
    """
    PredictionPlotter(predictor)

    Builds a configurable plotter that allows to output to a file
    a plot representing the data predicted via Extreme Value Analysis.
    Plotter allows to print both original data and predicted
    survival curve as well as to assign custom label to x and y axis.

    Parameters
    ----------
    predictor : LoadPredictor
      Object of the class LoadPredictor (or subclass) that allows
      to extract all data to be plotted

    Examples
    --------
    >>> from pyscale import LoadPredictor
    >>> load_data = [ 4352, 4472, 3847, 4915, 4969, 4333, 4381, 4091, 4135,
    ... 4160, 3534, 4598, 4086, 3788, 4038, 3396, 4118, 3822, 4333, 4034 ]
    >>> predictor = LoadPredictor(load_data)
    >>> plotter   = PredictionPlotter(predictor)
    >>> plotter.xlabel('Requests')
    >>> plotter.ylabel('Probability')
    >>> plotter.plot("plot.png", 0.001)
    """
    def __init__(self, predictor):
        self.__original_data = True
        self.__grid = True
        self.__predictor = predictor
        self.__figure = Figure()
        self.__subplt = self.__figure.add_subplot(111)

    def xlabel(self, label):
        """
        Sets the x axis label

        Parameters
        ----------
        label : str
          The label for the x axis

        Examples
        --------
        >>> from pyscale import LoadPredictor
        >>> load_data = [ 4352, 4472, 3847, 4915, 4969, 4333, 4381, 4091, 4135,
        ... 4160, 3534, 4598, 4086, 3788, 4038, 3396, 4118, 3822, 4333, 4034 ]
        >>> predictor = LoadPredictor(load_data)
        >>> plotter   = PredictionPlotter(predictor)
        >>> plotter.xlabel('Requests')
        """
        self.__subplt.set_xlabel(label)

    def ylabel(self, label):
        """
        Sets the y axis label

        Parameters
        ----------
        label : str
          The label for the y axis

        Examples
        --------
        >>> from pyscale import LoadPredictor
        >>> load_data = [ 4352, 4472, 3847, 4915, 4969, 4333, 4381, 4091, 4135,
        ... 4160, 3534, 4598, 4086, 3788, 4038, 3396, 4118, 3822, 4333, 4034 ]
        >>> predictor = LoadPredictor(load_data)
        >>> plotter   = PredictionPlotter(predictor)
        >>> plotter.ylabel('Probability')
        """
        self.__subplt.set_ylabel(label)

    def original_data(self, enable):
        """
        Enable or disable the display of discrete survival function.
        By default the discrete survival function is printed

        Parameters
        ----------
        enable : bool
          If True enables the display of discrete survival function
          If False disables the display of discrete survival function

        Examples
        --------
        >>> from pyscale import LoadPredictor
        >>> load_data = [ 4352, 4472, 3847, 4915, 4969, 4333, 4381, 4091, 4135,
        ... 4160, 3534, 4598, 4086, 3788, 4038, 3396, 4118, 3822, 4333, 4034 ]
        >>> predictor = LoadPredictor(load_data)
        >>> plotter   = PredictionPlotter(predictor)
        >>> plotter.original_data(False)
        """
        self.__original_data = enable

    def grid(self, enable):
        """
        Enable or disable the display of a grid on the plot.
        By default the grid is printed

        Parameters
        ----------
        enable : bool
          If True enables the display of the grid
          If False disables the display of the grid

        Examples
        --------
        >>> from pyscale import LoadPredictor
        >>> load_data = [ 4352, 4472, 3847, 4915, 4969, 4333, 4381, 4091, 4135,
        ... 4160, 3534, 4598, 4086, 3788, 4038, 3396, 4118, 3822, 4333, 4034 ]
        >>> predictor = LoadPredictor(load_data)
        >>> plotter   = PredictionPlotter(predictor)
        >>> plotter.grid(False)
        """
        self.__grid = enable

    def plot(self, filename, desired_exceedance=0.001, max_exceedance=0.00001):
        """
        Outputs the plot of the EVA survival function to a file.
        If specified also annotates the value for a provided probability of
        interest.
        Depending on how the object was configured might also output
        the discrete survival function.

        Parameters
        ----------
        filename : str
          The name of the output file
        desired_exceedance : float, optional
          An exceedance probability of interested, annotates the corresponding
          load value on the plot. Default value is 0.001
        max_exceedance : float, optional
          Minimum probability value on the y axis. Default value is 0.00001

        Examples
        --------
        >>> from pyscale import LoadPredictor
        >>> load_data = [ 4352, 4472, 3847, 4915, 4969, 4333, 4381, 4091, 4135,
        ... 4160, 3534, 4598, 4086, 3788, 4038, 3396, 4118, 3822, 4333, 4034 ]
        >>> predictor = LoadPredictor(load_data)
        >>> plotter   = PredictionPlotter(predictor)
        >>> plotter.plot("plot.png")
        """
        (values, frequencies) = self.__predictor.survival_data()
        params = self.__predictor.gev_parameters()

        max_value = self.__predictor.predict_load(max_exceedance)
        min_value = min(values)

        # 100 points should be enough
        x_points = np.linspace(min_value, max_value, (max_value-min_value)/100)
        self.__subplt.plot(
          x_points,
          gumbel.sf(x_points, params[1], params[2]),
          'r', linewidth=1.5, label='Extreme Value Distribution')

        if self.__original_data:
            self.__subplt.plot(
              values,
              frequencies,
              '.', alpha=0.2, label='Original Data')

        xlimits = self.__subplt.get_xlim()
        selected_value = self.__predictor.predict_load(desired_exceedance)
        self.__subplt.annotate(
          str(selected_value),
          xy=(selected_value, desired_exceedance))

        self.__subplt.plot([selected_value, selected_value],
          [0, desired_exceedance],
          '--', color='black')

        self.__subplt.plot([xlimits[0], selected_value],
          [desired_exceedance, desired_exceedance],
          '--', color='black')

        if self.__grid:
            self.__subplt.grid(
              b=True,
              which='major',
              color='black', alpha=0.2, linestyle='-')

        self.__subplt.set_yscale('log', nonposy='clip')
        yticks = []
        ytick = max_exceedance
        while ytick <= 10:
            yticks.append(ytick)
            ytick *= 10

        self.__subplt.set_yticks(yticks)
        self.__subplt.legend(loc='upper right')

        canvas = FigureCanvas(self.__figure)
        canvas.print_figure(filename)
