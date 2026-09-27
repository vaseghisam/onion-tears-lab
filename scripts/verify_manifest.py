"""Check the SHA-256 identities of the originally delivered files."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    count = 0
    for line in (ROOT / 'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
        expected, relative = line.split('  ', 1)
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise SystemExit(f'Missing or invalid path: {relative}')
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit(f'Hash differs: {relative}')
        count += 1
    print(f'Manifest verified: {count} files.')


if __name__ == '__main__':
    main()
