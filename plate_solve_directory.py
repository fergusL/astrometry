#!/usr/bin/python3

import glob, os, sys, time
import argparse
import subprocess

from panoptes.utils.images.fits import get_solve_field

from multiprocessing import Pool
from functools import partial
import tqdm


def solve_field_task(options, fpath):
    """Small wrapper function to run get_solve_field() and ignore any timeouts.

    Args:
        options (dict): dictionary containing one keyword 'solve_opts' which maps
                        to a list of solve-field arguments
        fpath (str): The filepath of the file to be processed by solve-field
    """
    try:
        get_solve_field(fpath, **options)
    except subprocess.TimeoutExpired:
        print(f'solve-field timed out on {fpath}.')
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default="./", help="Directory to search for files for processing.")
    parser.add_argument('--timeout', type=int, default=30, help="The time out length (S) for each solve-field job.")
    parser.add_argument('--downsample', type=int, default=10, hepl="Downsample images by an integer factor, makes processing faster")
    parser.add_argument('--scalelow', type=int, default=1, help="Set minimum scale (deg) for solve-field to look for features.")
    parser.add_argument('--scalehigh', type=int, default=2, help="Set maximum scale (deg) for solve-field to look for features.")
    parser.add_argument('--nproc', type=int, default=1, help="Number of processors to use in multiprocessing.")
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