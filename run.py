#!/usr/bin/env python
"""
Generate Clash Royale vector arena maps from CSV tilemap.
"""

import csv
import os
import subprocess
import re
import json
from reportlab.pdfgen import canvas
from reportlab.lib.units import pica

import yaml
from box import Box


def camelcase_split(s):
    """Split camel case into list of strings"""
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', s)


class App:

    colors = {
        '-1': (0.9, 0.9, 0.9),
        '0': (0.9, 0.9, 0.9),
        '1': (0.5, 0.9, 0.9),
        '2': (0.9, 0.9, 0.5),
        '16': (0.7, 0.5, 0.5),
        '17': (0.5, 0.7, 0.5),
        '18': (0.5, 0.5, 0.7),
        '32': (0.7, 0.7, 0.7),
        '33': (0.4, 0.9, 0.6),
        '34': (0.4, 0.7, 0.5),
        '48': (0.2, 0.8, 0.8),
        '49': (0.8, 0.2, 0.8),
        '50': (0.3, 0.6, 0.6),
        '64': (0.6, 0.4, 0.6)
    }

    def __init__(self, config_path=None):
        with open(config_path) as f:
            self.config = Box(yaml.load(f))


    def run(self):
        """Run app."""
        for t in self.config.tilemaps:
            self.make_tilemap(t)

    def draw_tile(self, c, x, y, value):
        w = 1
        h = 1
        s = 0.5 * pica
        x0 = 1 * pica
        y0 = 1 * pica
        c.setLineWidth(0.3)
        c.setStrokeColorRGB(0.2, 0.2, 0.2)
        c.setFillColorRGB(*self.colors[value])
        c.rect(x0 + x * s, y0 + y * s, w * s, h * s, fill=1)

    def make_tilemap(self, config):
        """Generate tilemap from csv to pdf."""

        c = canvas.Canvas(config.pdf, bottomup=0)

        with open(config.csv) as f:
            reader = csv.reader(f)
            y = 0
            start = -10000
            for row in reader:
                x = 0
                if row[0] == 'Map':
                    start = -2

                if row[0] == 'Layout':
                    start = -10000

                if start > 0:
                    for value in row:
                        if x > 0:
                            if value == '':
                                value = '-1'
                            self.draw_tile(c, x, start, value)
                        x += 1
                y += 1
                start += 1

        c.showPage()
        c.save()

        if self.config.openfile:
            subprocess.call(['open', config.pdf])


if __name__ == '__main__':
    app = App(config_path='./config.yml')
    app.run()
