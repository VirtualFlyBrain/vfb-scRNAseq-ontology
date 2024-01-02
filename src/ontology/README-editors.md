These notes are for the maintainers of VFB_scRNAseq

This project was created using the [ontology development kit](https://github.com/INCATools/ontology-development-kit). See the site for details.

## Editors Version

** DO NOT MANUALLY EDIT ANY ONTOLOGY FILES ON THIS REPO **

Everything is automatically generated.

## Imports

All import modules are in the [imports/](imports/) folder.

These are automatically generated for each dataset.

## Release Manager notes

These instructions assume you have
[docker](https://www.docker.com/get-docker). This folder has a script
[run.sh](run.sh) that wraps docker commands.

To release:

    `sh run_release.sh`

This adds new ontology and expression files and updates imports for each dataset. Existing ontology (metadata) and expression files are not refreshed by default (would require a lot of memory).

After checking that everything looks good, commit and push changes to github.

IMMEDIATELY AFTERWARDS (do *not* make further modifications) go here:

 * https://github.com/VirtualFlyBrain/vfb-scRNAseq-ontology/releases
 * https://github.com/VirtualFlyBrain/vfb-scRNAseq-ontology/releases/new

__IMPORTANT__: The value of the "Tag version" field MUST be

    vYYYY-MM-DD

where YYYY-MM-DD is the release date.

This cannot be changed after the fact, be sure to get this right!

Release title should be YYYY-MM-DD, optionally followed by a title (e.g. "January release").

Drag and drop release files onto the release page.

Then click "publish release"

__IMPORTANT__: NO MORE THAN ONE RELEASE PER DAY.

Most of the PURLs will not resolve, since VFB takes the ontologies directly from the repo. 
