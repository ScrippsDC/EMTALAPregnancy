library(readxl)
library(writexl)

# Changed to reference the files as they're named at source
cms_deficiencies1 <- read_xlsx("data/source/Hospital_2567s_2022Q3/Hospital 2567s - 2022Q3 Part 1.xlsx")
cms_deficiencies2 <- read_xlsx("data/source/Hospital_2567s_2022Q3/Hospital 2567s - 2022Q3 Part 2.xlsx")

events_all<- bind_rows(cms_deficiencies1, cms_deficiencies2)

emtala_events_psych_crit_short <- events_all %>%
 filter(grepl('2400|2401|2402|2403|2404|2405|2406|2407|2408|2409|2410|2411', deficiency_tag))

emtala_events_psych_crit_short$index <- 1:nrow(emtala_events_psych_crit_short)

emtala_events_psych_crit_short$year <- format(as.Date(emtala_events_psych_crit_short$inspection_date, format="%Y/%M/%D"),"%Y")

emtala_events_psych_crit_short$key_identifier <-
  paste(emtala_events_psych_crit_short$deficiency_tag, emtala_events_psych_crit_short$EVENT_ID)

# Our keyword/stop word system is good enough that this filter isn't doing anything anymore
# emtala_events_crit_short <- filter(emtala_events_psych_crit_short, hospital_type != "Psychiatric")

# Moved these into their own files so they're easier to work with
# Stop phrases are almost universally to screen out uses of the word "pregnancy" that are about pregnancy in the abstract, not a particular pregnancy
stopph <- readLines("data/manual/0_etl_stopphrases.txt")
keywords <- readLines("data/manual/0_etl_keywords.txt")

emtala_events_crit_short$inspection_text2 <- stringi::stri_replace_all_regex(emtala_events_crit_short$inspection_text,
                                  pattern=stopph,
                                  replacement="",vectorize=FALSE)

emtala_events_crit_short$inspection_len <- nchar(as.character(emtala_events_crit_short$inspection_text2))

emtala_key_word_deficiencies <- emtala_events_crit_short %>% 
  dplyr::select(facility_name, hospital_type, facility_id, address, city, state, deficiency_tag, dfcncy_desc,inspection_date, EVENT_ID, inspection_text2, index, key_identifier, year, inspection_len) %>% 
  dplyr::filter(str_detect(inspection_text2, paste(keywords, collapse = "|")))

print(dim(emtala_key_word_deficiencies))

#aggregate by hospital type to prove we don't need to filter out psychiatric hospitals
emtala_key_word_deficiencies_hosp_type <- emtala_key_word_deficiencies %>%
  group_by(hospital_type) %>%
  summarise(count = n())

print(emtala_key_word_deficiencies_hosp_type)

# Truncate rows where the inspection_text is too long to write to excel
emtala_key_word_deficiencies$inspection_text2 <- ifelse(emtala_key_word_deficiencies$inspection_len > 32767, substr(emtala_key_word_deficiencies$inspection_text2,0,32766), emtala_key_word_deficiencies$inspection_text2)
write_xlsx(emtala_key_word_deficiencies, "data/processed/0_etl_simple_text_search.xlsx")