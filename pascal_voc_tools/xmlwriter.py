#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@File: xmlwriter.py
@Time: 2019-01-14
@Author: ternencewang
@Direc: write a xml file about pascal voc annotation.
"""
import os
from jinja2 import Environment, PackageLoader


class XmlWriter():
    """Write a xml file about pascal voc annotation."""
    def __init__(self, path, width, height, depth=3, database='Unknown', segmented=0):
        """Generate a xml file
        Arguments:
            path: str, arg in xml about image.
            width: int or str, image width.
            height: int or str, image height.
            depth: int or str, image channle.
            database: str, default='Unknown'.
            segmented: int or str, default=0.
        """
        environment = Environment(loader=PackageLoader('pascal_voc_tools', 'templates'), keep_trailing_newline=True)
        self.annotation_template = environment.get_template('annotation.xml')

        abspath = os.path.abspath(path)

        self.template_parameters = {
            'path': abspath,
            'filename': os.path.basename(abspath),
            'folder': os.path.basename(os.path.dirname(abspath)),
            'width': width,
            'height': height,
            'depth': depth,
            'database': database,
            'segmented': segmented,
            'objects': []
        }

    def add_object(self, name, xmin, ymin, xmax, ymax, pose='Unspecified', truncated=0, difficult=0):
        """add an object info
        Arguments:
            name: str, class name.
            xmin: int, left.
            ymin: int, top.
            xmax: int, right.
            ymax: int, bottom.
            pose: str, default is 'Unspecified'.
            truncated: str, default is 0.
            difficult: int, default is 0.
        """
        self.template_parameters['objects'].append({
            'name': name,
            'xmin': xmin,
            'ymin': ymin,
            'xmax': xmax,
            'ymax': ymax,
            'pose': pose,
            'truncated': truncated,
            'difficult': difficult,
        })

    def save(self, annotation_path):
        """Write a xml file to save info.
        Arguments:
            annotation_path: str, the path of xml to save.
        """
        with open(annotation_path, 'w') as xml_file:
            content = self.annotation_template.render(**self.template_parameters)
            xml_file.write(content)
