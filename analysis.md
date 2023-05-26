cms_hospital_deficiency
================
Rachel Gold
2022-07-12

## R Markdown

The purpose of this markdown is to analyze CMS Hospital Survey
Deficiencies that we’ve already filtered down to EMTALA violations
involving pregnant patients.

``` r
library(readxl)
library(dplyr)
```

    ## 
    ## Attaching package: 'dplyr'

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

``` r
library(stringr)
library(writexl)
library(readr)
```

## Data

Reading in violations from 2011-Q3 2022 that we automatically filtered
by features of the inspection_text field (0_etl, 1_etl, and 2_etl).
These were then manually reviewed by Rachel Gold and Karen Rodriguez for
whether they, in fact, pertained to pregnant patients.

``` r
emtala_pregnant <- read_xlsx("data/manual/confirmed_pregnant.xlsx")
emtala_all <- read_xlsx("data/processed/0_etl_all_emtala_deficiencies.xlsx")
```

## Hospital counts, features

Web: “Our investigation found 389 hospitals spanning 44 states have
violated EMTALA statutes while attending to pregnant patients, racking
up at least 675 federal violations since 2011.”

Script: “OUR SCRIPPS NEWS INVESTIGATION FOUND IT IS AMONG 389 HOSPITALS
(FC) AROUND THE COUNTRY REPONSIBLE FOR NEARLY 700 VIOLATIONS OF THE
EMERGENCY MEDICAL TREATMENT AND LABOR ACT – OR EMTALA”

## Violation count

Web: “racking up at least 675 federal violations since 2011.”

``` r
facility_count<-n_distinct(emtala_pregnant$facility_id)

violation_count<-n_distinct(emtala_pregnant$key_identifier)

state_count<-n_distinct(emtala_pregnant$state)

print(paste("facility_count:",facility_count,"violation_count:",violation_count,"state_count:",state_count))
```

    ## [1] "facility_count: 389 violation_count: 683 state_count: 44"

``` r
emtala_pregnant%>%
  count(state,sort=TRUE)
```

    ## # A tibble: 44 × 2
    ##    state     n
    ##    <chr> <int>
    ##  1 CA       66
    ##  2 TN       46
    ##  3 NC       45
    ##  4 NY       43
    ##  5 FL       41
    ##  6 GA       34
    ##  7 PA       33
    ##  8 OR       29
    ##  9 AL       27
    ## 10 TX       26
    ## # ℹ 34 more rows

## Date range

Script:“…ALL INVOLVING PREGNANCY EMERGENCIES BETWEEN 2011 AND 2022.”

``` r
emtala_pregnant%>%
  count(year)
```

    ## # A tibble: 12 × 2
    ##     year     n
    ##    <dbl> <int>
    ##  1  2011    77
    ##  2  2012    43
    ##  3  2013    51
    ##  4  2014    72
    ##  5  2015    81
    ##  6  2016    53
    ##  7  2017    91
    ##  8  2018    69
    ##  9  2019    64
    ## 10  2020    25
    ## 11  2021    40
    ## 12  2022    17

## Percentage of EMTALA overall

Web: “Cases involving pregnant women made up about 15% of all EMTALA
investigations.”

``` r
#number of EMTALA pregnant patient investigations since 2011
count_preg<-n_distinct(emtala_pregnant$EVENT_ID)

#number of EMTALA investigations overall since 2011
count_invest<-n_distinct(emtala_all$EVENT_ID)

#percent of EMTALA investigations involving a pregnant patient since 2011 
print(paste(count_preg,"investigations of violations against pregnant patients, out of",count_invest,"investigations of overall. (",count_preg/count_invest*100,"%)"))
```

    ## [1] "417 investigations of violations against pregnant patients, out of 2694 investigations of overall. ( 15.4788418708241 %)"

## EMTALA violation ranking

Web: “We found the most common EMTALA violation was “failure to provide
medical screening examinations.” (medical screening exam = 2406)

``` r
emtala_pregnant %>%
  count(deficiency_tag,sort=TRUE)
```

    ## # A tibble: 11 × 2
    ##    deficiency_tag     n
    ##             <dbl> <int>
    ##  1           2406   262
    ##  2           2409   122
    ##  3           2405    87
    ##  4           2407    83
    ##  5           2400    77
    ##  6           2408    15
    ##  7           2411    12
    ##  8           2402     9
    ##  9           2404     9
    ## 10           2403     4
    ## 11           2401     3

``` r
# filter emtala_pregnant for deficiency tag == 2406
count_all_preg <- n_distinct(emtala_pregnant$key_identifier)
count_2406 <- n_distinct((emtala_pregnant %>% filter(deficiency_tag == 2406))$key_identifier)

print(paste(count_2406,"medical screening violations against pregnant patients, out of",count_all_preg,"violations against pregnant patients of overall. (",count_2406/count_all_preg*100,"%)"))
```

    ## [1] "262 medical screening violations against pregnant patients, out of 683 violations against pregnant patients of overall. ( 38.3601756954612 %)"

## Turnaway count

Rachel Gold and Karen Rodriguez also manually reviewed the EMTALA
violations for whether the pregnant patient was actually turned away by
the hospital.

Web: “Our investigation found of the cases that were investigated by
CMS, at least 241 involved pregnant women going to the ER for care and
being turned away.”

``` r
# I added "turnaway" as a column in confirmed_pregnant.xlsx
turnaway <- emtala_pregnant %>% filter(turnaway == TRUE)
n_distinct(turnaway$EVENT_ID)
```

    ## [1] 241

## Rural vs. urban

Web: “EMTALA violations involving pregnancy \[…\] included small
hospitals and large ones, in both rural and urban areas.”

``` r
emtala_facilities <- read.csv("data/processed/facility_summary.csv")
emtala_facilities %>%
  count(Rural.Status)
```

    ##   Rural.Status   n
    ## 1           No 165
    ## 2          Yes 129
    ## 3         <NA>  95
