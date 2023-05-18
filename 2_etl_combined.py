import pandas

etl_0 = pandas.read_excel("data/processed/0_etl_simple_text_search.xlsx")
etl_1 = pandas.read_excel("data/processed/1_etl_nearby_text_search.xlsx")

def method(key_identifier):
    simp_txt_keys = etl_0["key_identifier"].unique().tolist()
    near_txt_keys = etl_1["key_identifier"].unique().tolist()
    if key_identifier in simp_txt_keys:
        if key_identifier in near_txt_keys:
            return "both"
        return "simple"
    if key_identifier in near_txt_keys:
        return "nearby"
    return ""

# Merge the two dataframes. If a row is in both, keep the row from etl_1 (the "may_be_pregnant_*" columns are useful for finding which keyword triggered inclusion)
combo = pandas.concat([etl_1,etl_0]).drop_duplicates(subset=["key_identifier"])
combo["method"] = combo["key_identifier"].apply(method)
combo["year"] = combo["inspection_date"].dt.year

keep_cols = ['key_identifier','method','facility_name', 'hospital_type', 'facility_id', 'address', 'city', 'state', 'deficiency_tag', 'missing_survey_tag_count', 'dfcncy_desc', 'defpref', 'inspection_date', 'EVENT_ID', 'inspection_text', 'may_be_pregnant_rc_near_text', 'may_be_pregnant_rc_graf','year']
combo[keep_cols].to_excel("data/processed/2_etl_combined.xlsx")

