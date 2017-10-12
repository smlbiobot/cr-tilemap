!#/usr/bin/env python
"""
Generate Clash Royale vector arena maps from CSV tilemap.
"""

import csv
import os
import re
import json

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
        self.make_tilemap()

    def make_tilemap(self):
        """Generate tilemap from csv to pdf."""




if __name__ == '__main__':
    app = App(config_path='./config.yml')
    app.run()
