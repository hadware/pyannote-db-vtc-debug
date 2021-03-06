# The MIT License (MIT)

# Copyright (c) 2021 COML

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hadrien TITEUX
import json

from ._version import get_versions

__version__ = get_versions()['version']
del get_versions


from pyannote.core import Annotation, Timeline
from pyannote.database import Database
from pyannote.database.protocol import SpeakerDiarizationProtocol
from pathlib import Path


class PoetryRecitalDiarization(SpeakerDiarizationProtocol):

    ANNOT_FOLDER = Path(__file__).parent / Path("data/annotations")

    def _subset_iter(self, subset):

        annot_folder = self.ANNOT_FOLDER / Path(subset)
        for annot_file in annot_folder.glob("*.json"):
            with open(annot_file) as json_file:
                json_data = json.load(json_file)
            annotation = Annotation.from_json(json_data)
            annotated = Timeline([annotation.get_timeline().extent()])
            current_file = {
                'database': 'VTCDebug',
                'uri': annotation.uri,
                'annotated': annotated,
                'annotation': annotation}

            yield current_file

    def trn_iter(self):
        return self._subset_iter('train')

    def dev_iter(self):
        return self._subset_iter('dev')

    def tst_iter(self):
        return self._subset_iter('test')


class VTCDebug(Database):
    """VTC debugging corpus"""

    def __init__(self, preprocessors={}, **kwargs):
        super().__init__(preprocessors=preprocessors, **kwargs)

        self.register_protocol(
            'SpeakerDiarization', 'PoetryRecitalDiarization', PoetryRecitalDiarization)
