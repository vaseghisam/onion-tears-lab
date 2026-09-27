"""Regenerate the canonical calculations, visuals, export and executable checks."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only', action='store_true',
                        help='Audit supplied outputs without rebuilding them.')
    args = parser.parse_args()
    if not args.check_only and not shutil.which('ffmpeg'):
        parser.error('Full reproduction requires FFmpeg with libx264 on PATH. '
                     'Use --check-only to audit the supplied results.')
    commands = [] if args.check_only else [
        ['-m', 'src.run_simulations'],
        ['-m', 'src.make_visuals'],
        ['scripts/export_tk.py'],
    ]
    commands += [['tests/run_checks.py'], ['scripts/validate_package.py']]
    start = time.monotonic()
    for command in commands:
        print('\nRunning: python ' + ' '.join(command), flush=True)
        subprocess.run([sys.executable, *command], cwd=ROOT, check=True)
    print(f'\nCompleted in {time.monotonic() - start:.1f} seconds.')


if __name__ == '__main__':
    main()
