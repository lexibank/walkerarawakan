import attr
from pathlib import Path
from collections import defaultdict

from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import Language as BaseLanguage
from pylexibank import FormSpec


@attr.s
class Language(BaseLanguage):
    Full_Name = attr.ib(default=None)
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    Local_ID = attr.ib(default=None)
    Size = attr.ib(default=None)
    Extant = attr.ib(default=None)
    Location = attr.ib(default=None)
    Original_Name = attr.ib(default=None)  # original name in Walker


class Dataset(BaseDataset):
    id = "walkerarawakan"
    dir = Path(__file__).parent
    language_class = Language

    form_spec = FormSpec(
        brackets={"[": "]", "{": "}", "(": ")", "‘": "’"},
        separators=";/,",
        replacements=[(" ", "_")],
        missing_data=("-", "", "-‘u"),
        strip_inside_brackets=True,
    )

    def cmd_download(self, args):
        pass

    def cmd_makecldf(self, args):
        args.writer.add_sources()

        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english), lookup_factory="Name"
        )
        languages = args.writer.add_languages(
            lookup_factory=lambda l: (l['Name'], l['Local_ID']),
        )
        languages_lexemes = {l[0]: languages[l] for l in languages}
        languages_cognates = {l[1]: languages[l] for l in languages}

        # load cognates
        cognates = defaultdict(list)
        
        for f in ['rspb20102579supp3-1.csv', 'rspb20102579supp3-2.csv']:
            for cogid, row in enumerate(self.raw_dir.read_csv(f, dicts=True, delimiter="\t"), 1):
                word = row.pop('id')
                cid = f"{slug(word)}-{cogid}"
                for lang_id, value in row.items():
                    if value in ('?', '0'):
                        continue
                    assert value == '1'  # ensure we don't have unusual states
                    cognates[(word, languages_cognates[lang_id])].append(cid)

        # lexemes
        for row in self.raw_dir.read_csv('Arawakan-lexemes.tsv', dicts=True, delimiter="\t"):
            for col in row:
                if col in ('ID', 'English'):
                    continue
                language = languages_lexemes[col]
                cogid = cognates.get((row['English'], language), [None])[0]
                for lex in args.writer.add_forms_from_value(
                    Language_ID=language,
                    Parameter_ID=concepts.get(row['English']),
                    Value=row[col],
                    Source=['walker2011'],
                    Cognacy=cogid
                    ):
                        args.writer.add_cognate(lexeme=lex, Cognateset_ID=cogid)
