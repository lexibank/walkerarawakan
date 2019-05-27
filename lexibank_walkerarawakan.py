# encoding: utf-8
from __future__ import unicode_literals, print_function
from collections import OrderedDict, defaultdict

import attr
from clldutils.misc import slug
from clldutils.path import Path
from clldutils.text import split_text, strip_brackets
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.dataset import NonSplittingDataset
from pylexibank.dataset import Concept, Language

from tqdm import tqdm

import csv
import lingpy

class Dataset(BaseDataset):
    id = 'walkerarawakan'
    dir = Path(__file__).parent
    concept_class = Concept
    language_class = Language

    def cmd_download(self, **kw):
        # nothing to do, as the raw data is in the repository
        pass

    def cmd_install(self, **kw):
        # read raw lexical data
        raw_data = self.dir.joinpath('raw', 'Arawakan-lexemes.tsv')
        with open(raw_data.as_posix()) as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            raw_entries = [row for row in reader]

        # add information to the dataset
        with self.cldf as ds:
            # add sources
            ds.add_sources(*self.raw.read_bib())

            # add languages
            lang_map = {}
            for language in self.languages:
                lid = slug(language['Name'])
                ds.add_language(
                    ID=lid,
                    Name=language['Name'],
                    Glottolog_Name=language['Glottolog_Name'],
                    Glottocode=language['Glottocode'],
                )
                lang_map[language['Name'].strip()] = lid

            # add concepts
            for concept in self.concepts:
                ds.add_concept(
                    ID=concept['ID'],
                    Name=concept['ENGLISH'],
                    Concepticon_ID=concept['CONCEPTICON_ID'],
                    Concepticon_Gloss=concept['CONCEPTICON_GLOSS'],
                )

            # add lexemes
            for idx, entry in tqdm(enumerate(raw_entries), desc='make-cldf'):
                # Add all entries (columns) except `ID`, which holds the
                # parameter id, and `English`, with a gloss
                entry.pop('English')
                pid = entry.pop('ID')

                for lang, value in entry.items():
                    lang = lang.strip()

                    for form in split_text(value):
                        # skip over empty forms
                        if form in ["-"]:
                            continue

                        # tokenize
                        segments = self.tokenizer(None, '^' + form + '$', column='IPA')

                        # add form
                        for row in ds.add_lexemes(
                            Language_ID=lang_map[lang],
                            Parameter_ID=pid,
                            Value=form,
                            Segments=segments,
                            Source=['walker2011']):
                            pass
