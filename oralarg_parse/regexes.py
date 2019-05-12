import re

casenum_pattern=re.compile("\s{5,40}(Case\s){0,1}[N|n][O|o]s{0,1}\.\s|\s{0,40}[N|n]umbers{0,1}\s")
casenum_separator_pattern = re.compile(",|CONSOLIDATED")
versus_pattern=re.compile("[V|v]\.|vs\.")
#casenum_pattern=re.compile("\s{0,40}No\.\s\d\d-\d{1,4}\n|\s{0,40}No\.\s\d{1,2},?\s[Oo]rig(\.|inal)\n|\s{0,40}Number\s\d\d-\d{1,4}\n")
month_pattern = re.compile("\s{0,40}(January|Jan\.|February|Feb\.|March|Mar\.|April|Apr\.|May|June|July|August|Aug\.|September|Sept\.|October|Oct\.|November|Nov\.|December|Dec\.)")
time_pattern = re.compile("(\d{1,2}):([0-5][0-9])")
lexus_cite_pattern = re.compile("U\.S\.\sTrans\.\sLEXIS")

begin_arg_pattern = re.compile("\s{0,4}ORAL\sARGUMENT\sOF\s|\s{0,4}ORAL\sARGUMENT\sBY\s|\s{0,4}REBUTTAL\sARGUMENT\sOF\s|\s{0,4}REBUTTAL\sARGUMENT\sBY\s")
petitioner_pattern = re.compile("PETITIONE[R|RS]|APPELLAN[T|TS]|PLAINTIF[F|FS]")
respondent_pattern = re.compile("RESPONDEN[T|TS]|APPELLE[E|ES]|DEFENDAN[T|TS]")


begin_speech_pattern = re.compile("^(MR\.|(CHIEF )*JUSTICE|MS\.|GENERAL|QUESTION|ORAL|REBUTTAL)")
full_speech_pattern = re.compile("^(MR\.|(CHIEF )*JUSTICE|MS\.|GENERAL|QUESTION|ORAL|REBUTTAL)([A-Z]| )*:")

appearance_pattern=re.compile("^APPEARANCES:")
opinion_pattern=re.compile("^OPINION:")

non_attorney_pattern = re.compile("^((CHIEF )*JUSTICE|GENERAL|QUESTION|ORAL|REBUTTAL)")