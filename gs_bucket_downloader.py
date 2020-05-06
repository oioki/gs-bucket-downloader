#!/usr/bin/env python3

import argparse
import pathlib

import requests
from lxml import etree


parser = argparse.ArgumentParser(description='Download contents of Google Cloud Storage bucket via XML API')
parser.add_argument('-u', '--url', required=True, help='HTTP(s) endpoint of public bucket')
parser.add_argument('-o', '--output', default='output', help='Local directory to dump bucket contents')
args = parser.parse_args()

base_url = args.url
output_root_dir = args.output


if base_url.endswith('/'):
    base_url = base_url[:-1]

bucket_name_printed = False


def get_paths_from_url(url):
    # Download and parse XML listing
    r = requests.get(url)
    root = etree.fromstring(r.text.encode('utf-8'))

    # Remove namespace prefixes
    for elem in root.getiterator():
        elem.tag = etree.QName(elem).localname

    # Remove unused namespace declarations
    etree.cleanup_namespaces(root)

    # Print bucket name for the first time
    global bucket_name_printed
    if not bucket_name_printed:
        print('\033[36mGoogle Storage bucket: {}\033[0m'.format(root.find('Name').text))
        bucket_name_printed = True

    # Print URL of current page
    print()
    print('\033[32m{}\033[0m'.format(url))

    next_marker = root.find('NextMarker')
    if next_marker is not None:
        next_marker = next_marker.text

    paths = []
    for child in root.findall('Contents'):
        for subchild in child:
            if subchild.tag == 'Key':
                paths.append(subchild.text)

    return paths, next_marker


def get_all_paths(base_url):
    url = base_url

    while True:
        paths, next_marker = get_paths_from_url(url)

        for path in paths:
            yield path

        if not next_marker:
            return

        url = base_url + '/?marker=' + next_marker


def make_directories_for_path(path):
    """Make directories recursively"""
    global output_root_dir
    path_parts = path.split('/')
    output_dir = '/'.join(path_parts[0:-1])
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)


def download(base_url, path):
    url = '{}/{}'.format(base_url, path)
    print(' ... ' + path, end='', flush=True)

    output_path = output_root_dir + '/' + path
    make_directories_for_path(output_path)

    r = requests.get(url)

    try:
        open(output_path, 'wb').write(r.content)
        print()
    except IsADirectoryError:
        print('    \033[33m[skipped]\033[0m')


if __name__ == "__main__":
    for path in get_all_paths(base_url):
        download(base_url, path)
