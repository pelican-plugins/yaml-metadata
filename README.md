pelican-yaml-metadata
=====================

This [Pelican](https://github.com/getpelican/pelican) plugin allows articles written in Markdown to
define their metadata using a [YAML](https://en.wikipedia.org/wiki/YAML) header. This format is
compatible with other popular static site generators like [Jekyll](https://jekyllrb.com/) or
[Hugo](https://gohugo.io/).

It is fully backwards-compatible with the default metadata parsing.

Usage
-----
This plugin aims to keep things simple. After installing and enabling it, any markdown files will
have the option of defining metadata using a YAML header instead of the standard key/value pairs.

In order to specify metadata using YAML, simply enclose it within `---` lines.

Example:
```
---
title: Some title
author: Some person
tags:
  - tag 1
  - tag 2
date: 2014-12-25 00:00
summary: The article summary will be __parsed__ as markdown
---

This is some article text.
```

If the YAML block is not found, the metadata will be parsed using the normal markdown metadata
syntax.

Installation
------------
1. Install using pip (`pip install git+https://github.com/pR0Ps/pelican-yaml-metadata.git`)
2. Enable the plugin in your `pelicanconf.py` by adding `"yaml_metadata"` to the `PLUGINS` list.

License
-------
Licensed under the [MIT license](https://opensource.org/licenses/MIT)
