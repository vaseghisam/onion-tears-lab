"""Write a fresh manifest and ZIP from the reviewed project files."""
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {'.git', '.venv', '__pycache__', '.pytest_cache', 'reproduction-output'}


def main():
    paths = sorted(path for path in ROOT.rglob('*')
                   if path.is_file()
                   and not EXCLUDED_PARTS.intersection(path.relative_to(ROOT).parts)
                   and path.suffix not in {'.pyc', '.zip'}
                   and path.name not in {'MANIFEST.sha256', '.DS_Store'})
    manifest = ROOT / 'MANIFEST.sha256'
    manifest.write_text(''.join(
        f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ROOT).as_posix()}\n'
        for path in paths), encoding='utf-8')
    paths.append(manifest)
    target = ROOT.parent / 'onion-tears-lab-v1.1.0.zip'
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(paths):
            info = zipfile.ZipInfo('onion-tears-lab/' + path.relative_to(ROOT).as_posix(),
                                  date_time=(2026, 9, 27, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    print(f'Created {target} ({target.stat().st_size:,} bytes; {len(paths)} files)')


if __name__ == '__main__':
    main()
