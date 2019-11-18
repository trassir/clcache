#!/usr/bin/env python
#
# This file is part of the clcache project.
#
# The contents of this file are subject to the BSD 3-Clause License, the
# full text of which is available in the accompanying LICENSE file at the
# root directory of this project.
#
import os
import argparse
import fnmatch
import pstats

def main():
    stats = pstats.Stats()

    parser = argparse.ArgumentParser()
    parser.add_argument('directory', default=os.getcwd(), nargs='?')
    parser.add_argument('--dump-aggregated', '-da')
    parser.add_argument('--silent', action='store_true')
    parser.add_argument('--perfile', action='store_true')
    args = parser.parse_args()

    for basedir, _, filenames in os.walk(args.directory):
        for filename in filenames:
            if fnmatch.fnmatch(filename, 'clcache-*.prof'):
                path = os.path.join(basedir, filename)
                if not args.silent:
                    print('Reading {}...'.format(path))
                if args.perfile:
                    print(f'{"-"*80}\n{path}:')
                    pstats.Stats(path).sort_stats('cumulative').print_stats()
                else:
                    stats.add(path)


    if not args.perfile:
        stats.strip_dirs()
        if args.dump_aggregated:
            stats.dump_stats(args.dump_aggregated)
        else:
            stats.sort_stats('cumulative')
            stats.print_stats()
            stats.print_callers()

if __name__ == "__main__":
    main()
