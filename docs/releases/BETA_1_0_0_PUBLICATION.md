# Beta 1.0.0 publication record

## Author decision, 6 November 2026

The author explicitly authorized building and publishing the first public beta
on GitHub, Modrinth and CurseForge. The full natural Survival playthrough will
use this beta. It is deferred to the public beta phase, not recorded as passed.
Later beta updates will address findings from that playthrough.

The shared version is `1.0.0-beta.1`, tag `v1.0.0-beta.1`. All four target files
use the Beta channel. The former `0.1.0-beta.1` was an unreleased preparation
candidate, not a previous public beta.

The tag workflow builds and tests all four targets and publishes only after its
checks pass. The GitHub release will contain the four JARs and SHA256SUMS.txt.
Source revision, workflow result and platform file IDs will be recorded after
the operations complete. Existing Alpha release assets are not replaced.

## Modrinth eligibility review

The [content rules](https://modrinth.com/legal/rules), checked again on
6 November 2026, sections 6.1 and 6.2 require an AI disclosure and exclude
projects whose content is primarily or entirely AI output or derived from it.
They also exclude page images created or derived from generative AI output.

Available provenance:

- Java sources and asset-generator scripts are present in the repository.
  Development used Codex, including code, generator and documentation changes.
  Commit authors are not a reliable measure of the share of human versus AI work.
- Selected structure exports have pinned hashes and local conversion/generation
  records. This establishes the build inputs, not independent human authorship
  or permission for the referenced visual designs.
- The icon is a deterministic crop of the author's Minecraft screenshot.
  The three gallery images are original shader captures from 1 October 2026.
  This proves capture provenance, not a policy exemption for the assets depicted.
- Visual references are credited to The Archive In Between and Josh White.
  Credits do not establish their permission or endorsement. No reference artwork
  is being newly downloaded or directly packaged for this beta.

The current evidence does not establish eligibility under the restriction on
predominantly AI-derived content. A definitive favorable interpretation requires
Modrinth's assessment. No claim of approval will be made and no public submission
will be sent while that condition remains unresolved. The existing project stays
a draft. A development-disclosure paragraph alone is not the platform's formal
content-disclosure setting and is not sufficient to resolve eligibility.

### Prepared question for Modrinth

Not sent. External contact requires the author's instruction.

> Titan Relics, draft project F6QDr5Vr, uses Codex-assisted Java code,
> programmatic structure-generator scripts and documentation. Its structures are
> generated and voxel-converted locally; their selected inputs are hash-pinned.
> Page images are the author's Minecraft shader captures, with an icon cropped
> from one capture. Those captures depict the generated structures. The visual
> inspirations are credited and the development assistance is disclosed. We
> cannot substantiate a mostly human-authored content share from commit metadata.
> Under sections 6.1 and 6.2, is this project eligible for publication, and do the
> captures count as images derived from generative AI output? Repository and
> source records: https://github.com/Auda29/Titan-Relics.

## CurseForge page access

The documented author API supports file uploads and file metadata, not general
project-page editing. The shared preview browser currently cannot start because
of the host's AppArmor restriction. A separate browser is checked for a usable
author session. Description, MIT, source/issues/wiki links, Colossus icon and
captioned shader images are prepared in the repository for the dashboard.

The author has approved uploading the beta files. Upload responses and moderation
state must be recorded independently of whether the project page can be edited.
No moderation approval or public download is assumed from an accepted upload.
