import hashlib
import urllib
import zipfile
import requests
from io import BytesIO
from zipfile import ZipFile


def download_and_unzip(u: str):
    url_file = urllib.request.urlopen(u)

    with zipfile.ZipFile(BytesIO(url_file.read())) as my_zip_file:
        my_zip_file.extractall()


def compute_md5(file):
    hasher = hashlib.md5()
    with open(file, 'rb') as input:
        buf = input.read()
        hasher.update(buf)

    return hasher.hexdigest()


def local_path(url):
    filename_with_args = url.split('/')[-1]
    filename = filename_with_args.split('?')[0]
    return filename

def download_file(url):
    local_filename = local_path(url)
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for i, chunk in enumerate(r.iter_content(chunk_size=8192), 1):
                if chunk:  # filter out keep-alive new chunks
                    print(".", end="")
                    if i % 80 == 0:
                        print("")
                    f.write(chunk)
                    # f.flush()
            if i % 80 != 0:
                print("")
    return local_filename


def extract_zip_file(filepath):
    zfile = zipfile.ZipFile(filepath)
    files = []
    for finfo in zfile.namelist():
        with zfile.open(finfo, "r") as input:
            with open(finfo, "w") as output:
                for i in input:
                    output.write(i.decode("utf-8"))
        files.append(finfo)

    return files
