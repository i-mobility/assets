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

    icons = set()
    for icon_type in ('icon', 'secondary_icon', 'group_icon'):
        if icon_type == 'icon':
            icon = mapping.get(icon_type, f'icon_transport_{mapping["id"]}')
        else:
            if icon_type not in mapping:
                continue

            icon = mapping[icon_type]

        if isinstance(icon, dict):
            for key, value in icon.items():
                icons.add(value + '.png')

        else:
            icons.add(icon + '.png')

    for i in icons:
        for res in ('mdpi', 'hdpi', 'xhdpi', 'xxhdpi'):
            assert (Path('images') / Path(res) / Path(i)).exists(), f'{i} in {res} does not exist.'

    all_icons.update(icons)

    if 'color' in mapping:
        assert COLOR_PATTERN.search(mapping['color']), f'{mapping["id"]} has invalid color {mapping["color"]}'

print('Checking for stray icons…')
for res in ('mdpi', 'hdpi', 'xhdpi', 'xxhdpi'):
    for entry in (Path('images') / Path(res)).iterdir():
        if entry.name not in all_icons:
            print(f'stray icon {entry.name}')  # entry.unlink()

print('Done!')
