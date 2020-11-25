# encoding: utf-8
import attr
from pathlib import Path

from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import Language as BaseLanguage
from pylexibank import FormSpec


@attr.s
class Language(BaseLanguage):
    Full_Name = attr.ib(default=None)
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)


class Dataset(BaseDataset):
    id = 'walkerarawakan'
    dir = Path(__file__).parent
    language_class = Language

    form_spec = FormSpec(
        brackets={"[": "]", "{": "}", "(": ")", "‘": "’"},
        separators=";/,",
        replacements=[(" ", "_")],
        missing_data=('-', '', '-‘u'),
        strip_inside_brackets=True
    )
    
    def cmd_download(self, args):
        pass

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split('-')[-1]+ '_' + slug(c.english),
            lookup_factory="Name"
        )
        
        languages = args.writer.add_languages(
            lookup_factory='Name',
        )
        for row in self.raw_dir.read_csv('Arawakan-lexemes.tsv', dicts=True, delimiter="\t"):
            for col in row:
                if col in ('ID', 'English'):
                    continue

                lex = args.writer.add_forms_from_value(
                    Language_ID=languages[col],
                    Parameter_ID=concepts.get(row['English']),
                    Value=row[col],
                    Source=['walker2011']
                )
