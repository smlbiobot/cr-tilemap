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
from reportlab.lib.units import cm

import yaml
from box import Box


def camelcase_split(s):
    """Split camel case into list of strings"""
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', s)


class App:

    def __init__(self, config_path=None):
        with open(config_path) as f:
            self.config = Box(yaml.load(f))


    def run(self):
        """Run app."""
        for t in self.config.tilemaps:
            self.make_tilemap(t)

    def draw_tile(self, c, x, y):
        w = 1
        h = 1
        s = 0.4 * cm
        c.setLineWidth(0.3)
        c.setStrokeColorRGB(0.2, 0.2, 0.2)
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.rect(x * s, y * s, w * s, h * s, fill=1)

    def make_tilemap(self, config):
        """Generate tilemap from csv to pdf."""

        c = canvas.Canvas(config.pdf, bottomup=0)

        with open(config.csv) as f:
            reader = csv.reader(f)
            y = 0
            for row in reader:
                x = 0
                for col in row:
                    print(col)
                    self.draw_tile(c, x, y)
                    x += 1
                y += 1
        self.draw_tile(c, 1, 1)
        c.showPage()
        c.save()

        if self.config.openfile:
            subprocess.call(['open', config.pdf])


if __name__ == '__main__':
    app = App(config_path='./config.yml')
    app.run()
