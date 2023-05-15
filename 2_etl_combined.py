import pandas

etl_0 = pandas.read_excel("data/processed/0_etl_simple_text_search.xlsx")
etl_1 = pandas.read_excel("data/processed/1_etl_nearby_text_search.xlsx")

# Merge the two dataframes. If a row is in both, keep the row from etl_1 (the "may_be_pregnant_*" columns are useful for finding which keyword triggered inclusion)
combo = pandas.concat([etl_1,etl_0]).drop_duplicates(subset=["key_identifier"])
print(combo.shape)
combo.to_excel("data/processed/2_etl_combined.xlsx")