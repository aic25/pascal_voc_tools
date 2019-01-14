#!/usr/bin/evn python3
# -*- coding:utf-8 -*-
"""
@File: decodeXml.py
@Author: ternencewang
@Desc: decode xml file of Pascal Voc annotation

"""

import os
import sys

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class XmlReader():
    """Decode the xml file"""
    def __init__(self, xml_file_path, debug=False):
        """
        Arguments:
            xml_file_path: str, the path of a xml file
        """
        self.debug = debug
        self.tree = None
        self.root = None
        self.rewrite = False
        self.file_path = xml_file_path
        self.get_root()

    def get_root(self):
        """get root node of the xml
        """
        self.tree = ET.parse(self.file_path)  #打开xml文档
        self.root = self.tree.getroot()         #获得root节点

    def get_file_name(self):
        """Get file name node information in xml"""
        print("*"*10)
        filename = self.root.find('filename').text
        filename = filename[:-4]
        print(filename)

    def get_width_and_height(self):
        """Get width and height of image in xml"""
        for size in self.root.findall('size'): # 找到root节点下的size节点
            width = size.find('width').text   # 子节点下节点width的值
            height = size.find('height').text   # 子节点下节点height的值
            print(width, height)

    def get_object_list(self):
        """Get all object name and number"""
        obj_list = {}
        for object in self.root.findall('object'):
            name = self.get_object_name(object)
            if name not in obj_list:
                obj_list[name] = 1
            else:
                obj_list[name] += 1
        return obj_list

    def get_object_name(self, object):
        """Get object's name
        Arguments:
            object: object, the the of xml node
        Return:
            name: str, the name of object
        """
        name = object.find('name').text
        # print('Object name is :{}'.format(name))
        return name
    
    def get_object_pose(self, object):
        pose = object.find('pose').text
        return pose

    def get_object_truncated(self, object):
        truncated = object.find('truncated').text
        return truncated

    def get_object_difficult(self, object):
        difficult = object.find('difficult').text
        return difficult

    def set_object_name(self, old_name, new_name):
        """replace old_name to new_name for all object nodes
        Arguments:
            old_name: str, the old class name
            new_name: str, the new class name
        """
        if self.debug:
            print('old_name: {}, new_name: {}'.format(old_name, new_name))
        for object in self.root.findall('object'):
            name = self.get_object_name(object)
            if name == old_name:
                object.find('name').text = new_name
                self.rewrite = True
                if self.debug:
                    print('will replace label name.')
        if self.rewrite is True:
            self.rewrite_xml()
            print('Rerite xml: {}'.format(self.file_path))
        
    def rewrite_xml(self, save_path=None):
        """Save xml file"""
        if save_path is None:
            save_path = self.file_path
        self.tree.write(save_path)
    
    def get_object_bndbox(self, object):
        """Get bbox in object node
        Arguments:
            object: object, the type of xml node
        Return:
            a string list of [xmin, ymin, xmax, ymax]
        """
        bndbox = object.find('bndbox')      #子节点下属性bndbox的值
        xmin = bndbox.find('xmin').text
        ymin = bndbox.find('ymin').text
        xmax = bndbox.find('xmax').text
        ymax = bndbox.find('ymax').text
        return [xmin, ymin, xmax, ymax]

    def set_object_bndbox(self, scale, pad=[0, 0], save_path=None):
        """reset object bndbox using sacle and pad
        Arguments:
            scale: float, the scale chang between original image and new image.
            pad: list of two int, top pad width and left pad width, the down pad is same as the top, the right pad is same as the left.
            save_path: str, the new xml save path, default is rewrite original file.
        """
        for obj in self.root.findall('object'):
            bndbox = obj.find('bndbox')
            bndbox.find('xmin').text = str(round(int(bndbox.find('xmin').text) * scale) + pad[1])  # add left pad
            bndbox.find('ymin').text = str(round(int(bndbox.find('ymin').text) * scale) + pad[0])  # add top pad
            bndbox.find('xmax').text = str(round(int(bndbox.find('xmax').text) * scale) + pad[1])
            bndbox.find('ymax').text = str(round(int(bndbox.find('ymax').text) * scale) + pad[0])
        self.rewrite_xml(save_path)

    def get_all_object_bndbox(self):
        bboxes = []
        for obj in self.root.findall('object'):
            bbox = self.get_object_bndbox(obj)
            bbox = [int(x) for x in bbox]
            bboxes.append(bbox)
    
        return bboxes
        
    def get_all_object(self):
        objects = []
        for obj in self.root.findall('object'):
            bbox = self.get_object_bndbox(obj)
            bbox = [int(x) for x in bbox]
            name = self.get_object_name(obj)
            pose = self.get_object_pose(obj)
            truncated = self.get_object_truncated(obj)
            difficult = self.get_object_difficult(obj)

            objects.append({'name': name, 'bbox': bbox, 'pose': pose, 'truncated': truncated, 'difficult': difficult})

        return objects
