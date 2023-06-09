#!/usr/bin/env python

import contextlib
import copy
import datetime
import logging
import re

from pelican.contents import Author, Category, Tag
from pelican.plugins import signals
from pelican.readers import DUPLICATES_DEFINITIONS_ALLOWED, MarkdownReader
from pelican.utils import get_date, pelican_open

# Only enable this extension if yaml and markdown packages are installed
ENABLED = False
with contextlib.suppress(ImportError):
    from markdown import Markdown
    import yaml

    ENABLED = True


logger = logging.getLogger(__name__)

HEADER_RE = re.compile(
    r"^---$" r"(?P<metadata>.+?)" r"^(?:---|\.\.\.)$" r"(?P<content>.*)",
    re.MULTILINE | re.DOTALL,
)

DUPES_NOT_ALLOWED = set(
    k for k, v in DUPLICATES_DEFINITIONS_ALLOWED.items() if not v
) - {"tags", "authors"}

_DEL = object()

YAML_METADATA_PROCESSORS = {
    "tags": lambda x, y: [Tag(_strip(t), y) for t in _to_list(x)] or _DEL,
    "date": lambda x, y: _parse_date(x),
    "modified": lambda x, y: _parse_date(x),
    "category": lambda x, y: Category(_strip(x), y) if x else _DEL,
    "author": lambda x, y: Author(_strip(x), y) if x else _DEL,
    "authors": lambda x, y: [Author(_strip(a), y) for a in _to_list(x)] or _DEL,
    "slug": lambda x, y: _strip(x) or _DEL,
    "save_as": lambda x, y: _strip(x) or _DEL,
    "status": lambda x, y: _strip(x) or _DEL,
}


def _strip(obj):
    return str(obj if obj is not None else "").strip()


def _to_list(obj):
    """Make object into a list."""
    return [obj] if not isinstance(obj, list) else obj


def _parse_date(obj):
    """Return a string representing a date."""
    # If it's already a date object, make it a string so Pelican can parse it
    # and make sure it has a timezone
    if isinstance(obj, datetime.date):
        obj = obj.isoformat()

    return get_date(str(obj).strip().replace("_", " "))


class YAMLMetadataReader(MarkdownReader):
    """Reader for Markdown files with YAML metadata."""

    enabled = ENABLED

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Don't use default Markdown metadata extension for parsing. Leave self.settings
        # alone in case we have to fall back to normal Markdown parsing.
        self._md_settings = copy.deepcopy(self.settings["MARKDOWN"])
        with contextlib.suppress(KeyError, ValueError):
            self._md_settings["extensions"].remove("markdown.extensions.meta")

    def read(self, source_path):
        """Parse content and YAML metadata of Markdown files."""
        self._source_path = source_path
        self._md = Markdown(**self._md_settings)

        with pelican_open(source_path) as text:
            m = HEADER_RE.fullmatch(text)

        if not m:
            logger.info(
                (
                    "No YAML metadata header found in '%s' - falling back to Markdown"
                    " metadata parsing."
                ),
                source_path,
            )
            return super().read(source_path)

        return (
            self._md.convert(m.group("content")),
            self._load_yaml_metadata(m.group("metadata")),
        )

    def _load_yaml_metadata(self, text):
        """Load Pelican metadata from the specified text."""
        try:
            metadata = yaml.safe_load(text)
            if not isinstance(metadata, dict):
                logger.error(
                    "YAML header didn't parse as a dict for file '%s'",
                    self._source_path,
                )
                logger.debug("YAML data: %r", metadata)
                return {}
        except Exception as e:  # NOQA: BLE001, RUF100
            logger.exception(
                "Error parsing YAML for file '%s': %s: %s",
                self._source_path,
                type(e).__name__,
                e,
            )
            return {}

        return self._parse_yaml_metadata(metadata)

    def _parse_yaml_metadata(self, meta):
        """Parse YAML-provided data into Pelican metadata.

        Based on MarkdownReader._parse_metadata.
        """
        output = {}
        for name, value in meta.items():
            name = name.lower()
            is_list = isinstance(value, list)

            if name in self.settings["FORMATTED_FIELDS"]:
                # join mutliple formatted fields before parsing them as markdown
                self._md.reset()
                value = self._md.convert("\n".join(value) if is_list else str(value))
            elif is_list and len(value) > 1 and name == "author":
                # special case: upconvert multiple "author" values to "authors"
                name = "authors"
            elif is_list and name in DUPES_NOT_ALLOWED:
                if len(value) > 1:
                    logger.warning(
                        "Duplicate definition of `%s` for %s (%s). Using first one.",
                        name,
                        self._source_path,
                        value,
                    )
                value = value[0]

            # Need to do our own metadata processing as YAML loads data in a
            # different way than the markdown metadata extension.
            if name in YAML_METADATA_PROCESSORS:
                value = YAML_METADATA_PROCESSORS[name](value, self.settings)
            if value is not _DEL:
                output[name] = value

        return output


def add_reader(readers):
    for k in YAMLMetadataReader.file_extensions:
        readers.reader_classes[k] = YAMLMetadataReader


def register():
    signals.readers_init.connect(add_reader)
