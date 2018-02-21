#!/usr/bin/env python

import os
import re
import csv
import sys
import iiif
import json
import yaml
import hashlib

from glob import glob
from iiif_prezi.factory import ManifestFactory

BASE_URL = "http://aadhum.mith.us"
MANIFEST_BASE = BASE_URL + '/manifests/'
IMAGE_BASE = BASE_URL + '/images/'

def generate(coll):
    metadata = get_metadata()

    mf = ManifestFactory()
    mf.set_base_prezi_uri(MANIFEST_BASE)
    mf.set_base_image_uri(IMAGE_BASE)
    mf.set_iiif_image_info(2.0, 0)

    manifest = None
    seq = None
    page_num = 0

    for folder in glob("data/%s/*" % coll):
        jpegs = glob(folder + "/*.jpg")
        jpegs.sort()
        if len(jpegs) == 0:
            continue

        folder_name = os.path.basename(folder)
        item_id = "%s-%s" % (coll, folder_name)

        folder_metadata = metadata.get(item_id, {})
        title = folder_metadata.get('Title', item_id)
        manifest = mf.manifest(label=title)

        desc = folder_metadata.get('Description/Summary')
        if desc:
            manifest.set_description(desc)

        manifest.set_metadata(folder_metadata)

        seq = manifest.sequence()
        page_num = 0
 
        for jpeg in jpegs:

            image_info = generate_tiles(jpeg)
            if not image_info:
                break


            page_num += 1
            id = BASE_URL + "/%s/%s/%s" % (coll, folder_name, page_num)

            canvas = seq.canvas(
                ident=id + "/canvas",
                label=os.path.basename(jpeg).replace('.jpg', '')
            )
            canvas.thumbnail = get_thumbnail(image_info)

            rel_path = image_info['@id'].replace(IMAGE_BASE, '')

            anno = canvas.annotation(ident=id + "/annotation")
            image = anno.image(ident=rel_path, iiif=True)
            image.height = image_info['height']
            image.width = image_info['width']

            canvas.height = image.height
            canvas.width = image.width

        write_manifest(manifest, coll, item_id)


def id(path):
    m = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            m.update(chunk)
    return m.hexdigest()


def get_image_url(id):
    return "%s/images/%s" % (BASE_URL, id)


def generate_tiles(image_path):
    image_id = id(image_path)
    image_url = get_image_url(image_id)
    local_path = os.path.join(".", "images", image_id)

    if not os.path.isdir(local_path):
        tiles = iiif.static.IIIFStatic(
            src=image_path,
            dst="./images",
            tilesize=1024,
            api_version="2.0"
        )
        print(image_path, image_id)
        tiles.generate(image_path, identifier=image_id)

    info_json = os.path.join(local_path, "info.json")
    info = json.load(open(info_json))
    info['@id'] = image_url
    json.dump(info, open(info_json, "w"), indent=2)
    return info


def write_manifest(manifest, coll, item_id):
    with open("manifests/%s.json" % item_id, "w") as fh:
        fh.write(manifest.toString(compact=False))

    # add the manifest to our index of manifests
    # TODO: make it a iiif:Collection

    index_file = "manifests/%s.json" % coll
    if os.path.isfile(index_file):
        index = json.load(open(index_file))
    else:
        index = []
    index.append({
        "manifestUri": "/manifests/%s.json" % item_id,
        "location": manifest.label
    })
    index.sort(key=lambda m: m['location'], reverse=True)
    json.dump(index, open(index_file, "w"), indent=2)
    print("wrote manifests/%s.json" % item_id)


def get_metadata():
    metadata = {}
    for row in csv.DictReader(open('selection/shipment-01.csv')):
        if 'FilenameRoot' in row and row['FilenameRoot']:
            metadata[row['FilenameRoot']] = row
    return metadata


def get_thumbnail(image_info):
    w = str(image_info["sizes"][0]["width"])
    image_url = image_info["@id"].strip("/")
    return {
        "@id": "%s/full/%s,/0/default.jpg" % (image_url, w),
        "service": {
            "@context": image_info["@context"],
            "@id": image_info["@id"],
            "profile": image_info["profile"]
        }
    }


if __name__ == "__main__":
    coll = sys.argv[1]
    if not os.path.isdir('manifests'):
        os.mkdir('manifests')
    generate(coll)
