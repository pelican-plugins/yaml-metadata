pelican-yaml-metadata
=====================

This [Pelican](https://github.com/getpelican/pelican) plugin adds a reader for Markdown files with [YAML](https://en.wikipedia.org/wiki/YAML) metadata.
YAML metadata allows for easier specification of more complex metadata, such as nested lists or dictionaries.

Usage
-----
This plugin aims to keep things simple. Install the plugin and `.md`, `.markdown`, `.mkd` and
`.mdown` files will use YAML-formatted data for their metadata.

The files must start with a `---` line, contain some YAML-formatted data, and then end in either another `---`
or `...` line. Anything between the `---` lines will be interpreted as YAML and set as metadata, anything
after is considered content and will be parsed according to the global markdown settings.

Example markdown file:
```
---
title: Some title
author: Some person
tags:
  - tag 1
  - tag 2
date: 2014-12-25 00:00
summary: The article summary will be __parsed__ as markdown!
---

This is the only text in the article.
```

Installation
------------
1. Clone the repo into your Pelican plugin directory
2. Install the plugin requirements (`pip install -r requirements.txt`)
3. Add `'pelican-yaml-metadata'` to the Pelican `PLUGINS` list in `pelicanconf.py`

License
-------
Licensed under the [MIT license](https://opensource.org/licenses/MIT)

