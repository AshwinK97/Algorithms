# -*- coding: utf-8 -*-
from time import time

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# Default configuration
contourParams = dict(
    zdir='z',
    alpha=0.5,
    zorder=1,
    antialiased=True,
    cmap=cm.hot
)

surfaceParams = dict(
    rstride=1,
    cstride=1,
    linewidth=1,
    edgecolors='k',
    alpha=0.5,
    antialiased=False,
    cmap=cm.hot
)


class BaseFunction:
    def __init__(self, dim=None, bounds=None, default_bounds=(-10, 10), name=None):
        if bounds is None:
            bounds = [default_bounds]
            if dim is not None:
                bounds = [default_bounds] * dim
        self.dimensions = len(bounds)
        self.bounds = bounds
        self.name = name or self.__class__.__name__

    def __call__(self, *args, **kwargs):
        return self.evaluate(*args, **kwargs)

    def plot2d(self, points=100, figure=None, figsize=(12, 8), contour=True, contour_levels=20,
               imshow_kwds=None, contour_kwds=None):
        if imshow_kwds is None:
            imshow_kwds = dict(cmap=cm.PuRd_r)
        if contour_kwds is None:
            contour_kwds = dict(cmap=cm.PuRd_r)
        xbounds, ybounds = self.bounds[0], self.bounds[1]
        x = np.linspace(min(xbounds), max(xbounds), points)
        y = np.linspace(min(xbounds), max(xbounds), points)
        X, Y = np.meshgrid(x, y)
        Z = self(np.asarray([X, Y]))
        if figure is None:
            fig = plt.figure(figsize=figsize)
        else:
            fig = figure
        ax = fig.gca()
        if contour:
            ax.contourf(X, Y, Z, contour_levels, **contour_kwds)
        else:
            im = ax.imshow(Z, **imshow_kwds)
        if figure is None:
            plt.show()
        return fig, ax

    def plot3d(self, points=100, contour_levels=20, ax3d=None, figsize=(12, 8),
               view_init=None, surface_kwds=None, contour_kwds=None):
        from mpl_toolkits.mplot3d import Axes3D
        contour_settings = dict(contourParams)
        surface_settings = dict(surfaceParams)
        if contour_kwds is not None:
            contour_settings.update(contour_kwds)
        if surface_kwds is not None:
            surface_settings.update(surface_kwds)
        xbounds, ybounds = self.bounds[0], self.bounds[1]
        x = np.linspace(min(xbounds), max(xbounds), points)
        y = np.linspace(min(ybounds), max(ybounds), points)
        X, Y = np.meshgrid(x, y)
        Z = self(np.asarray([X, Y]))
        if ax3d is None:
            fig = plt.figure(figsize=figsize)
            ax = Axes3D(fig)
            if view_init is not None:
                ax.view_init(*view_init)
        else:
            ax = ax3d
        # Make the background transparent
        ax.patch.set_alpha(0.0)
        # Make each axis pane transparent as well
        ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        surf = ax.plot_surface(X, Y, Z, **surface_settings)
        contour_settings['offset'] = np.min(Z)
        cont = ax.contourf(X, Y, Z, contour_levels, **contour_settings)
        if ax3d is None:
            plt.show()
        return ax

    def __repr__(self):
        return '{} {}D'.format(self.name, self.dimensions)

class Ackley(BaseFunction):
  def __init__(self, dim=2, bounds=None, default_bounds=(-10, 10), a=20, b=0.2, c=2 * np.pi):
    super().__init__(dim, bounds, default_bounds)
    self.a = a
    self.b = b
    self.c = c

  def evaluate(self, x):
    d = len(x) 
    s1 = sum(np.power(x, 2))
    s2 = sum(np.cos(2*np.pi*x))
    return -20 * np.exp(-0.2 * np.sqrt(sum(np.power(x, 2))/len(x))) - np.exp(sum(np.cos(2*np.pi*x))/len(x)) + self.a + np.exp(1)

class Rastrigin(BaseFunction):
  def __init__(self, dim=2, bounds=None, default_bounds=(-10, 10), a=10, b=2 * np.pi):
    super().__init__(dim, bounds, default_bounds)
    self.a = a
    self.b = b

  def evaluate(self, x):
    d = len(x)
    s = np.power(x, 2) - self.a * np.cos(self.b * x)
    return (self.a * d) + sum(s)

class Rosenbrock(BaseFunction):
  def __init__(self, dim=2, bounds=None, default_bounds=(-10, 10), a=100):
    super().__init__(dim, bounds, default_bounds)
    self.a = a
  
  def evaluate(self, x):
    return sum(100 * np.power((np.power(x[:-1], 2) - x[1:]), 2) + np.power((x[:-1] - 1), 2))

class HighConditionedElliptic(BaseFunction):
  def __init__(self, dim=2, bounds=None, default_bounds=(-10, 10), a=10 ** 6):
    super().__init__(dim, bounds, default_bounds)
    self.a = a

  def evaluate(self, x):
    d = len(x)
    s = [np.power(self.a, (i)/(d-1)) * (item ** 2) for i, item in enumerate(x)]
    return sum(s)

class BentCigar(BaseFunction):
  def __init__(self, dim=2, bounds=None, default_bounds=(-10, 10), a=10 ** 6):
    super().__init__(dim, bounds, default_bounds)
    self.a = a
  
  def evaluate(self, x):
    s = np.power(x[1:], 2)
    return (x[0] ** 2) + (self.a * sum(s))

class Discus(BaseFunction):
  def __init__(self, dim=2, bounds=None, default_bounds=(-10, 10), a=10 ** 6):
    super().__init__(dim, bounds, default_bounds)
    self.a = a
  
  def evaluate(self, x):
    s = np.power(x[1:], 2)
    return sum(s) + (self.a * (x[0]) ** 2 )

class Weierstrass(BaseFunction):
  def __init__(self, dim=2, bounds=None, default_bounds=(-10, 10), a=2 * np.pi, b=0.5, c=3):
    super().__init__(dim, bounds, default_bounds)
    self.a = a
    self.b = b
    self.c = c
  
  def evaluate(self, x):
    d = len(x)
    s1 = sum(map(lambda k: np.power(self.a, k) * np.cos(self.c * np.power(self.b, k) * (np.array(x) + 0.5)) , range(1, 21)))
    s2 = sum(map(lambda k: np.power(self.a, k) * np.cos(self.c * np.power(self.b, k) * 0.5) , range(1, 21)))

    return sum(s1) - d * s2

class Griewank(BaseFunction):
  def __init__(self, dim=2, bounds=None, default_bounds=(-10, 10), a=1, b=4000):
    super().__init__(dim, bounds, default_bounds)
    self.a = a
    self.b = b

  def evaluate(self, x):
    s = np.power(x, 2) / self.b
    p = [np.cos(item / (i + 1)) + self.a for i, item in enumerate(x)]

    return sum(s) - np.prod(p)

#Returns a inf dataset
class Katsuura(BaseFunction):
  def __init__(self, dim=2, bounds=None, default_bounds=(-10, 10), a=10, b=1):
    super().__init__(dim, bounds, default_bounds)
    self.a = a
    self.b = b 
  
  def evaluate(self, x):
    d = len(x)
    p = [self.b + i * sum(map(lambda j: abs(np.power(2, j) * item - np.round(np.power(2, j) * item)) / np.power(2, j), range(1, 33))) for i, item in enumerate(x)]
    
    return (self.a / d) * np.prod(np.power(p, (self.a / np.power(d, 1.2)))) - (self.a / np.power(d, 2))