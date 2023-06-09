Pelican YAML Metadata
=====================

[![Build Status](https://img.shields.io/github/actions/workflow/status/pelican-plugins/yaml-metadata/main.yml?branch=main)](https://github.com/pelican-plugins/yaml-metadata/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-yaml-metadata)](https://pypi.org/project/pelican-yaml-metadata/)
![License](https://img.shields.io/pypi/l/pelican-yaml-metadata?color=blue)

This [Pelican](https://github.com/getpelican/pelican) plugin allows articles written in Markdown to
define their metadata using a [YAML](https://en.wikipedia.org/wiki/YAML) header. This format is
compatible with other popular static site generators like [Jekyll](https://jekyllrb.com/) or
[Hugo](https://gohugo.io/).

It is fully backwards-compatible with the default metadata parsing.

Installation
------------
This plugin can be installed via:

    python -m pip install pelican-yaml-metadata

As long as you have not explicitly added a `PLUGINS` setting to your Pelican settings file, then the newly-installed plugin should be automatically detected and enabled. Otherwise, you must add `yaml_metadata` to your existing `PLUGINS` list. For more information, please see the [How to Use Plugins](https://docs.getpelican.com/en/latest/plugins.html#how-to-use-plugins) documentation.

Usage
-----
This plugin aims to keep things simple. After installing and enabling it, any Markdown files will
have the option of defining metadata using a YAML header instead of the standard key/value pairs.

In order to specify metadata using YAML, enclose it within `---` lines.

Example:
```yaml
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

If the YAML block is not found, the metadata will be parsed using the normal Markdown metadata
syntax.

Contributing
------------
Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/yaml-metadata/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

License
-------
This project is licensed under the [MIT license](https://opensource.org/licenses/MIT).
