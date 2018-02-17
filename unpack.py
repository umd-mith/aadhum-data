#!/usr/bin/env python

"""
Used to copy data of delivered disks and put into a folder directory
structure.


"""

import os
import shutil


def copy(src, dst):
    for dirpath, dirnames, filenames in os.walk(src):
        for f in filenames:
            if f.endswith('.jpg') or f.endswith('.mp3'):
                path = os.path.join(dirpath, f)
                new_path = os.path.join(dst, *f.split('-'))
                if not os.path.isdir(os.path.dirname(new_path)):
                    os.makedirs(os.path.dirname(new_path))
                if os.path.isfile(new_path): 
                    continue
                print(path, new_path)
                shutil.copyfile(path, new_path)


copy('UMD092/Driskell and Labor shipment 1', 'aadhum')
copy('UMD039/University of Maryland College Park', 'aadhum')
copy('UMD092/Driskell Audio/Streaming/', 'aadhum')
