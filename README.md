# EMTALA_PREGNANCY

---
title: "cms_hospital_deficiency"
author: "Rachel Gold"
date: '2022-07-12'
contact: "rachel.goldaz@gmail.com""
output: html_document
editor_options: 
  markdown: 
    wrap: 72
---

## Scripps News Pregnant in the ER Methodological Notes

Scripps News based this investigation on data Rachel Gold, Scripps News data reporter, publicly obtained through the Centers for Medicare and Medicaid Services (CMS) Hospitals website. The data is a list of deficiencies in which hospitals have violated CMS Conditions of Participation (CoP), including the Emergency Medical Treatment and Labor Act (EMTALA).

Enforcing EMTALA is primarily a complaint-driven system, leaving the burden of reporting violations in the hands of patients and hospital staff. 

The data contains rows of violations from January 1, 2011 to September 30, 2022 from short-term, critical access and psychiatric hospitals in all 50 states. Each violation has a unique identifier, EVENT_ID, that groups together violations within the same investigation. One investigation (EVENT_ID) may have multiple violations. The dataset labels each violation with a deficiency tag that correlates to the specific CMS Condition of Participation violated within the investigation.

Scripps News reporters limited their analysis to short-term and critical access hospitals (as opposed to psychiatric hospitals) because reporters agreed pregnant patients experiencing medical emergencies were most likely to go to short-term and critical access hospitals for care.

Scripps News reporters' main goal was to capture any EMTALA violations that involved a pregnant patient. EMTALA violations are cataloged by deficiency tags 2400 through 2411. Reporters filtered the dataset for all violations with EMTALA deficiency tags.

Each violation includes an inspection text, a detailed note of the violation. This text tells the story of the patient including a patient identifier, the medical complaint, a timeline of events, interviews with medical professionals and any policies relating to the violation. Any identifying patient or medical professional information was heavily redacted.

##Capturing EMTALA Violations Involving Pregnant Patients

Scripps News reporters realized capturing violations involving a pregnant patient would require three separate keyword searches. The reasons were two-fold:

The inspection text included hospital policies regarding pregnant patients but the patient within the violation was not pregnant. Reporters did not want to capture these violations.

Inspection texts identified a pregnant patient using a variety of descriptors relating to pregnancy or obstetrics.

#Keyword Search

Scripps News reporters found the following key words were more likely to improperly capture violations describing hospital policies for pregnant patients but the patient within the violation was not pregnant. Reporters replaced these key words with blank spaces within the inspection text:

| Phrases                                                                                                                                                                                                                                                                                                                            |
|------------------------------------------------------------------------|
| `A minor who understands the nature and consequences of treatment is capable of consenting if the minor is 18 years of age or older, graduated from high school, has married, has been pregnant, needs diagnosis or treatment of pregnancy or venereal disease, or is 14 years of age or older and requests psychiatric treatment` |
| `A preterm or premature baby is delivered before 37 weeks of the pregnancy`                                                                                                                                                                                                                                                        |
| `An evaluation sufficient to determine if an emergency medical condition or pregnancy with contractions existsAn evaluation sufficient to determine if an emergency medical condition or pregnancy with contractions exists`                                                                                                       |
| `Abdominal pain - any female of childbearing age requiring diagnostic testing to determine pregnancy`                                                                                                                                                                                                                              |
| `abdominal pain, vaginal bleeding`                                                                                                                                                                                                                                                                                                 |
| `citizenship, religion, pregnancy`                                                                                                                                                                                                                                                                                                 |
| `complaint is non-pregnancy related`                                                                                                                                                                                                                                                                                               |
| `complaints were not related to pregnancy`                                                                                                                                                                                                                                                                                         |
| `discussion with prophylaxis against pregnancy`                                                                                                                                                                                                                                                                                    |
| `rug screen, Urine, pregnancy`                                                                                                                                                                                                                                                                                                     |
| `during her pregnancy could be assessed for labor by a labor and delivery nurse except for pregnancy`                                                                                                                                                                                                                              |
| `hospital does not do ultrasounds except for pregnancy`                                                                                                                                                                                                                                                                            |
| `If an emergency medical condition or pregnancy with contractions is present, the hospital must provide such additional medical examination and treatment`                                                                                                                                                                         |
| `In pregnancy at-term, stabilization includes delivery of the child and the placenta`                                                                                                                                                                                                                                              |
| `medical condition, and /or pregnancy within its capabilities`                                                                                                                                                                                                                                                                     |
| `medical screening examinations for patients with pregnancy-related conditions under standardized procedures`                                                                                                                                                                                                                      |
| `no intrauterine pregnancy`                                                                                                                                                                                                                                                                                                        |
| `possible EMCs related to pregnancy`                                                                                                                                                                                                                                                                                               |
| `policy when presenting unscheduled for pregnancy related emergency care`                                                                                                                                                                                                                                                          |
| `pregnancy/active labor`                                                                                                                                                                                                                                                                                                           |
| `pregnancy test`                                                                                                                                                                                                                                                                                                                   |
| `presenting to ED with pregnancy greater than 20 weeks`                                                                                                                                                                                                                                                                            |
| `relates to pregnancy`                                                                                                                                                                                                                                                                                                             |
| `someone in need of emergency care for a psychiatric or pregnancy-relations condition`                                                                                                                                                                                                                                             |
| `treatment based on how far along they were in their pregnancy`                                                                                                                                                                                                                                                                    |
| `urine pregnancy`                                                                                                                                                                                                                                                                                                                  |
| `urine pregnancy test if potential for pregnancy`                                                                                                                                                                                                                                                                                  |
| `urine test for pregnancy`                                                                                                                                                                                                                                                                                                         |
| `Using screen for pregnancy`                                                                                                                                                                                                                                                                                                       |
| `without pregnancy','pregnancy and childbirth`                                                                                                                                                                                                                                                                                     |

Reporters used the following key words to search for and capture any violations involving pregnant patients:

| Phrases                       |
|-------------------------------|
| `currently pregnant`          |
| `gestational age`             |
| `leaking amniotic fluid`      |
| `miscarried`                  |
| `months gestation`            |
| `months pregnant`             |
| `pregnancy`                   |
| `she was pregnant`            |
| `stillborn`                   |
| `water breaking`              |
| `water broke`                 |
| `water had broken`            |
| `was born`                    |
| `was in active labor`         |
| `was in labor`                |
| `was noticeably pregnant`     |
| `was pregnant`                |
| `wks (weeks)`                 |
| `weeks pregnant`              |
| `week pregnant`               |
| `weeks of pregnancy`          |
| `wks (weeks) preg (pregnant)` |
| `weeks gestation`             |
| `weeks' gestation`            |
| `weeks with labor`            |
| `year old pregnant`           |

Reporters captured any violations where the following words appeared 100 characters before or 200 characters after the patient identifier:

| Phrases        |
|----------------|
| `active labor` |
| `c section`    |
| `c-section`    |
| `csection`     |
| `caeserian`    |
| `eclampsia`    |
| `gestation`    |
| `gravid`       |
| `obstetr`      |
| `para`         |
| `pregnan`      |
| `water break`  |
| `water broke`  |

For accuracy, Scripps News reporters manually reviewed each captured violation to determine if it involved a pregnant patient. After manual review, the resulting EMTALA_pregnancy database included 683 violations that totaled 417 investigations within 389 hospitals.

Reporters used the EMTALA_pregnancy database for additional analysis and findings within the investigation.

#Hospitals Turning Away Pregnant Patients

Scripps News Reporters manually reviewed every captured EMTALA violation of inappropriate transfer, lack of medical screening exam and lack of stabilization within our EMTALA pregnancy database. These violations are the most serious because they pose the greatest health risk if violated and can be potentially life-threatening. Scripps News determined whether a pregnant patient was turned away from the emergency department if the patient sought care and was not able to receive it. Reporters found at least 241 investigations of women being turned away.
