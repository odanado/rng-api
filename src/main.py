import os
import sys
from time import time

VENDOR_PATH = os.environ['VENDOR_PATH']
sys.path.append(VENDOR_PATH)
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import boto3  # NOQA
from gen7_rng import Gen7RNG # NOQA

AWS_S3_BUCKET_NAME = 'pokemon-sfmt-binary-db'
s3 = boto3.resource('s3')


def _search(step, needles):
    start = time()
    encoded_needle = Gen7RNG.encode_needle(needles)
    object_key_name = '{}/{:04X}.bin'.format(step, encoded_needle & 0xFFFF)

    obj = s3.Object(AWS_S3_BUCKET_NAME, object_key_name)
    res = obj.get()
    db = res['Body'].read()
    print(time() - start)

    gen7_rng = Gen7RNG(417)
    results = gen7_rng.search_seed(needles, db)
    print(time() - start)

    return results


def main(event, context):
    needles = event['needle']
    step = event['step']

    return _search(step, needles)


if __name__ == '__main__':
    step = 417
    needles = [15, 1, 13, 13, 1, 2, 3, 15, 2, 13]
    _search(step, needles)
