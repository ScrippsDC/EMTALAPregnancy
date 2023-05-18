import pandas

etl_2_combined = pandas.read_excel("data/processed/2_etl_combined.xlsx")
manual_pregnant_patient = pandas.read_excel("data/processed/EMTALA_PREGNANT_2011-2022.xlsx")
more_to_remove = ["2409 PTBH11","2409 D6YK11","2409 IT9611","2407 74BC11","2409 VRM911","2409 NZOV11","2406 05FK11","2407 ZY3N11","2406 JOU711","2406 4F4G11","2406 8E2Y11","2409 PKRO11","2407 T0DE11","2406 CITS12","2406 S4NX11","2406 RU2V11","2407 UD9X11","2407 KZUZ11","2406 D9FE11"]

pregnant_patient_keys = manual_pregnant_patient["key_identifier"].str.strip().unique().tolist()
not_confirmed_pregnant = etl_2_combined[~(etl_2_combined["key_identifier"].str.strip().isin(pregnant_patient_keys))|(etl_2_combined["key_identifier"].str.strip().isin(more_to_remove))|(etl_2_combined["hospital_type"]=="Psychiatric")]
not_confirmed_pregnant.to_excel("data/processed/3_etl_not_confirmed_pregnant.xlsx",index=False)

confirmed_pregnant = etl_2_combined[(etl_2_combined["key_identifier"].str.strip().isin(pregnant_patient_keys))&(~etl_2_combined["key_identifier"].str.strip().isin(more_to_remove))&(etl_2_combined["hospital_type"]!="Psychiatric")]
confirmed_pregnant.to_excel("data/processed/3_etl_confirmed_pregnant.xlsx",index=False)