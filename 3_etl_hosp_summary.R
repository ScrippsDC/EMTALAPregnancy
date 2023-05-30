# Code written by Rachel Gold (rachelgoldaz), edited by Rosie Cima (cimar)

library(readxl)
library(dplyr)
library(stringr)
library(writexl)

emtala_pregnant <- read_xlsx("data/manual/confirmed_pregnant.xlsx")

# Convert facility_id to character str
emtala_pregnant$facility_id <- as.character(emtala_pregnant$facility_id)

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

rural_urban <- read_xlsx("data/source/Data_Explorer_Dataset--hrsa_hcs_mua.xlsx")
rural_urban <- rural_urban %>% dplyr:: select("Provider #", "Rural Status")

by_facility_rural_urban <- left_join(by_facility_lim_cols_drop_dup, rural_urban, by = c("facility_id" = "Provider #"))

# Remove duplicates
by_facility_rural_urban <- distinct(by_facility_rural_urban)

write.csv(by_facility_rural_urban, "data/processed/3_etl_facility_summary.csv")