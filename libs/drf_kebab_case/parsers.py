from rest_framework import parsers

from .utils import underscoreize


class KebabCaseFormParser(parsers.FormParser):
    def parse(self, stream, media_type=None, parser_context=None):
        data = super(KebabCaseFormParser, self).parse(
            stream, media_type=media_type, parser_context=parser_context)
        return underscoreize(data)


class KebabCaseMultiPartParser(parsers.MultiPartParser):
    def parse(self, stream, media_type=None, parser_context=None):
        data_and_files = super(KebabCaseMultiPartParser, self).parse(
            stream, media_type=media_type, parser_context=parser_context)
        data_and_files.data = underscoreize(data_and_files.data)
        data_and_files.files = underscoreize(data_and_files.files)

        return data_and_files


class KebabCaseJSONParser(parsers.JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        data = super(KebabCaseJSONParser, self).parse(
            stream, media_type=media_type, parser_context=parser_context)

        return underscoreize(data)
