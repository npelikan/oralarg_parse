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
INTERRUPTION_RE = re.compile("^(QUESTION|(CHIEF )*JUSTICE)")


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
        ir_wordcount = []
        interruption_data = []

        # creates speaker exports
        for speaker in attorney_speakers:

            last_name = re.sub(r"(MR|MS)\. ", "", speaker)

            output_filename = "{path}/{docket_num}_{last_name}.txt".format(
                path=output_dir, docket_num=docket_num, last_name=last_name)

            speaker_corpus = [t for n, t in zip(speaker_order, speaker_texts) if n == speaker]

            with open(output_filename, "w+") as f:
                f.write("\n".join(speaker_corpus))

            interruptions = 0
            interruption_corpus = []
            interruptors = []
            for i in range(len(speaker_order)):
                current_speaker = speaker_order[i]
                try:
                    next_speaker = speaker_order[i + 1]
                    if current_speaker == speaker and re.search(INTERRUPTION_RE, next_speaker):
                        interruptions += 1
                        interruptors.append(next_speaker)
                        interruption_corpus.append(speaker_texts[i + 1])
                except IndexError:
                    pass

            interruptor_data = {}
            for interruptor in set(interruptors):
                si_corpus = [
                    text for speaker, text in zip(interruptors, interruption_corpus) if speaker == interruptor
                ]
                interruptor_data[interruptor] = {
                    "count": len(si_corpus),
                    "word_count": sum(len(re.findall(r'\w+', x)) for x in si_corpus)
                }


            with open("{path}/{docket_num}_{last_name}_interruptions.txt".format(
                path=output_dir, docket_num=docket_num, last_name=last_name), "w+") as f:
                f.write("\n".join(interruption_corpus))

            interrupted_speakers.append(last_name)
            interruptions_count.append(interruptions)
            interruption_data.append(interruptor_data)

            # gets word count of interruptions
            ir_wordcount.append(sum(len(re.findall(r'\w+', x)) for x in interruption_corpus))

        with open("{path}/{docket_num}_interruptions.json".format(
                path=output_dir, docket_num=docket_num), "w+") as f:
            json.dump(
                [
                    {"name": s, "total_count": c, "total_words": w, "interruption_data": i}
                    for s,c,w,i in zip(
                        interrupted_speakers,
                        interruptions_count,
                        ir_wordcount,
                        interruption_data
                    )
                ],
                f)

        print("{docket_num} extracted successfully!".format(docket_num=docket_num))


def main():
    args = docopt.docopt(__doc__)
    input_dir = args['input_dir']
    output_dir = args['output_dir']
    atty_interruptions(input_dir=input_dir, output_dir=output_dir)


if __name__ == "__main__":
    main()










