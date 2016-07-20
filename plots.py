import numpy as np
import matplotlib.pyplot as plt
import os.path
import collections
import math
import networkx as nx

class PlotFunction:
    def __init__(self, func, description):
        self._func = func
        self._description = description

    def description(self):
        return self._description

    def __call__(self, val):
        return self._func(val)

def identity(var = 'x'):
    return PlotFunction(lambda x: x, "${}$".format(var))

def linear(factor, var = 'x'):
    return PlotFunction(lambda x: factor * x, "${}{}$".format(factor, var)) 

def nlogn(var = 'x'):
    return PlotFunction(lambda x: x * math.log(x) if x > 0 else 0, "${0}\log({0})$".format(var)) 

def power(pow, var = 'x'):
    return PlotFunction(lambda x: x ** pow, "${{{}}}^{{{}}}$".format(var, pow))

def log(base = math.e, var = 'x'):
    if base == math.e:
        description = "$\log({})$".format(var)
    else:
        description = "$\log_{{{}}}({})$".format(base, var)
    return PlotFunction(lambda x: math.log(x, base) if x > 0 else 0, description)

def logpow(pow, var = 'x'):
    return PlotFunction(lambda x: math.log(x) ** pow if x > 0 else 0, "$\log^{{{}}}({})$".format(pow, var))

def exp(base=math.e, var = 'x'):
    if base == math.e:
        description = "$e^{{{}}}$".format(var)
    else:
        description = "${}^{{{}}}$".format(base, var)
    return PlotFunction(lambda x: base**x, description)


def set_up_plot(xlimit = None, ylimit = None):
    def wrap(f):
        def inner(*args, **kwargs):
            plt.cla()
            f(*args, **kwargs)
            plt.tick_params(axis='x',
                            which='both',
                            bottom='off',
                            top='off')
            plt.tick_params(axis='y',
                            which='both',
                            left='off',
                            right='off')
            axes = plt.gca()
            if xlimit is not None:
                axes.set_xlim(0, xlimit)
            if ylimit is not None:
                axes.set_ylim(0, ylimit)
            axes.set_aspect('equal', 'box-forced')
        return inner
    return wrap

def plot_funcs(*funcs, **kwargs):
    xlimit = kwargs.pop('xlimit', None)
    ylimit = kwargs.pop('ylimit', None)
    npoints = kwargs.pop('npoints', 10000)

    @set_up_plot(xlimit, ylimit)
    def inner():
        if xlimit is None:
            points = np.arange(npoints)
        else:
            points = np.linspace(0, xlimit, npoints)
        
        for func in funcs:
            filtered_points = filter(lambda (x, y): y > 0 and y <= ylimit, 
                                     map(lambda x: (x, func(x)), points))
            plt.plot(*zip(*filtered_points), label=func.description())
    return inner

def plot_random_graph(n, p):
    def inner():
        G = nx.fast_gnp_random_graph(n, p, seed=246)
        nx.draw(G, node_color='b')
    return inner

plots = {
    "o-notation-1.svg": plot_funcs(identity(var='n'), linear(2, var='n'),
                                   power(2, var='n'), xlimit=4.5, ylimit=3),
    "o-notation-2.svg": plot_funcs(identity(var='n'), linear(2, var='n'),
                                   power(2, var='n'), xlimit=30, ylimit=20),
    "o-notation-3.svg": plot_funcs(identity(var='n'), linear(2, var='n'),
                                   power(2, var='n'), xlimit=300, ylimit=200),
    "o-notation-4.svg": plot_funcs(identity(var='n'), linear(2, var='n'),
                                   power(2, var='n'), linear(5, var='n'), linear(10, var='n'),
                                   xlimit=1000, ylimit=666),
    "o-notation-5.svg": plot_funcs(power(2, var='n'), power(3, var='n'),
                                   power(4, var='n'), power(10, var='n'), xlimit=15, ylimit=10),
    "o-notation-6.svg": plot_funcs(log(var='n'), logpow(2, var='n'),
                                   logpow(3, var='n'), logpow(5, var='n'), xlimit=30, ylimit=20),
    "o-notation-7.svg": plot_funcs(exp(2, var='n'), exp(var='n'),
                                   exp(3, var='n'), exp(10, var='n'), xlimit=15, ylimit=10),
    "o-notation-8.svg": plot_funcs(nlogn(var='n'), identity(var='n'), xlimit=60, ylimit=40),
    "graphs-1.svg": plot_random_graph(6, 0.6)
}

to_update = ["o-notation-8.svg"]

if __name__ == '__main__':
    if to_update == "all":
        plots_to_update = plots.items()
    elif isinstance(to_update, collections.Iterable):
        plots_to_update = [(i, plots[i]) for i in to_update]
    else:
        plots_to_update = [plot for plot in plots.items() if not os.path.exists(plot[0])]

    for plot in plots_to_update:
        plot[1]()
        plt.legend()
        plt.savefig(plot[0])