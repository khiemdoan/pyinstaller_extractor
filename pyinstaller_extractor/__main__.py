import argparse
import io
import sys
from datetime import datetime
from pathlib import Path

from PyInstaller.archive.readers import CArchiveReader
from uncompyle6 import code_deparse
from xdis import load_module_from_file_object

from pyinstaller_extractor.version import VERSION


class Extractor:

    def __init__(self, path):
        self.path = path

    def extract_to(self, extracted_dir: Path):
        extracted_dir.mkdir(parents=True, exist_ok=True)

        arch = CArchiveReader(self.path)
        pyc_header = self.extract_pyc_header(arch)

        for dpos, dlen, ulen, flag, typcd, nm in arch.toc.data:
            ndx = arch.toc.find(nm)
            x, data = arch.extract(ndx)
            """
            'm': 'PYMODULE',
            's': 'PYSOURCE',
            'b': 'EXTENSION',
            'z': 'PYZ',
            'a': 'PKG',
            'x': 'DATA',
            'b': 'BINARY',
            'Z': 'ZIPFILE',
            'b': 'EXECUTABLE',
            'd': 'DEPENDENCY',
            'o': 'OPTION',
            """
            name = nm
            if typcd in ('s', 'm'):
                name += '.pyc'

            print(name)
            file_path = extracted_dir / name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with (file_path).open('wb+') as fp:
                if typcd == 's':
                    fp.write(pyc_header)
                fp.write(data)

                if typcd in ('s', 'm'):
                    self.extract_source(fp, extracted_dir / (nm + '.py'))

    def extract_pyc_header(self, arch: CArchiveReader) -> bytes:
        ndx = arch.toc.find('pyimod01_os_path')
        x, data = arch.extract(ndx)
        with io.BytesIO(data) as buffer:
            buffer.seek(0)
            float_version, _, _, _, _, _, _ = load_module_from_file_object(buffer)
        if float_version >= 3.7:
            return data[:16]
        if float_version >= 3.3:
            return data[:12]
        return data[:8]

    def extract_source(self, pyc_file, sourcefile):
        pyc_file.seek(0)
        float_version, timestamp, _, co, _, source_size, _ = load_module_from_file_object(pyc_file)
        if float_version >= 3.8:
            return
        
        with open(sourcefile, 'w') as srcfile:            
            srcfile.write(f'# From PyInstaller Extractor {VERSION} by Khiem Doan with love\n')
            if co.co_filename:
                srcfile.writelines(f'# File name: {co.co_filename}\n')
            if timestamp:
                srcfile.writelines(f'# Compiled at: {datetime.fromtimestamp(timestamp)}\n')
            if source_size:
                srcfile.writelines(f'# Size: {source_size} bytes\n')
            srcfile.write('\n')

            code_deparse(co, srcfile, float_version)


if __name__ == '__main__':
    description = f'PyInstaller Extractor {VERSION}'

    parser = argparse.ArgumentParser(prog='python -m pyinstaller_extractor', description='PyInstaller Extractor')
    parser.add_argument(dest='file', type=str, nargs='?', metavar='path_to_file',
                        help='PyInstaller file')
    parser.add_argument('-d', '--dir', dest='dir', type=str, nargs='?', metavar='path_to_directory',
                        help='Directory extracted to')

    args = parser.parse_args()
    filepath = args.file
    extracted_dir = args.dir

    if filepath is None:
        parser.print_help()
        sys.exit(0)

    if extracted_dir is None:
        extracted_dir = Path(filepath + '.extracted')

    extractor = Extractor(filepath)
    extractor.extract_to(extracted_dir)
