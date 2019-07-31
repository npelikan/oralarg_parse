import re
from .regexes import *


class OralArgument:
    def __init__(self, filename):
        """
        Reads in a .txt supreme court transcript file and returns a cleaned list of strings for further analysis

        :param filename: The filename of a supreme court transcript
        """

        with open(filename, "r") as infile:
            self.raw_transcript = infile.read().split("\n\n")

        self.clean_transcript = tuple(map(
            lambda x: x.replace(u"\u00A0", ""),
            self.raw_transcript
        ))

    @property
    def title(self, nlines=5):
        """
        Searches first `nlines` for a title.
        :param nlines: an integer > 0
        """
        searched_lines = [
            x for x in self.clean_transcript[:nlines] if re.search(versus_pattern, x)
        ]

        if any(searched_lines):
            title_working = searched_lines[0].lstrip().replace('\n', ' ')
            title_working = re.sub("\s{1,50}", " ", title_working)
            return re.sub(",", "", title_working)

    @property
    def casenumber(self, nlines=6):
        """
        Searches first `nlines` for a case number.
        :param nlines: an integer > 0
        """
        searched_lines = [
            x for x in self.clean_transcript[:nlines] if re.search(casenum_pattern, x)
        ]

        if any(searched_lines):
            gs = re.sub(r"(No\.|Nos\.|Case|NO\.|Number|Orig\.*|ORIGINAL)", "", searched_lines[0])
            return gs.strip()

    @property
    def citation(self, startline=3, endline=8):
        """
        Searches between `startline` and `endline` for a citation
        :param startline: an integer > 0
        :param endline: an integer > 0
        """
        searched_lines = [
            x for x in self.clean_transcript[startline:endline] if re.search(lexus_cite_pattern, x)
        ]

        if any(searched_lines):
            return searched_lines[0].strip()

    @property
    def date(self, startline=5, endline=9):
        """
        Searches between `startline` and `endline` for a date.
        :param startline: an integer > 0
        :param endline: an integer > 0
        """
        searched_lines = [
            x for x in self.clean_transcript[startline:endline] if re.search(month_pattern, x)
        ]

        if any(searched_lines):
            date = searched_lines[0]
            date = date.lstrip()
            date = re.sub(",", "", date)
            date = date.split()
            return date[0:3]  # this creates a three-element list [month, day, year]

    @property
    def time(self, startline=5, endline=15):
        """
        Searches between `startline` and `endline` for a time.
        :param startline: an integer > 0
        :param endline: an integer > 0
        """
        searched_lines = [
            x for x in self.clean_transcript[startline:endline] if re.search(time_pattern, x)
        ]

        if any(searched_lines):
            return searched_lines[0].replace("(", " ").replace(")", " ")

    def extract_speakers(self):
        ct = self.clean_transcript

        speaker_lines = []
        for i in range(len(ct)):
            x = ct[i]
            if re.search(full_speech_pattern, x):
                speaker_lines.append(x)
            elif not re.search(break_pattern, x):
                if len(speaker_lines) > 0:
                    speaker_lines[len(speaker_lines) - 1] = speaker_lines[len(speaker_lines) - 1] + " " + x

        if any(speaker_lines):
            speakers = tuple(
                re.search(full_speech_pattern, x).group(0).replace(":", "") for x in speaker_lines
            )

            cleaned_lines = tuple(
                re.sub(full_speech_pattern, "", x).replace("\n", " ") for x in speaker_lines
            )

            return speakers, cleaned_lines
        else:
            raise ValueError("No speaker lines found")
