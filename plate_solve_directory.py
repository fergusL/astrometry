#!/usr/bin/python3

import glob, os, sys, time
import argparse
import subprocess

from panoptes.utils.images.fits import get_solve_field

from multiprocessing import Pool
from functools import partial
import tqdm


def solve_field_task(options, fname):
    try:
        get_solve_field(fname, **options)
    except subprocess.TimeoutExpired:
        print(f'solve-field timed out on {fname}.')
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default="./")
    parser.add_argument('--timeout', type=int, default=30)
    parser.add_argument('--downsample', type=int, default=10)
    parser.add_argument('--scalelow', type=int, default=1)
    parser.add_argument('--scalehigh', type=int, default=2)
    parser.add_argument('--nproc', type=int, default=1)
    args = parser.parse_args()

    fpaths = []
    for dirpath, dirnames, filenames in os.walk(args.path):
        for file in filenames:
            if file.endswith('.fits') or file.endswith('.fits.fz'):
                fpaths.append(os.path.join(dirpath,file))

    print(fpaths)

    options = {'solve_opts': [
        '--guess-scale',
        '--cpulimit', str(args.timeout),
        '--no-verify',
        '--crpix-center',
        '--temp-axy',
        '--index-xyls', 'none',
        '--solved', 'none',
        '--match', 'none',
        '--rdls', 'none',
        '--corr', 'none',
        '--downsample', str(args.downsample),
        '--scale-units', "degwidth",
        '--scale-low', str(args.scalelow),
        '--scale-high', str(args.scalehigh),
        '--no-plots',
        ]
    }

    # print(options)

    # Calculate wcs for files
    print(f"Processing astrometry for {len(fpaths)} files.")
    with Pool(args.nproc) as pool:
        work = partial(solve_field_task, options)
        for _ in tqdm.tqdm(pool.imap_unordered(work, fpaths), total=len(fpaths)):
            pass