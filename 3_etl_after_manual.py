import pandas

etl_2_combined = pandas.read_excel("data/processed/2_etl_combined.xlsx")
manual_pregnant_patient = pandas.read_excel("data/manual/EMTALA_PREGNANT_2011-2022.xlsx")

pregnant_patient_keys = manual_pregnant_patient["key_identifier"].unique()
not_confirmed_pregnant = etl_2_combined[~(etl_2_combined["key_identifier"].isin(pregnant_patient_keys))]
not_confirmed_pregnant.to_excel("data/processed/3_etl_not_confirmed_pregnant.xlsx",index=False)
