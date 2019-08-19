.. plot_hemispheres:

==================
plot_hemispheres
==================

------------------
Synopsis
------------------
Plots data on the cortical surface (`source code <https://github.com/MICA-MNI/BrainSpace/blob/master/matlab/plot_data/plot_hemispheres.m>`_). 

------------------
Usage
------------------

::

   handles = plot_hemispheres(data,surface);
   handles = plot_hemispheres(data,surface,parcellation);

- *data*: n n-by-1 vector of data to plot where n is the number of vertices or parcels.
- *surface*: a surface readable by :ref:`convert_surface` or a two-element cell array containing left and right hemispheric surfaces in that order. 
- *parcellation*: an m-by-1 vector containing the parcellation scheme, where m is the number of vertices. 
- *handles*: a structure containing the handles of the graphics objects. 

------------------
Description
------------------
Plots any data vector onto cortical surfaces. Data is always provided as a single vector; if two surfaces are provided then the *n* vertices of the first surface will be assigned datapoints 1:*n* and the second surface is assigned the remainder. If a parcellation scheme is provided, data should have as many datapoints as there are parcels.  

BrainSpace only provides basic figure building functionality. For more information on how to use Matlab to create publication-ready figures we recommend delving into `graphics object properties <https://www.mathworks.com/help/matlab/graphics-object-properties.html>`_ (e.g. `figure <https://www.mathworks.com/help/matlab/ref/matlab.ui.figure-properties.html>`_, `axes <https://www.mathworks.com/help/matlab/ref/matlab.graphics.axis.axes-properties.html>`_, `surface <https://www.mathworks.com/help/matlab/ref/matlab.graphics.primitive.surface-properties.html>`_). Also see the `source code <https://github.com/MICA-MNI/BrainSpace/blob/master/matlab/plot_data/plot_hemispheres.m>`_ for basic graphic object property modifications.
