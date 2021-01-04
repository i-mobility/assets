# Remote Assets for iMobility Apps

This repository contains icons, colors and other definitions used to remotely
update iMobility apps.

Follow the instructions in the "assets" section here https://imobility.atlassian.net/wiki/spaces/imob/pages/613416961/Partner+Integration+Walkthrough+-+Nov.+2018

For optimal file size run

```bash
find . -iname "*.png" -exec optipng -o7 {} \;
```

from the root directory before pushing new images.

## Notes
- For `definitions.json` the order of the `transport` list matters since clients use this order to determine which icon to show for stations.
- Translations that should be pulled into the bundle need to have the `remoteassets` tag added.

## Releasing

Just merge development branch to master branch - this will invoke 
the jenkins pipeline which will create a release for you.

