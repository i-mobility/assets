# Remote Assets for iMobility Apps

This repository contains icons, colors and other definitions used to remotely
update iMobility apps.

Follow the instructions in the "assets" section here https://imobility.atlassian.net/wiki/spaces/imob/pages/613416961/Partner+Integration+Walkthrough+-+Nov.+2018

For optimal file size run

```bash
find . -iname "*.png" -exec optipng -o7 {} \;
```

from the root directory before pushing new images.

## Releasing

Just merge development branch to master branch - this will invoke 
the jenkins pipeline which will create a release for you

