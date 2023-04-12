# EMTALA_PREGNANCY

---
title: "cms_hospital_deficiency"
author: "Rachel Gold"
date: '2022-07-12'
output: html_document
editor_options: 
  markdown: 
    wrap: 72
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```
Here is the source link: https://www.cms.gov/Medicare/Provider-Enrollment-and-Certification/CertificationandComplianc/Hospitals

There are 1,326 critical access hospitals with emergency departments.
There are 2,956 Acute Care Hospitals with emergency departments. The rest (1,025 hospitals) are hospitals without emergency departments,
psychiatric hospitals and department of defense hospitals.
<https://data.cms.gov/provider-data/dataset/xubh-q36u>

Keep in mind: many hospitals are private and do not accept Medicaid.
There are 786 hospitals across the US that do not accept Medicaid therefore are not subject to EMTALA.
<https://www.cms.gov/Medicare/Provider-Enrollment-and-Certification/CertificationandComplianc/Hospitals>

The purpose of this markdown is to analyze CMS Hospital Survey Deficiencies for specific reproductive-language words. I will create a database for all the keyword searches.



```{r}
library(tidyverse)
library(dplyr)
library(readxl)
library(stringr)
library(ggplot2)
library(reshape2)
library(raster)
library(writexl)
library(gganimate)
```

We need to import the two datasets into R. These datasets were
downloaded from
<https://www.cms.gov/Medicare/Provider-Enrollment-and-Certification/CertificationandComplianc/Hospitals>

Dataset:Full Text Statements of Deficiencies Hospital Surveys - 2022Q3
(ZIP) - 2 excel files in the zip file.

The two datasets are separated via state. Part 1 is CMS Critical Care
hospital deficiences in all states and SOME CMS Short Term hospitals
(sorted alphabetically by state). Part 2 is CMS Short Term hospital
deficiences and Psychiatric hospitals (sorted alphabetically by state) .

For the purpose of our study, we will be focusing on Critical Access
Care and Short Term Hospitals. Critical Access Care Hospital:
<https://www.cms.gov/Medicare/Provider-Enrollment-and-Certification/CertificationandComplianc/CAHs>

The dataset contains the following columns: facility_name,
hospital_type, facility_id, address, city, state. deficiency_tag,
missing_survey_tag_count, dfcncy_desc, inspection_date, EVENT_ID,
inspection_text.

## Combining the datasets and cleaning

We need to combine part 1 and part 2 so we have one cohesive data table.
We will be using bind_rows function.

Lets upload the datasets.

```{r}
cms_deficiencies1 <- read_xlsx(
"data/source/cms_emtala_violations1.xlsx")

cms_deficiencies2 <- read_xlsx(
"data/source/cms_emtala_violations2.xlsx")

```

Lets combine the datasets.

```{r}
events_all<- bind_rows(cms_deficiencies1, cms_deficiencies2)
```

Since we aren't using data from Psychiatric hospitals, we are going to
get rid of rows in which "Psychiatric" is present.

```{r}
events_crit_short <- 
filter(events_all, hospital_type != "Psychiatric")
```

We want to filter for only emtala deficiencies using the following
emtala deficiency tags:

State Operations Manual Outline of Data Tags Used for Citing Violations
of Responsibilities of Medicare Participating Hospitals in Emergency
Cases. Here are the deficiency tags associated with EMTALA:

A/C-2400 §489.20 Policies and Procedures Which Address AntiDumping
Provisions A/C-2401 §489.20(m) Receiving Hospitals Must Report Suspected
Incidences of Individuals With An Emergency Medical Condition
Transferred in Violation of §489.24(e) 
A/C-2402 §489.20(q) Sign Posting
A/C-2403 §489.24(r) Maintain Transfer Records for Five Years A/C-2404
§489.20(r)(2); §489.24(j) On-Call Physicians 
A/C-2405 §489.20(r)(3) Logs
A/C-2406 §489.24(a); §489.24(c) Appropriate Medical Screening
Examination A/C-2407 §489.24(d)(3) Stabilizing Treatment 
A/C-2408 §489.24(d)(4) and (5) No Delay in Examination or Treatment in Order to Inquire About Payment Status 
A/C-2409 §489.24 (e)(1) and (2) Appropriate Transfer 
A/C-2410 §489.24(e)(3) Whistleblower Protections 
A/C-2411 §489.24(f) Recipient Hospital Responsibilities (Nondiscrimination)

Here are the specific deficiency tags we are looking for:

2400, 2401, 2402, 2403, 2404, 2405, 2406, 2407, 2408, 2408, 2409, 2410,
2411

```{r}
events_crit_short$key_identifier <-
  paste(events_crit_short$deficiency_tag, events_crit_short$EVENT_ID)
```


```{r}
emtala_events_crit_short <- events_crit_short %>%
 filter(grepl('2400|2401|2402|2403|2404|2405|2406|2407|2408|2409|2410|2411', deficiency_tag))

emtala_events_crit_short$index <- 1:nrow(emtala_events_crit_short)

emtala_events_crit_short$year <- format(as.Date(emtala_events_crit_short$inspection_date, format="%Y/%M/%D"),"%Y")
```

When we filter out events in psychiatric hospitalsand emtala deficiency
tags, we are left with 6,477 short term and critical access care
hospital deficiencies since January 2011.

Before we start doing our key word search for compelling cases regarding
pregnant people, many inspection texts cite emtala statutes with the
words relating to pregnant people but the event id will not have to do
with a pregnant patient's records. So we want to delete that string of
words from each inspection text so we can truly search for event ids
relating to pregnant people.


```{r}
emtala_events_crit_short$inspection_text2 <- stringi::stri_replace_all_regex(emtala_events_crit_short$inspection_text,
                                  pattern=c('abdominal pain, vaginal bleeding', 'pregnancy test', 'medical condition, and /or pregnancy within its capabilities', 'medical condition, and/or pregnancy within its capabilities','pregnancy/active labor','hospital does not do ultrasounds except for pregnancy','the hospital does not do ultrasounds except for pregnancy','treatment based on how far along they were in their pregnancy','relates to pregnancy','during her pregnancy could be assessed for labor by a labor and delivery nurse','A preterm or premature baby is delivered before 37 weeks of the pregnancy','medical screening examinations for patients with pregnancy-related conditions under standardized procedures','urine test for pregnancy','urine pregnancy test if potential for pregnancy','except for pregnancy','citizenship, religion, pregnancy','without pregnancy','pregnancy and childbirth','no intrauterine pregnancy','urine pregnancy','Drug screen, Urine, pregnancy','complaints were not related to pregnancy','presenting to ED with pregnancy greater than 20 weeks','complaint is non-pregnancy related','An evaluation sufficient to determine if an emergency medical condition or pregnancy with contractions exists','possible EMCs related to pregnancy','If an emergency medical condition or pregnancy with contractions is present, the hospital must provide such additional medical examination and treatment','A minor who understands the nature and consequences of treatment is capable of consenting if the minor is 18 years of age or older, graduated from high school, has married, has been pregnant, needs diagnosis or treatment of pregnancy or venereal disease, or is 14 years of age or older and requests psychiatric treatment','someone in need of emergency care for a psychiatric or pregnancy-relations condition','discussion with prophylaxis against pregnancy','In pregnancy at-term, stabilization includes delivery of the child and the placenta','Using screen for pregnancy','Abdominal pain - any female of childbearing age requiring diagnostic testing to determine pregnancy','policy when presenting unscheduled for pregnancy related emergency care'),
                                            
                                            
                                          
                                  replacement=c('','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''),vectorize=FALSE)
```

```{r}
emtala_key_word_deficiencies <- emtala_events_crit_short %>% 
  dplyr::select(facility_name, hospital_type, facility_id, address, city, state, deficiency_tag, dfcncy_desc,inspection_date, EVENT_ID, inspection_text, inspection_text2, index, key_identifier, year) %>% 
  dplyr::filter(str_detect(inspection_text2, "weeks pregnant|miscarried|stillborn|water breaking|water broke|weeks gestation|weeks' gestation|weeks with labor|week pregnant|she was pregnant|was pregnant|water had broken|was in labor|was in active labor|was born|was noticeably pregnant|year old pregnant|months pregnant|months gestation|wks (weeks) preg (pregnant)|currently pregnant|weeks of pregnancy|gestational age|leaking amniotic fluid|wks (weeks)|pregnancy"))

```


Lets take a random sample: random sample 20 descriptions with 2406 deficiency code where they don't pass the keyword filter BUT the word "pregnancy" is in them

```{r}
emtala_sample_pregnancy <- emtala_events_crit_short%>%
  dplyr::select(facility_name, hospital_type, facility_id, address, city, state, deficiency_tag, dfcncy_desc,inspection_date, EVENT_ID, inspection_text, inspection_text2) %>% 
  filter(str_detect(inspection_text2, "pregnancy"))
```



```{r}
 sample1 <- sample_n(emtala_sample_pregnancy, 20)  
```

12/20 relate to pregnant people
```{r}
write.csv(sample1, "data/source/sample1.csv")
```

Lets take another random sample: random sample 20 descriptions with 2406 deficiency code where they DO pass the keyword filter -- how many of the 20 are/aren't pregnant people?

```{r}
sample2 <- sample_n(emtala_key_word_deficiencies, 20)  
```

15/20 relate to pregnant people
```{r}
write.csv(sample2, "data/source/sample2.csv")
```

```{r}
sample3 <- sample_n(emtala_key_word_deficiencies, 20)
```
20/20 relate to pregnant people

```{r}
write.csv(sample3, "data/source/sample3.csv")
```

```{r}
sample4 <- sample_n(emtala_key_word_deficiencies, 20)
```

```{r}
write.csv(sample4, "data/source/sample4.csv")
```


Reading in the violations from 2021 (post manual review) that involve pregnancy. 
```{r}
old_key_words <- read_csv("data/source/01092023_copy.csv", show_col_types = FALSE)

old_key_words = subset(old_key_words,select = -c(...17,...18,...19,...20,...21,...22,...23,...24,...25,...26,...27,...28))

old_key_words$key_identifier <-
  paste(old_key_words$deficiency_tag,old_key_words$EVENT_ID)
```

Reading in Rosie's database post manual review - 109 of 169 cases 
```{r}
in_rc <- read_csv("data/source/in_rc_emtala.csv")

in_rc <- in_rc %>%
  dplyr::mutate(across(everything(), as.character))

in_rc$key_identifier <-
  paste(in_rc$deficiency_tag,in_rc$EVENT_ID)

in_rc$inspection_date <- format(as.Date(in_rc$inspection_date, format="%Y/%M/%D"))

```


```{r}
old_new <- emtala_key_word_deficiencies%>%
  inner_join(old_key_words, by = "key_identifier")

old_new <- old_new %>% 
rename_at(vars(ends_with(".x")),
    ~str_replace(., "\\..$","")) %>% 
  select_at(vars(-ends_with(".y")))


#After manual review, I am taking out the cases that do not involve a pregnant person. 
old_new <- old_new %>%
filter(!key_identifier %in% c('2400 ZSG311','2402 ZSG311','2405 ZSG311','2405 X8E611','2405 X8E611','2402 C4HB11','2406 M5D411','2400 MQ7J11','2400 VGG711','2406 VGG711','2402 WEKB11','2406 O33711','2406 0TY011','2407 0TY011','2406 DMLL11','2407 DMLL11'))

old_new$inspection_date <- format(as.Date(old_new$inspection_date, format="%Y/%M/%D"))

old_new<- bind_rows(old_new,in_rc)

old_new$index <- 1:nrow(old_new)
```

```{r}
old_new%>%
  count(facility_name)%>%
  arrange(desc(n))
```




Text: “Even before the fall of Roe, 414 hospitals violated EMTALA when dealing with pregnant patients.” (414 hospitals but one hospital had a violation after the fall of Roe 9/2/2022 TAYLORVILLE MEMORIAL HOSPITAL)

```{r}

n_distinct(old_new$facility_id)

n_distinct(old_new$EVENT_ID)

n_distinct(emtala_events_crit_short$EVENT_ID)

431/2619

700/6477

415/1739

old_new%>%
  count(year)

100/16.456

```

```{r}
old_new_distinct_events <- old_new[!duplicated(old_new$EVENT_ID), ]

old_new_distinct_events$year <- format(as.Date(old_new_distinct_events$inspection_date, format="%Y/%M/%D"),"%Y")

oldnew_keyword_year_count <- old_new_distinct_events %>%
count(year)
```


```{r}
oldnew_def_count <- old_new %>%
  group_by(deficiency_tag)%>%
 count(year, deficiency_tag) 

edc <- dcast(oldnew_def_count, deficiency_tag ~ year) 

edc [is.na(edc)] <- 0

```

```{r}
edc_melt <- melt(edc, id.vars ="deficiency_tag", value.name ="value", variable.name ="year")
```

```{r}
ggplot(data=edc_melt, aes(x=year, y=value, group = deficiency_tag, colour = deficiency_tag)) +
    geom_line() +
    geom_point( size=0, shape=21, fill="white") #+
#facet_wrap(vars(deficiency_tag))+
  #theme_minimal()
```

How many of these distinct events had a 2406 violation? 

```{r}
old_new%>%
  count(deficiency_tag)

```

```{r}
emtala_events_crit_short %>%
  count(deficiency_tag)

old_new %>%
  count(deficiency_tag)

```

```{r}
old_new %>%
  count(state)
```

```{r}
old_new %>%
 count(year)

emtala_events_crit_short %>%
  count(year)
```




