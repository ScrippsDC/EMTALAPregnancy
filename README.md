# Scripps News Pregnant in the ER Methodological Notes

This repository contains code to reproduce the findings featured in the Scripps News investigation ["'We Don't Deliver Babies Here': Hospitals Turn Away Pregnant Patients"](https://www.scripps.org/news_items/STORY-URL), by Karen Rodriguez, Rachel Gold, Lori Jane Gliha, and Rosie Cima published on June 7, 2023.

The analysis document ([analysis.md]("analysis.md")) contains the code used to produce all the findings in our investigation. We based these findings off ([EMTALA_pregnancy database](data/manual/confirmed_pregnant.xlsx)) -- several hundred EMTALA violations involving pregnant patients. We outline the steps we took to clean, extract, and validate this data in the section below.

## Source Data

Scripps News based this investigation on data Rachel Gold, Scripps News data reporter, obtained through the [Centers for Medicare and Medicaid Services (CMS) Hospitals website](https://www.cms.gov/Medicare/Provider-Enrollment-and-Certification/CertificationandComplianc/Hospitals). The data -- "Full Text Statements of Deficiencies Hospital Surveys" -- is a list of deficiencies in which hospitals have violated CMS Conditions of Participation (CoP), including the Emergency Medical Treatment and Labor Act (EMTALA).

EMTALA enforcement is primarily a complaint-driven system, leaving the burden of reporting violations in the hands of patients and hospital staff. 

At the time of our analysis, the data contained violations from January 1, 2011 to September 30, 2022 from short-term, critical access and psychiatric hospitals in all 50 states. Each violation has an identifier, EVENT_ID, that groups together violations within the same investigation. One investigation (EVENT_ID) may have multiple violations. The dataset labels each violation with a deficiency tag that correlates to the specific CMS Condition of Participation violated within the investigation.

## Data cleaning and extraction

Scripps News reporters used the following steps to clean and extract the data:

* [0_etl_simple_text_search.R](0_etl_simple_text_search.R) -- Our first pass at trying to identify EMTALA violations involving pregnant patients.
* [1_etl_nearby_text_search.py](1_etl_nearby_text_search.py) -- A slightly differnt method of identifying EMTALA violations involving pregnant patients.
* [2_etl_combined.py](2_etl_combined.py) -- Combining the results of the first two methods.
* **Manual review** -- Reporters manually reviewed each captured violation to determine if it did in fact involve a pregnant patient, and then reviewed those for cases of patients being turned away from care. ([EMTALA_pregnancy database](data/manual/confirmed_pregnant.xlsx))
* [3_etl_hospital_summary.R](3_etl_hospital_summary.R) -- Creates a hospital-level (as opposed to violation-level) summary of the data.
* [4_etl_geocode_hosp.py](4_etl_geocode_hosp.py) -- Geocode the hospitals for mapping, for use in graphics.

Scripps News reporters' main goal was to capture any EMTALA violations that involved a pregnant patient. EMTALA violations are catalogued by deficiency tags 2400 through 2411. Reporters filtered the dataset for all violations with EMTALA deficiency tags.

Each violation includes an inspection text, which is a detailed note on the violation. This text can include a patient identifier, their medical complaint(s), a timeline of events, interviews with medical professionals, and policies relating to the violation. Any information personally identifying the patient or medical professional is heavily redacted.

### Simple text search

The code for this step is in [0_etl_simple_text_search.R](0_etl_simple_text_search.R).

Rachel Gold headed up trying to identify violations against pregnant patients, by searching the whole inspection text for certain keywords. This is complicated for two reasons: 

1) A violation's inspection text often includes language _about_ pregnancy, even if the patient themselves was not pregnant. Sometimes a patient would come in with a broken leg, and the inspection text would describe their broken leg, and then go on to quote from a section of EMTALA that mentions pregnant patients.

2) There are a wide variety of descriptors relating to pregnancy or obstetrics. Not every pregnant patient is described as "pregnant" -- sometimes a patient "was in labor" or at a certain number of "weeks gestation," to name just a couple.

Rachel Gold identified 26 specific keywords and phrases ([0_etl_keywords.txt](data/manual/0_etl_keywords.txt)) that were likely to indicate a pregnant patient.

To deal with the problem of false positives, she also identified 29 "stop phrases" ([0_etl_stopphrases.txt](data/manual/0_etl_stopphrases.txt)) that mention those keywords but are unlikely to describe a pregnant patient on their own (e.g. if the only time the word "pregnancy" appears in the inspection text is in the phrase "complaints were not related to pregnancy", we ignore it). This is done by replacing all stop phrases with an empty string before searching the inspection text for keywords.

Fine-tuning these keywords and stop phrases involved a lot of trial and error. Rachel Gold would run the code, manually review a sample of the results, and then add or remove key words and stop phrases as needed.

### Nearby text search

The code for this step is in [1_etl_nearby_text_search.py](1_etl_nearby_text_search.py).

After some manual review of the results returned by the simple text search, data editor Rosie Cima noticed the inspection text field was somewhat structured. Patients were often identified by an alias like "Patient #13", or "Patient Identifier 7", or "PI 4", which was often followed by a description of the patient's complaint, and then a timeline of events.

Rosie wrote some code to do the same kind of keyword search as in the previous step, but _only_ in the text surrounding the patient identifier -- either in the same paragraph as it, or a certain number of characters before or after. Because we were searching a more targeted text field, we were able to use more general key words and phrases ([1_etl_keywords.txt](data/manual/1_etl_keywords.txt) and fewer stop phrases [1_etl_stopphrases.txt](data/manual/1_etl_stopphrases.txt))

### Manual review for pregnant patients and turn-aways
For accuracy, Scripps News reporters manually reviewed _every violation_ captured by the steps above to determine if it actually involved a pregnant patient. After manual review, the resulting [EMTALA_pregnancy database](data/manual/confirmed_pregnant.xlsx) included 683 violations that totaled 417 investigations within 389 hospitals. 

Scripps News Reporters then also manually reviewed every inappropriate transfer (disposition 2409), lack of medical screening exam (2406), and lack of stabilization (2407) violation within our EMTALA pregnancy database. These violations are the most serious because they pose the greatest health risk if violated and can be potentially life-threatening. 

For each of these violations, Scripps News determined whether a pregnant patient was turned away from the emergency department. We defined a patient as "turned away" if the patient sought care and was not able to receive it, like the woman interviewed in our piece, who ended up giving birth in her car on the side of the road. 

Reporters found at least 241 investigations (involving 232 facilities) into instances of of patients being turned away.
