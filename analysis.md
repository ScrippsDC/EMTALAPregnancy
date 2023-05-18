cms_hospital_deficiency
================
Rachel Gold
2022-07-12

## R Markdown

The purpose of this markdown is to analyze CMS Hospital Survey
Deficiencies for specific reproductive-language words. Our goal is to
capture all EMTALA violations involving pregnant patients.

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

\##Reading in violations from 2011-Q3 2022 post manual review of
inspection_text to determine if violation involved a pregnant patient:
This includes Rosie’s 109 captured violations

``` r
emtala_pregnant <- read_xlsx("data/manual/confirmed_pregnant.xlsx")
emtala_all <- read_xlsx("data/processed/0_etl_all_emtala_deficiencies.xlsx")
```

Web: “Our investigation found 386 hospitals spanning 44 states have
violated EMTALA statutes while attending to pregnant patients, racking
up at least 675 federal violations since 2011.”

Script: “OUR SCRIPPS NEWS INVESTIGATION FOUND IT IS AMONG 386 HOSPITALS
(FC) AROUND THE COUNTRY REPONSIBLE FOR NEARLY 700 VIOLATIONS OF THE
EMERGENCY MEDICAL TREATMENT AND LABOR ACT – OR EMTALA—

…ALL INVOLVING PREGNANCY EMERGENCIES BETWEEN 2011 AND 2022.”

``` r
facility_count<-n_distinct(emtala_pregnant$facility_id)

violation_count<-n_distinct(emtala_pregnant$key_identifier)

state_count<-n_distinct(emtala_pregnant$state)

emtala_pregnant%>%group_by(state)%>% summarize(violations_per_state = n_distinct(key_identifier))
```

    ## # A tibble: 44 × 2
    ##    state violations_per_state
    ##    <chr>                <int>
    ##  1 AK                       2
    ##  2 AL                      27
    ##  3 AR                       5
    ##  4 AZ                       7
    ##  5 CA                      65
    ##  6 CO                      19
    ##  7 CT                       3
    ##  8 FL                      41
    ##  9 GA                      34
    ## 10 IA                      23
    ## # ℹ 34 more rows

``` r
print(paste("facility_count:",facility_count,"violation_count:",violation_count,"state_count:",state_count))
```

    ## [1] "facility_count: 386 violation_count: 675 state_count: 44"

Web: “racking up at least 675 federal violations since 2011.”
Script:“…ALL INVOLVING PREGNANCY EMERGENCIES BETWEEN 2011 AND 2022.”

``` r
emtala_pregnant%>%
  count(year)
```

    ## # A tibble: 12 × 2
    ##     year     n
    ##    <dbl> <int>
    ##  1  2011    76
    ##  2  2012    43
    ##  3  2013    51
    ##  4  2014    72
    ##  5  2015    81
    ##  6  2016    52
    ##  7  2017    90
    ##  8  2018    66
    ##  9  2019    62
    ## 10  2020    25
    ## 11  2021    40
    ## 12  2022    17

Web: “Cases involving pregnant women made up about 16% of all EMTALA
investigations.”

``` r
#number of EMTALA pregnant patient investigations since 2011
count_preg<-n_distinct(emtala_pregnant$EVENT_ID)

#number of EMTALA investigations overall since 2011
count_invest<-n_distinct(emtala_all$EVENT_ID)

#percent of EMTALA investigations involving a pregnant patient since 2011 
print(paste(count_preg,"investigations of violations against pregnant patients, out of",count_invest,"investigations of overall. (",count_preg/count_invest*100,"%)"))
```

    ## [1] "413 investigations of violations against pregnant patients, out of 2694 investigations of overall. ( 15.3303637713437 %)"

Web: “We found the most common EMTALA violation was “failure to provide
medical screening examinations.” (medical screening exam = 2406)

``` r
emtala_pregnant %>%
  count(deficiency_tag)
```

    ## # A tibble: 11 × 2
    ##    deficiency_tag     n
    ##             <dbl> <int>
    ##  1           2400    77
    ##  2           2401     3
    ##  3           2402     4
    ##  4           2403     4
    ##  5           2404     9
    ##  6           2405    84
    ##  7           2406   262
    ##  8           2407    83
    ##  9           2408    15
    ## 10           2409   122
    ## 11           2411    12

``` r
# filter emtala_pregnant for deficiency tag == 2406
count_all_preg <- n_distinct(emtala_pregnant$key_identifier)
count_2406 <- n_distinct((emtala_pregnant %>% filter(deficiency_tag == 2406))$key_identifier)

print(paste(count_2406,"medical screening violations against pregnant patients, out of",count_all_preg,"violations against pregnant patients of overall. (",count_2406/count_all_preg*100,"%)"))
```

    ## [1] "262 medical screening violations against pregnant patients, out of 675 violations against pregnant patients of overall. ( 38.8148148148148 %)"

262/675

Web: “Our investigation found of the cases that were investigated by
CMS, at least 237 involved pregnant women going to the ER for care and
being turned away.”

``` r
# I added "turnaway" as a column in confirmed_pregnant.xlsx
emtala_pregnant <- read_xlsx("data/manual/confirmed_pregnant.xlsx")
turnaway <- emtala_pregnant %>% filter(turnaway == TRUE)
n_distinct(turnaway$EVENT_ID)
```

    ## [1] 241

``` r
turnaway <- read_xlsx("data/processed/turnaway.xlsx")
turnaway_y <- turnaway %>%
  filter(turnaway == "Y")
 

n_distinct(turnaway_y$EVENT_ID)
```

    ## [1] 237
