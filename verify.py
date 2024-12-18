import re
import sys

from json import load
from pathlib import Path
from collections import defaultdict
from subprocess import check_output

COLOR_PATTERN = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
RESOLUTIONS = ('mdpi', 'hdpi', 'xhdpi', 'xxhdpi')
TRANSPORT_ICON_TYPES = ('icon', 'secondary_icon', 'group_icon', 'indicator')
EXPECTED_SIZES={
    'transport.icon': {
        'mdpi': '24x24', 
        'hdpi': '36x36', 
        'xhdpi': '48x48', 
        'xxhdpi': '72x72'
    },
    'transport.secondary_icon': {
        'mdpi': '15x15', 
        'hdpi': '15x15', 
        'xhdpi': '15x15', 
        'xxhdpi': '15x15'
    },
    'transport.group_icon': {
        'mdpi': '15x15', 
        'hdpi': '15x15', 
        'xhdpi': '15x15', 
        'xxhdpi': '15x15'
    },
    'transport.indicator': {
        'mdpi': '15x15', 
        'hdpi': '15x15', 
        'xhdpi': '15x15', 
        'xxhdpi': '15x15'
    },
    'redeem_code.provider': {
        'mdpi': '15x15', 
        'hdpi': '15x15', 
        'xhdpi': '15x15', 
        'xxhdpi': '15x15'
    }

}

transport_icons = defaultdict(set)
issues = list()

def expect(condition, message):
    if not condition:
        print(f'::error:: {message}')
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
    'identify', '-format', '\'%wx%h\'', path
    ]).decode('utf-8')
    

print(f'Checking icons…')
for type, icons in transport_icons.items():
    all_icons.update(icons)

    for i in icons:
        for res in RESOLUTIONS:
            path = Path('images') / Path(res) / Path(i)

            if not expect(path.exists(), f'{i} in {res} does not exist.'):
                continue

            expected_size=EXPECTED_SIZES[type][res]
            actual_size=get_image_size(path)
            
            expect(actual_size == expected_size, f'Expected {path} to have size {expected_size} got {actual_size}')


print('Checking for stray icons…')
for res in RESOLUTIONS:
    for entry in (Path('images') / Path(res)).iterdir():
        if entry.name not in all_icons:
            print(f'stray icon {entry.name}')  # entry.unlink()


if len(issues) == 0:
    print('All good 👍')
else:
    sys.exit(1)
