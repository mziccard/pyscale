from scipy.stats import gumbel_r as gumbel
import warnings
import sys

class LoadPredictor(object):
    """
    LoadPredictor(data, block_size=0)

    Applies Extreme Value Analysis to a sample of data.
    Computes the discete survival function for the provided data.
    If needed, applies Block Maxima to the sample and then fits a
    Gumbel distribution.
    Allows to extract values from the survival function
    for arbitrarily low exceedance probabilities

    Parameters
    ----------
    data : ndarray
      Sample of load data to analyze. Can have several sources
      (traffic, memory, CPU usage)
    block_size : int, optional
      Block size to apply block maxima technique. If not specified
      and enough data is provided (len(data) > 40) a
      suitable block size is computed

    Raises
    ------
    Exception
      When len(data)<10, not enough data is provided do make predictions

    Examples
    --------
    >>> from pyscale import LoadPredictor
    >>> load_data = [ 4352, 4472, 3847, 4915, 4969, 4333, 4381, 4091, 4135,
    ... 4160, 3534, 4598, 4086, 3788, 4038, 3396, 4118, 3822, 4333, 4034 ]
    >>> predictor = LoadPredictor(load_data)
    """
    def __init__(self, data, block_size=0):
        if len(data) < 10:
            raise Exception("Not enough data to make predictions")

        self.__data = data
        histogram = {}

        if block_size:
            self.__block_size = block_size
        else:
            # Block sizes between 20 and 50 are ok if
            # all the dataset can be represented in less
            # than 20 blocks
            self.__block_size = len(data)/20

        if self.__block_size < 1:
            warnings.warn("Invalid block size, set it to 1")
            self.__block_size = 1

        block_maxima = []

        current_block_size = 0
        current_block_maximum = -sys.maxint - 1

        # Compute block maxima
        for value in data:
            if value in histogram:
                histogram[value] += 1
            else:
                histogram[value] = 1
            current_block_size += 1
            if value > current_block_maximum:
                current_block_maximum = value
            if current_block_size == self.__block_size:
                block_maxima.append(current_block_maximum)
                current_block_maximum = 0
                current_block_size = 0

        # Build original 1-cdf histogram
        self.__values = histogram.keys()
        self.__values.sort()
        self.__values.pop()
        self.__frequencies = []
        previous = 0.0
        for value in self.__values:
            previous = histogram[value]/float(len(self.__data)) + previous
            self.__frequencies.append(1-previous)

        # Fit Gumbel distribution to block maxima
        params = gumbel.fit(block_maxima)
        self.__shape = 0
        self.__location = params[0]
        self.__scale = params[1]

    def predict_load(self, probability):
        """
        Returns a value that corresponds to the specified probability
        in the Gumbel survival function computed via EVA. The value is
        such that according to EVA it is only exceeded with the
        specified probability

        Parameters
        ----------
        probability : float
          The desired probability

        Returns
        -------
        value : int or float
          A value such that according to EVA it is only exceeded with the
          specified probability

        Examples
        --------
        >>> from pyscale import LoadPredictor
        >>> load_data = [ 4352, 4472, 3847, 4915, 4969, 4333, 4381, 4091, 4135,
        ... 4160, 3534, 4598, 4086, 3788, 4038, 3396, 4118, 3822, 4333, 4034 ]
        >>> predictor = LoadPredictor(load_data)
        >>> predictor.predict_load(0.001)
        6527.0363787150509
        """
        return gumbel.isf(probability, self.__location, self.__scale)

    def survival_data(self):
        """
        Returns the histogram representing the discrete survival
        distribution computed from the input data (no EVA involved)

        Returns
        -------
        values : ndarray
          List of unique values from input data, in ascending order
        frequencies : ndarray
          Discrete probability values for the survival function such that
          frequencies[i] is the discrete probability of values[i]

        Examples
        --------
        >>> from pyscale import LoadPredictor
        >>> load_data = [ 4352, 4472, 3847, 4915, 4969,
        ... 4333, 4381, 4091, 4135, 4034 ]
        >>> predictor = LoadPredictor(load_data)
        >>> predictor.survival_data()
        ([3847, 4034, 4091, 4135, 4333, 4352, 4381, 4472, 4915],
        [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1])
        """
        return (self.__values, self.__frequencies)

    def gev_parameters(self):
        """
        Returns the parameters (shape, location and scale) that describe
        the Gumbel distribution fit by Extreme Value Analysis

        Returns
        -------
        shape : float
          Shape of the curve (0 for Gumbel)
        location : float
          Parameter that determines the shift of the distribution
        scale : float
          Scale of the distribution function

        Examples
        --------
        >>> from pyscale import LoadPredictor
        >>> load_data = [ 4352, 4472, 3847, 4915, 4969, 4333, 4381, 4091, 4135,
        ... 4160, 3534, 4598, 4086, 3788, 4038, 3396, 4118, 3822, 4333, 4034 ]
        >>> predictor = LoadPredictor(load_data)
        >>> predictor.gev_parameters()
        (0, 4191.2070584065641, 280.17234166683176)
        """
        return (self.__shape, self.__location, self.__scale)

    def __str__(self):
        return 'epsilon (shape) = {0}\n'.format(self.__shape) + \
          'mu (location) = {0}\n'.format(self.__location) + \
          'sigma (scale) = {0}'.format(self.__scale)
