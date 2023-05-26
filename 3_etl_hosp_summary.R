# Code written by Rachel Gold (rachelgoldaz), edited by Rosie Cima (cimar)

library(readxl)
library(dplyr)
library(stringr)
library(writexl)


emtala_pregnant <- read_xlsx("data/manual/confirmed_pregnant.xlsx")

# GroupBy facility_id
by_facility <- emtala_pregnant %>%
     group_by(facility_id) %>% 
     # Put all these summary calculations in the same line, within the same groupby, instead of doing the groupby multiple times and joining
     mutate(violations = paste0(dfcncy_desc, collapse = ", "),inspection_dates = paste0(inspection_date, collapse = ", "),distinct_investigations = n_distinct(EVENT_ID))

# Limit to the columns that are going to be the same within each group
cols_to_keep <- c("facility_name", "hospital_type", "facility_id", "address", "city", "state","violations","inspection_dates","distinct_investigations")
by_facility_lim_cols <- by_facility %>% dplyr:: select(all_of(cols_to_keep))

# Remove duplicates
by_facility_lim_cols_drop_dup <- distinct(by_facility_lim_cols)
write.csv(by_facility_lim_cols_drop_dup, "data/source/facility_summary.csv")