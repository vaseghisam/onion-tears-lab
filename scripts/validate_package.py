"""Preflight article syntax and check its links, citations and headline numbers."""
import csv
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

from export_tk import normalize

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def balanced(text, opening, closing):
    depth = 0
    for char in re.sub(r'\\[{}]', '', text):
        if char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
        if depth < 0:
            return False
    return depth == 0


def article_syntax(text):
    require(text.startswith('THE SERIOUS SCIENCE OF SMALL ANNOYANCES\n\n# '),
            'Missing article title or series line')
    require('```' not in text and '<a ' not in text and '#ref-' not in text,
            'Code wrapper or internal citation markup found')
    require(not re.search(r'</?[A-Za-z][^>]*>', text), 'Raw HTML found')
    require(not re.search(r'^\S[^\n]+\n[=-]{3,}\s*$', text, re.M),
            'Underline-style heading found')
    equation_count = 0
    for line in text.splitlines():
        if '$$' in line:
            require(line.startswith('$$') and line.endswith('$$')
                    and line.count('$$') == 2, 'Multiline or inline display equation')
            maths = [line[2:-2]]
            equation_count += 1
        else:
            require(line.count('$') % 2 == 0, 'Unbalanced inline math delimiter')
            maths = re.findall(r'\$([^$]*)\$', line)
        for equation in maths:
            require(all(balanced(equation, left, right)
                        for left, right in [('{', '}'), ('(', ')'), ('[', ']')]),
                    'Unbalanced equation grouping: ' + equation)
            require(not any(token in equation for token in ['F!\\left', '*{\\delta}', '*{\\varepsilon}']),
                    'Corrupted mathematical markup')
    require(equation_count >= 5, 'Missing expected display equations')
    return equation_count


def main():
    article = (ROOT / 'article.md').read_text(encoding='utf-8')
    export = (ROOT / 'article_tk.md').read_text(encoding='utf-8')
    require(normalize(article) == export, 'TK export differs from the complete article')
    displays = article_syntax(article)
    article_syntax(export)
    body, bibliography = article.split('\n## References\n', 1)
    citations = sorted(set(int(number) for number in re.findall(r'\[(\d+)\]', body)))
    listed = [int(number) for number in re.findall(r'^(\d+)\. ', bibliography, re.M)]
    require(citations == listed == list(range(1, 9)), 'References are missing or nonsequential')
    require(not re.search(r'\[\d+\]\(', body), 'In-text citations must be plain numbers')
    with (ROOT / 'research/reference_crosswalk.csv').open(encoding='utf-8', newline='') as stream:
        crosswalk = list(csv.DictReader(stream))
    require([int(row['article_reference']) for row in crosswalk] == listed,
            'Reference crosswalk differs from article')
    bibtex = (ROOT / 'research/references.bib').read_text(encoding='utf-8')
    for row in crosswalk:
        require(row['url'] in bibliography, 'Missing reference URL ' + row['url'])
        require('{' + row['source_id'] + ',' in bibtex, 'Missing BibTeX reference')

    checked_links = 0
    for path in [ROOT / 'README.md', ROOT / 'article.md', ROOT / 'article_tk.md']:
        for target in re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', path.read_text(encoding='utf-8')):
            if target.startswith(('https://', 'http://', '#')):
                continue
            linked = (path.parent / target).resolve()
            require(linked.is_relative_to(ROOT) and linked.exists(),
                    f'Missing or external local link: {target}')
            checked_links += 1

    summary = json.loads((ROOT / 'results/summary.json').read_text())
    records = {(row['source_id'], row['scenario_id']): row for row in summary['results']}
    table_checks = [('No mean drift', 'no_mean_drift', '.2f'),
                    ('Toward the observation point', 'toward', '.2f'),
                    ('Perpendicular to the source-observer line', 'transverse', '.3f'),
                    ('Away from the observation point', 'away', '.4f')]
    table_meta = json.loads((ROOT / 'assets/table_01_air_motion.json').read_text())
    require(table_meta['source_sha256'] == digest(ROOT / 'results/summary.json'),
            'Exposure table source hash differs from saved summary')
    svg = ET.parse(ROOT / 'assets/table_01_air_motion.svg').getroot()
    svg_text = [''.join(node.itertext()).strip() for node in svg.iter()
                if node.tag.rsplit('}', 1)[-1] == 'text']
    for index, (label, scenario, precision) in enumerate(table_checks):
        expected = format(records['fast', scenario]['exposure_120s_s_per_m3'], precision)
        row = table_meta['rows'][index]
        require(row['scenario_id'] == scenario and row['display_value'] == expected,
                'Exposure table metadata differs from saved result')
        require(expected in svg_text and label.replace('-', '–') in svg_text,
                'Exposure table SVG differs from data or scenario labels')
    for suffix, expected in table_meta['output_sha256'].items():
        require(digest(ROOT / f'assets/table_01_air_motion.{suffix}') == expected,
                'Exposure table rendering differs from recorded version')
    require('](assets/table_01_air_motion.png)' in article, 'Exposure table is not embedded')
    fast = records['fast', 'toward']['peak_concentration_per_m3']
    slow = records['slow', 'toward']['peak_concentration_per_m3']
    ratio = summary['comparison']['toward_slow_to_fast_exposure_120s_ratio']
    require(f'${fast:.2f}$ to ${slow:.2f}' in article, 'Peak concentration prose differs from data')
    require(f'${ratio:.3f}$ times' in article, 'Finite-exposure ratio prose differs from data')
    captured_percent = round(100 * (1 - summary['comparison']['no_mean_drift_fast_tail_fraction_after120s']))
    require(f'about {captured_percent}%' in article, 'Tail qualification differs from data')

    visual_metadata = json.loads((ROOT / 'assets/visual_metadata.json').read_text())
    for relative, expected in visual_metadata['input_files_sha256'].items():
        require(digest(ROOT / relative) == expected, 'Visual metadata has stale input: ' + relative)
    figures = [int(n) for n in re.findall(r'^_Figure (\d+)\.', body, re.M)]
    require(figures == list(range(1, 6)), 'Figure captions are not numbered 1–5 in reading order')
    require(re.findall(r'^_Animation (\d+)\.', body, re.M) == ['1'],
            'Animation numbering differs')
    image_paths = re.findall(r'!\[[^\]\n]*\]\(([^\s)]+)\)', body)
    source_record = json.loads((ROOT / 'assets/asset_sources.json').read_text())
    require(image_paths == [r['path'] for r in source_record['images']],
            'Images differ from the publication asset map')
    require(len(image_paths) == 8 and all(p.startswith('assets/') for p in image_paths),
            'Article images must all be bundled locally')
    for row in source_record['images']:
        if row['origin'].startswith('third-party'):
            require(digest(ROOT / row['path']) == row['sha256'],
                    'Imported image differs from author-supplied source')
    required_assets = ['figure_02_chemistry', 'figure_04_release_exposure',
                       'figure_05_remedies', 'table_01_air_motion', 'animation_01_transport_static']
    for stem in required_assets:
        for suffix in ['.png', '.svg']:
            require((ROOT / 'assets' / (stem + suffix)).stat().st_size > 1000,
                    'Missing or empty figure')
    for suffix in ['.gif', '.mp4']:
        require((ROOT / 'assets' / ('animation_01_transport' + suffix)).stat().st_size > 1000,
                'Missing or empty animation')
    report = {
        'status': 'passed', 'generated_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Local Markdown syntax, file/citation consistency and rounded headline values; not an actual TK import.',
        'article_sha256': digest(ROOT / 'article.md'),
        'tk_export_sha256': digest(ROOT / 'article_tk.md'),
        'reference_count': len(listed), 'display_equation_count': displays,
        'local_links_checked': checked_links, 'headline_values_checked': 8,
        'visual_input_hashes_current': True,
        'figure_numbers': figures, 'animation_numbers': [1],
        'local_article_images': len(image_paths), 'exposure_table_checked_against_saved_data': True,
    }
    (ROOT / 'qa/article_checks.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Article and package preflight passed: eight references, consistent numbers, current visual inputs and local assets.')


if __name__ == '__main__':
    main()
