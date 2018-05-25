from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functiosns


class Grid:
    def __init__(self, window, width=4, height=4):
        self.win = window
        self.width = width
        self.height = height
        self.screen_scaling = 1.6
        self.square_width = 0.15
        self.square_height = self.square_width * self.screen_scaling
        self.square_border = 0.01
        self.square_border_x = self.square_border * self.screen_scaling
        self.placement_x = -1.5 * (self.square_width + self.square_border)
        self.placement_y = -1.5 * (self.square_height + self.square_border_x)
        self.squares = [[0 for x in xrange(4)] for x in xrange(4)]
        self.dot_positions_x = [[0 for x in xrange(4)] for x in xrange(4)]
        self.dot_positions_y = [[0 for x in xrange(4)] for x in xrange(4)]
        # Set up pixel coordinates for dot positions:

        self.dot_positions_x[0] = self.placement_x
        self.dot_positions_x[1] = -1 / 2 * \
            (self.square_width + self.square_border_x)
        self.dot_positions_x[2] = 1 / 2 * \
            (self.square_width + self.square_border_x)
        self.dot_positions_x[3] = -self.placement_x
        self.dot_positions_y[0] = -self.placement_y
        self.dot_positions_y[1] = -1 / 2 * \
            (self.square_height + self.square_border)
        self.dot_positions_y[2] = 1 / 2 * \
            (self.square_height + self.square_border)
        self.dot_positions_y[3] = self.placement_y

        self.circle = visual.Polygon(win=self.win,
                                     edges=32,
                                     radius=0.05,
                                     fillColor=[255, 0, 0],
                                     fillColorSpace='rgb255',
                                     size=[1, self.screen_scaling])

        self.probe = visual.Polygon(win=self.win,
                                    edges=32,
                                    radius=0.05,
                                    lineColor=[255, 0, 0],
                                    lineColorSpace='rgb255',
                                    lineWidth=4, size=[1, self.screen_scaling])

        self.setup_squares()

    def setup_squares(self):
        for x in range(4):
            for y in range(4):
                self.square = visual.Rect(win=self.win,
                                          name='matrix1_WM2_training',
                                          width=self.square_width,
                                          height=self.square_height,
                                          ori=0,
                                          pos=[self.placement_x + x *
                                               (self.square_width +
                                                self.square_border),
                                               self.placement_y + y *
                                               (self.square_height +
                                                self.square_border *
                                                self.screen_scaling)],
                                          lineWidth=1,
                                          lineColor=[1, 1, 1],
                                          lineColorSpace=u'rgb',
                                          fillColor=[1, 1, 1],
                                          fillColorSpace=u'rgb',
                                          opacity=1,
                                          interpolate=True)

                self.squares[x][y] = self.square

    def paint_grid(self):
        for x in range(4):
            for y in range(4):
                self.squares[x][y].setAutoDraw(True)
        self.win.flip()

    def hide_grid(self):
        for x in range(4):
            for y in range(4):
                self.squares[x][y].setAutoDraw(False)
        self.win.flip()
    #
    # def paint_dot(self, coordinates):
    #     # get dot coordinates:
    #     dot_coordinates = [self.dot_positions_x[coordinates[0] - 1],
    #                        self.dot_positions_y[coordinates[1] - 1]]
    #     self.circle.setPos(dot_coordinates)
    #
    #     self.circle.setAutoDraw(True)
    #     self.win.flip()
    #
    # def hide_dot(self):
    #     self.circle.setAutoDraw(False)
    #     self.win.flip()
    #
    # def paint_probe(self, coordinates):
    #     # get dot coordinates:
    #     probe_coordinates = [
    #         self.dot_positions_x[coordinates[0] - 1], self.dot_positions_y[coordinates[1] - 1]]
    #     self.probe.setPos(probe_coordinates)
    #
    #     self.probe.setAutoDraw(True)
    #     self.win.flip()
    #
    # def hide_probe(self):
    #     self.probe.setAutoDraw(False)
    #     self.win.flip()
