# Code written by Rachel Gold (rachelgoldaz), edited by Rosie Cima (cimar)

library(readxl)
library(dplyr)
library(stringr)
library(writexl)

emtala_pregnant <- read_xlsx("data/manual/confirmed_pregnant.xlsx")

emtala_concat_violations<- emtala_pregnant %>%
  dplyr:: select(facility_name, hospital_type, facility_id, address, city, state, deficiency_tag,dfcncy_desc, inspection_date, EVENT_ID, year)%>%
     group_by(EVENT_ID) %>% 
     mutate(violations = paste0(dfcncy_desc, collapse = ", "))

emtala_concat_violations

distinct_concat_eventid<- 
     distinct(emtala_concat_violations, EVENT_ID, .keep_all = TRUE)

distinct_concat_eventid[duplicated(distinct_concat_eventid$EVENT_ID),]

distinct_concat_hospitals<- distinct_concat_eventid%>%
  group_by(facility_id) %>% 
     mutate(violation = paste0(dfcncy_desc, collapse = ", "))

distinct_concat_hospitals

distinct_concat_hospitals<- distinct_concat_hospitals%>%
  group_by(facility_id)%>%
  mutate(inspection_dates = paste0(inspection_date, collapse = ", "))

investigations_count<-distinct_concat_hospitals %>%
  group_by(facility_id) %>%
  summarize(distinct_investigations = n_distinct(EVENT_ID))

distinct_concat_hospitals[duplicated(distinct_concat_hospitals$facility_id),]

concat_hospitals <- distinct_concat_hospitals %>% inner_join(investigations_count,by="facility_id")

concat <- concat_hospitals[!duplicated(concat_hospitals$facility_id),]



rural_urban_hospitals <- read_excel("data/public/rural_urban_hospitals.xlsx")

rural_urban_hospitals <- 
  as.data.frame(rural_urban_hospitals)

rural_urban_hospitals<- rural_urban_hospitals%>%
  mutate(facility_id=as.numeric(facility_id))

emtala_hospital_status <- concat %>% inner_join(rural_urban_hospitals,by="facility_id")

emtala_hospital_status <- distinct(emtala_hospital_status, EVENT_ID, .keep_all = TRUE)

write_csv(emtala_hospital_status, "data/source/emtala_hospital_status.csv")


emtala_hospital_status[duplicated(emtala_hospital_status$facility_id),]
