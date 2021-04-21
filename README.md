# BH_deid
SNUBH de-identification of clinical note project.

### Whitelist
- Whitelist of clinical terms referenced by http://www.kmle.co.kr/kmle_cdict_1_1_download.php
- Use Java environment to access databse and extract raw data.
  - `java -cp "KMLE dictionary 1.1.jar" org.hsqldb.util.DatabaseManager`
  - URL : delete '.'(dot) and write 'cdictionary'.
  - Password : None.
  - Execute `selecte * from {dict_name}` and File-Save results.
- This data preprocessed to use easily by `refine_rawdict.ipynb`
- The result file is `dict_eng.csv` and `dict_abb.csv`.

### Blacklist
- Name
  - Crwal Korean name information from https://koreanname.me/

