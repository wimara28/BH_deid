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


## 2021-05  changed
- Instead of considering all whitelist/blacklist, constructing regular expression to catch PHI patterns.
- `tagging.py` uses regular expression to de-identifying clinical notes with several pre-defined regex patterns.

### Tagging.py
- This file needs some environments.
1. Clinical notes `csv` file with column name 'NOTE_ID' and 'note_text'.
2. Pre-defined regular expression folders with form of `regex/{PHI category}/{regular expression txt files corresponding the category`.
  For example, `regex/dates/YYYY-MM-DD.txt` or `regex/hospitals/hospital_kor.txt`.
3. Before run, regex files must be transformed by `regex/transform_regex.py`. Only `_transformed.txt` files could be read to catch patterns.
4. To save output, create `output/` folder.
5. If you want asterisk(`*`) results, add `--asterisk` or `-a` args. 
