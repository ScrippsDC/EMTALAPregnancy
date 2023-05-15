import pandas, re

# Stop phrases @cimar methodology for detecting pregnant patients -- this is adding back in some of the generic 
# uses of the word "pregnancy" that @rachgoldaz's methodology removed. But since we're only looking at text nearby
# patient identifiers, we get fewer false positives.
IGNORE_PHRASES_PASS_RC = ["pregnancy test","test for pregnancy","active labor act","active labor (sic) act"]

# Keywords for @cimar methodology for detecting pregnant patients
KEYWORDS_RC = ['gravid','pregnan','eclampsia','caeserian',' c-section',' csection',' c section',' para ','gestation','water break','water broke','active labor','obstetr']

# EMTALA deficiency codes: (2400, 2401, 2402, 2403, 2404, 2405, 2406, 2407, 2408, 2409, 2410, 2411)
EMTALA_RANGE = range(2400,2412)

# The inspection text often has phrases that identify single, anonymous patients. These are the substrings and regex that indicate a patient identifier.
PATIENT_ID_STRS = ["patient #","patient id #", "pt #", "pi #", "(pi) #"]
PATIENT_ID_REGEX = ["patient \\d","patient id \\d","pt \\d", "pi \\d", "(pi) \\d"]

WINDOW_AFTER = 200
WINDOW_BEFORE = 100

q3pt1 = pandas.read_excel("data/source/Hospital_2567s_2022Q3/Hospital 2567s - 2022Q3 Part 1.xlsx")
q3pt2 = pandas.read_excel("data/source/Hospital_2567s_2022Q3/Hospital 2567s - 2022Q3 Part 2.xlsx")

q3 = pandas.concat([q3pt1,q3pt2])

# This function standardizes the text field by lowercasing it and removing the phrases in the ignore_words list
def std_text(insp_text, ignore_words):
    std_text = insp_text.lower()
    for p in ignore_words:
        std_text = std_text.replace(p,"")
    return std_text

def make_key_identifier(row):
    return str(row["deficiency_tag"]).split(".")[0] + " " + str(row["EVENT_ID"])

q3["key_identifier"] = q3.apply(make_key_identifier, axis=1)
q3["std_text_rc"] = q3["inspection_text"].apply(std_text, ignore_words=IGNORE_PHRASES_PASS_RC)

def search_kw(std_text,kw):
    for k in kw:
        if k in std_text:
            return True
    return False

# @cimar's methodology has two steps -- looking at characters near any patient identifiers in the inspection text, and looking at the paragraphs that contain patient identifiers

# This function looks for keywords in the vicinity of patient identifiers (defined as substrings or regex). It returns the first keyword found -- if it finds one. Otherwise it returns None.
def may_be_preg_rc_near_text(text):
    for p in PATIENT_ID_STRS:
        inc = 0
        while True:
            ind = text.find(p,inc)
            if ind < 0:
                break
            start = ind - WINDOW_BEFORE
            end = ind + WINDOW_AFTER
            substr = text[start:end]
            k = search_kw(substr,KEYWORDS_RC)
            for k in KEYWORDS_RC:
                if k in substr:
                    return k
            inc = ind+len(p)
    for r in PATIENT_ID_REGEX:
        inc = 0
        while True:
            contains_regex = re.search(r,text[inc:])
            if not contains_regex:
                break
            ind = contains_regex.span()[0]
            start = ind - WINDOW_BEFORE
            end = ind + WINDOW_AFTER
            substr = text[start:end]
            for k in KEYWORDS_RC:
                if k in substr:
                    return k
            inc += contains_regex.span()[1]
    return None

# This function looks for keywords in the same paragraphs as patient identifiers (defined as substrings or regex). It returns the first keyword found -- if it finds one. Otherwise it returns None.
def may_be_preg_rc_graf(text):
    grafs = text.split("\n")
    for g in grafs:
        for p in PATIENT_ID_STRS:
            if p in g:
                for k in KEYWORDS_RC:
                    if k in g:
                        return k
        for r in PATIENT_ID_REGEX:
            if re.search(r,g):
                for k in KEYWORDS_RC:
                    if k in g:
                        return k
    return None

def is_emtala_deficiency(code):
    if code in EMTALA_RANGE:
        return True
    return False

q3["may_be_pregnant_rc_near_text"] = q3["std_text_rc"].apply(may_be_preg_rc_near_text)
q3["may_be_pregnant_rc_graf"] = q3["std_text_rc"].apply(may_be_preg_rc_graf)

# Passing either part of @cimar's methodology AND having an EMTALA deficiency code flags the case for manual review.
emtala_may_be_preg = q3[((~q3["may_be_pregnant_rc_graf"].isnull())|(~q3["may_be_pregnant_rc_near_text"].isnull()))&(q3["deficiency_tag"].apply(is_emtala_deficiency))]

# Export for manual review -- there are csv encoding issues with the inspection text field, so I'm exporting to Excel.
emtala_may_be_preg.to_excel("data/processed/1_etl_nearby_text_search.xlsx",index=False)

print(emtala_may_be_preg.shape)

