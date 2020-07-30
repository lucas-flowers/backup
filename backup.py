#!/usr/bin/env python3

import sys
import subprocess
from subprocess import CalledProcessError, PIPE
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

def sync(src: Path, dest: Path, outlog: Path, errlog: Path):

    args = [
        'rsync',
        '--archive',
        '--delete',
        '--verbose',
        '--exclude', '/lost+found',
        str(src) + '/', # We're copying src's *children*, not src itself
        str(dest),
    ]

    with open(outlog, 'w') as stdout:
        result = subprocess.run(args, stdout=stdout, stderr=PIPE, text=True)

    if result.stderr:
        errlog.write_text(result.stderr)

def parse_args():

    parser = ArgumentParser(
        description='Use rsync to back up src to dest, while writing logs at the root of src.',
    )

    parser.add_argument(
        'src',
        type=Path,
        help='The source directory',
    ),
    parser.add_argument(
        'dest',
        type=Path,
        help='The directory whose contents should be identical to src',
    )

    return parser.parse_args()

def main():

    args = parse_args()

    prefix = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

    # Keep the logs in the root directory so their (non)existence is clearly
    # visible when browsing src. This is useful when using this script as a
    # cron job: Existence of error logs shows there was a problem, and
    # nonexistence of logs means it wasn't run at all. A poor man's dashboard.
    #
    # Because of how the sync function works, the log for a given invocation
    # won't be fully written to dest until the next invocation. That's not a
    # big deal to me, so I'm not gonna fix it right now.
    #
    sync(
        src=args.src,
        dest=args.dest,
        outlog=args.src/f'{prefix}.log',
        errlog=args.src/f'{prefix}-error.log',
    )

if __name__ == '__main__':
    main()

