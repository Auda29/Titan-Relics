"""Shared artifact version; release CI may supply the validated tag version."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
VERSION_PATTERN = r'(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?'


def validate_version(value: str) -> str:
    if not re.fullmatch(VERSION_PATTERN, value):
        raise ValueError('Expected a release version such as 0.1.0-alpha.5.0.3')
    return value


def release_version(default: str | None = None) -> str:
    override = os.environ.get('RELICS_RELEASE_VERSION')
    if override is not None:
        return validate_version(override)
    if default is None:
        default = json.loads((ROOT / 'src/main/resources/fabric.mod.json').read_text(encoding='utf-8'))['version']
    return validate_version(default)


def tag_version(tag: str) -> str:
    # Accept historical target suffixes, while recommending one shared release tag.
    match = re.fullmatch(r'v(' + VERSION_PATTERN + r')(?:\+mc(?:26\.2|1\.21\.1)(?:-neoforge)?)?', tag)
    if match is None:
        raise ValueError('Release tag must be v<VERSION>, optionally with a supported +mc target suffix')
    return validate_version(match.group(1))


if __name__ == '__main__':
    print(release_version())
