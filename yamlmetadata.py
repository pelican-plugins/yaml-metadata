import logging
import six

try:
    from markdown import Markdown
except ImportError:
    Markdown = False

try:
    import yaml
    try:
        from yaml import CBaseLoader as YamlLoader
    except ImportError:
        from yaml import BaseLoader as YamlLoader
except ImportError:
    yaml = False

from pelican import signals
from pelican.contents import Category, Tag, Author
from pelican.readers import MarkdownReader
from pelican.utils import get_date, pelican_open

logger = logging.getLogger(__name__)

class YAMLMetadataReader(MarkdownReader):
    """Reader for Markdown files with YAML metadata"""

    enabled = bool(Markdown) and bool(yaml)

    def __init__(self, *args, **kwargs):
        super(YAMLMetadataReader, self).__init__(*args, **kwargs)
        # Remove the default markdown metadata extension
        try:
            self.settings['MARKDOWN']['extensions'].remove('markdown.extensions.meta')
        except ValueError:
            logger.warning("'markdown.extensions.meta' extension not enabled. "
                           "Did something change in MarkdownReader.__init__?")

    def read(self, source_path):
        self._source_path = source_path
        self._md = Markdown(**self.settings['MARKDOWN'])

        with pelican_open(source_path) as text:
            content, metadata = self._process_content(text.strip())

        return self._md.convert(content), self._parse_metadata(metadata)

    def _process_content(self, text):
        """Split the YAML metadata from the content and load it into a dict

        Returns a (content_text, metadata_dict) tuple
        """
        if not text or not text.startswith("---\n"):
            logger.debug("No YAML header found in file {0}"
                         "".format(self._source_path))
            return text, {}

        # Find end of YAML block
        lines = text.split("\n")[1:]
        for line_num, line in enumerate(lines):
            if line == "---" or line == "...":
                break

        # Load YAML
        try:
            data = yaml.load("\n".join(lines[:line_num]), YamlLoader)
            if not isinstance(data, dict):
                logger.warning("YAML header wasn't a dict for file {0}"
                               "".format(self._source_path))
                logger.debug("YAML data: {0}".format(data))
                data = {}
        except yaml.parser.ParserError as e:
            logger.error("Error parsing YAML for file {0}: {1}"
                         "".format(self._source_path, e))
            data = {}

        return "\n".join(lines[line_num+1:]), data

    def _to_list(self, obj):
        """Make sure to always return a list"""
        return [obj] if isinstance(obj, six.text_type) else obj

    def _parse_metadata(self, meta):
        """Parse and sanitize metadata"""
        _DEL = object() # Used as a sentinel
        FCNS = {
            'tags': lambda x, y: [Tag(t, y) for t in self._to_list(x)] or _DEL,
            'date': lambda x, y: get_date(x) if x else _DEL,
            'modified': lambda x, y: get_date(x) if x else _DEL,
            'category': lambda x, y: Category(x, y) if x else _DEL,
            'author': lambda x, y: Author(x, y) if x else _DEL,
            'authors': lambda x, y: [Author(a, y) for a in self._to_list(x)]
                                    or _DEL,
            'default': lambda x, y: x
        }

        out = {}
        for k, v in meta.items():
            k = k.lower()
            if k in self.settings['FORMATTED_FIELDS']:
                self._md.reset()
                temp = self._md.convert("\n".join(self._to_list(v)))
            else:
                temp = FCNS.get(k, FCNS["default"])(v, self.settings)

            if temp is not _DEL:
                out[k] = temp
        return out

def add_reader(readers):
    for k in YAMLMetadataReader.file_extensions:
        readers.reader_classes[k] = YAMLMetadataReader

def register():
    signals.readers_init.connect(add_reader)
