import numpy as np
import matplotlib.pyplot as plt
import os.path
import collections

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

def power(pow, var = 'x'):
	return PlotFunction(lambda x: x ** pow, "${}^{{{}}}$".format(var, pow))

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
	npoints = kwargs.pop('npoints', 100)

	@set_up_plot(xlimit, ylimit)
	def inner():
		if xlimit is None:
			points = np.arange(npoints)
		else:
			points = np.linspace(0, xlimit, npoints)
		
		for func in funcs:
			filtered_points = filter(lambda (x, y): True, 
									 map(lambda x: (x, func(x)), points))
			plt.plot(*zip(*filtered_points), label=func.description())
	return inner

plots = {
	"2-plot-1.svg": plot_funcs(identity(var='n'), linear(2, var='n'), power(2, var='n'), xlimit=4.5, ylimit=3),
	"2-plot-2.svg": plot_funcs(identity(var='n'), linear(2, var='n'), power(2, var='n'), xlimit=30, ylimit=20),
	"2-plot-3.svg": plot_funcs(identity(var='n'), linear(2, var='n'), power(2, var='n'), xlimit=300, ylimit=200),
	"2-plot-4.svg": plot_funcs(identity(var='n'), linear(2, var='n'), power(2, var='n'), linear(5, var='n'), linear(10, var='n'), 
							   xlimit=1000, ylimit=666)
}

to_update = "all"

if __name__ == '__main__':
	if to_update == "all":
		plots_to_update = plots.items()
	elif isinstance(to_update, collections.Iterable):
		plots_to_update = [(i, plots[i]) for i in to_update]
	else:
		plots_to_update = [plot for plot in plots.items() if not os.path.exists(plot[0])]

	for plot in plots_to_update:
		plot[1]()
		plt.legend();
		plt.savefig(plot[0], bbox_inches='tight', pad_inches=0)