"""Parse any number of supreme court transcripts.

Usage:
    parse_oralargs <input_dir> <output_dir>

"""
import docopt
import os
import re
import json

from . import OralArgument

# List of possible interruption values
INTERRUPTION_LIST = "QUESTION"


def atty_interruptions(input_dir, output_dir):
    file_list = os.listdir(input_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in file_list:
        oa = OralArgument(
            filename="{path}/{filename}".format(path=input_dir, filename=file)
        )

        speaker_order, speaker_texts = oa.extract_speakers()
        docket_num = oa.casenumber

        # creates list of attorney speakers
        attorney_speakers = [
            x for x in set(speaker_order) if not re.search("^((CHIEF )*JUSTICE|GENERAL|QUESTION|ORAL|REBUTTAL)", x)
        ]

        interrupted_speakers = []
        interruptions_count = []

        # creates speaker exports
        for speaker in attorney_speakers:

            last_name = re.sub(r"(MR|MS)\. ", "", speaker)

            output_filename = "{path}/{docket_num}_{last_name}.txt".format(
                path=output_dir, docket_num=docket_num, last_name=last_name)

            speaker_corpus = [t for n, t in zip(speaker_order, speaker_texts) if n == speaker]

            with open(output_filename, "w+") as f:
                f.writelines(speaker_corpus)

            interruptions = 0
            for i in range(len(speaker_order)):
                current_speaker = speaker_order[i]
                try:
                    next_speaker = speaker_order[i + 1]
                    if current_speaker == speaker and next_speaker in INTERRUPTION_LIST:
                        interruptions += 1
                except IndexError:
                    pass

            interrupted_speakers.append(last_name)
            interruptions_count.append(interruptions)

        with open("{path}/{docket_num}_interruptions.json".format(
                path=output_dir, docket_num=docket_num, last_name=last_name), "w+") as f:
            json.dump(
                dict(zip(interrupted_speakers, interruptions_count)),
                f)

        print("{docket_num} extracted successfully!".format(docket_num=docket_num))


def main():
    args = docopt.docopt(__doc__)
    input_dir = args['input_dir']
    output_dir = args['output_dir']
    atty_interruptions(input_dir=input_dir, output_dir=output_dir)


if __name__ == "__main__":
    main()










