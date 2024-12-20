import re
import sys
import os
import shutil

from json import load
from pathlib import Path
from collections import defaultdict
from subprocess import check_output

CORRECT = os.getenv("CORRECT_ASSETS", 'False').lower() in ('true', '1', 't')
COLOR_PATTERN = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
RESOLUTIONS = ('mdpi', 'hdpi', 'xhdpi', 'xxhdpi')
TRANSPORT_ICON_TYPES = ('icon', 'secondary_icon', 'group_icon', 'indicator')
EXPECTED_SIZES={
    'transport.icon': {
        'mdpi': '36x36', 
        'hdpi': '54x54', 
        'xhdpi': '72x72', 
        'xxhdpi': '108x108'
    },
    'transport.secondary_icon': {
        'mdpi': '36x36', 
        'hdpi': '54x54', 
        'xhdpi': '72x72', 
        'xxhdpi': '108x108'
    },
    'transport.group_icon': {
        'mdpi': '36x36', 
        'hdpi': '54x54', 
        'xhdpi': '72x72', 
        'xxhdpi': '108x108'
    },
    'transport.indicator': {
        'mdpi': '15x15', 
        'hdpi': '23x23', 
        'xhdpi': '30x30', 
        'xxhdpi': '45x45'
    },
    'redeem_code.provider': {
        'mdpi': '40x40', 
        'hdpi': '60x60', 
        'xhdpi': '80x80', 
        'xxhdpi': '120x120'
    }
}

transport_icons = defaultdict(set)
issues = list()


if CORRECT:
    shutil.copytree('images', 'images_corrected')


def expect(condition, message, path=None):
    if not condition:
        if not path:
            print(f'::error:: {message}')
        else:
            print(f'::error file={path}:: {message}')

        issues.append(message)
    return condition

with open('definitions.json') as fh:
    defs = load(fh)

print(f'Checking definitions.json…')
print(f'Checking transport…')
for mapping in defs['transport']:
    if not expect('id' in mapping, '"id" is required for each transport mapping'):
        continue

    print(f'- {mapping["id"]}')

    for icon_type in TRANSPORT_ICON_TYPES:
        icon = mapping.get(icon_type, dict())
      
        if isinstance(icon, str):
            icon = { 'default': icon }

        if icon_type == 'icon':
            if not 'default' in icon:
                icon['default'] = f'icon_transport_{mapping["id"]}'

        for key, value in icon.items():
            if key == 'indicator':
                transport_icons['transport.indicator'].add(value + '.png')
            else:
                transport_icons['transport.' + icon_type].add(value + '.png')

    if 'color' in mapping:
        expect(COLOR_PATTERN.search(mapping['color']), f'{mapping["id"]} has invalid color {mapping["color"]}')

print(f'Checking redeem_code.sponsors…')
for mapping in defs['redeem_code']['providers']:
    if not expect('id' in mapping, '"id" is required for each provider mapping'):
        continue
    if not expect('icon' in mapping, '"icon" is required for each provider mapping'):
        continue
    print(f'Checking sponsor mapping {mapping["id"]}…')

    transport_icons['redeem_code.provider'].add(mapping['icon'] + '.png' )

    if 'color' in mapping:
        expect(COLOR_PATTERN.search(mapping['color']), f'{mapping["id"]} has invalid color {mapping["color"]}')

all_icons = set()

def get_image_size(path):
    return check_output([
     'magick', 'identify', '-format', '%wx%h', path
    ]).decode('utf-8')
    

print('Checking icons…')
for type, icons in transport_icons.items():
    all_icons.update(icons)

    print(f'- {type}')
    for i in icons:
        for res in RESOLUTIONS:
            path = Path('images') / Path(res) / Path(i)

            if not expect(path.exists(), f'{i} in {res} does not exist.'):
                continue

            expected_size = EXPECTED_SIZES[type][res]
            actual_size = get_image_size(path)
            extra_info = ''

            if actual_size != expected_size:
                for other_res, expected in EXPECTED_SIZES[type].items():
                    if expected == actual_size:
                        extra_info = f', Probably belongs in {other_res}'
                        if CORRECT:
                            destination_path = Path('images_corrected') / Path(other_res) / Path(i)
                            if os.path.exists(destination_path):
                                os.remove(destination_path)
                            shutil.copyfile(path, destination_path)

            expect(actual_size == expected_size, f'Expected {path} to have size {expected_size} got {actual_size}{extra_info}', path = path)
           

print('Checking for stray icons…')
for res in RESOLUTIONS:
    for entry in (Path('images') / Path(res)).iterdir():
        if entry.name not in all_icons:
            print(f'::warning file={entry}::stray icon {entry}')  # entry.unlink()


if len(issues) == 0:
    print('All good 👍')
else:
    sys.exit(1)
