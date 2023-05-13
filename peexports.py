import sys
import json
from pefile import PE, DIRECTORY_ENTRY
import pickle
import argparse
from glob import glob
from pprint import pprint
from os.path import basename, isfile, isdir
from os import name as os_name
from functools import partial
from multiprocessing import Pool
import logging
from hashlib import sha256

log = logging.getLogger(__name__)

__version__ = '1.0.0'
__author__ = '@c3r3b3ru5d3d53c'

def worker(debug, file_path):
    try:
        if debug is True: print(file_path)
        return {
            'sha256': sha256(open(file_path, 'rb').read()).hexdigest(),
            'library': basename(file_path),
            'exports': get_pe_exports(file_path)
        }
    except Exception as error:
        if debug is True: print(file_path + ' ' + str(error))
        return None

def get_pe_exports(file_path):
    pe = PE(file_path)
    d = [DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT']]
    pe.parse_data_directories(directories=d)
    exports = []
    for export in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if export.name is not None: exports.append(export.name.decode())
    return list(set(exports))
    
def get_dll_files(path, recursive=False):
    if recursive is True: return glob(path + '/**/*.dll', recursive=recursive)
    return glob(path + '*.dll', recursive=recursive)

def write_json(results, file_path, indent=False):
    log.info(file_path)
    if indent is True: open(file_path, 'w').write(json.dumps(results, indent=4))
    else: open(file_path, 'w').write(json.dumps(results))

def write_pickle(results, file_path):
    log.info(file_path)
    pickle.dump(results, open(file_path, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

def setup_logging(file_path, level):
    levels = {
        'debug': logging.DEBUG,
        'error': logging.ERROR,
        'info': logging.INFO
    }
    logging.basicConfig(
        filename=file_path,
        level=levels[level],
        format='[%(levelname)s]\t%(asctime)s\t%(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S%z'
    )

def main():
    parser = argparse.ArgumentParser(
        prog=f'peexports v{__version__}',
        description='A PE Export Collection Utility',
        epilog=f'Author: {__author__}'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'v{__version__}'
    )
    parser.add_argument(
        '-i',
        '--input',
        default=None,
        type=str,
        help='Input Directory or File',
        required=True
    )
    parser.add_argument(
        '-r',
        '--recursive',
        default=False,
        action='store_true',
        help='Search for DLLs Recursively'
    )
    parser.add_argument(
        '-o',
        '--output',
        default=None,
        type=str,
        required=True,
        help='Output File'
    )
    parser.add_argument(
        '-f',
        '--format',
        nargs='?',
        default='json',
        choices=['json', 'pickle'],
        help='Output Format'
    )
    parser.add_argument(
        '-p',
        '--pretty',
        action='store_true',
        default=False,
        help='Indent JSON Output'
    )
    parser.add_argument(
        '-t',
        '--threads',
        default=1,
        type=int,
        required=False,
        help='Threads'
    )
    parser.add_argument(
        '-ll',
        '--log-level',
        default='error',
        choices=['error', 'debug', 'info'],
        required=False,
        help='Logging Level'
    )
    parser.add_argument(
        '-l',
        '--log',
        default=None,
        required=False,
        help='Log File'
    )
    args = parser.parse_args()
    setup_logging(args.log, args.log_level)
    files = []
    if isfile(args.input): files = [args.input]
    elif isdir(args.input): files = get_dll_files(args.input, recursive=args.recursive)
    else: sys.exit(1)
    files = [f for f in files if isfile(f)]
    pool = Pool(processes=args.threads) 
    results = pool.map(partial(worker, args.log_level == 'debug',), files)
    results = list(filter(lambda r: r is not None, results))
    if args.format == 'json': write_json(results, args.output, indent=args.pretty)
    if args.format == 'pickle': write_pickle(results, args.output)
    sys.exit(0)
if __name__ in '__main__':
    main()