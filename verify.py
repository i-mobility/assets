import re

from json import load
from pathlib import Path

COLOR_PATTERN = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')

all_icons = set()


with open('definitions.json') as fh:
    defs = load(fh)

for mapping in defs['transport']:
    assert 'id' in mapping, '"id" is required for each transport mapping'
    print(f'Checking transport mapping {mapping["id"]}…')

    icon = mapping.get('icon', f'icon_transport_{mapping["id"]}')
    icons = set()

    if isinstance(icon, dict):
        for key, value in icon.items():
            icons.add(value + '.png')

    else:
        icons.add(icon + '.png')

    if 'secondary_icon' in mapping:
        for key, value in mapping['secondary_icon'].items():
            icons.add(value + '.png')

    if 'group_icon' in mapping:
        icons.add(mapping['group_icon'] + '.png')

    for i in icons:
        for res in ('mdpi', 'hdpi', 'xhdpi', 'xxhdpi'):
            assert (Path('images') / Path(res) / Path(i)).exists(), f'icon {icon} in {res} does not exist.'

    all_icons.update(icons)

    if 'color' in mapping:
        assert COLOR_PATTERN.search(mapping['color']), f'{mapping["id"]} has invalid color {mapping["color"]}'

print('Checking for stray icons…')
for res in ('mdpi', 'hdpi', 'xhdpi', 'xxhdpi'):
    for entry in (Path('images') / Path(res)).iterdir():
        if entry.name not in all_icons:
            entry.unlink()
