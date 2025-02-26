# BH_deid
- SNUBH de-identification of clinical note project.
- Summarized notion [link](https://knotty-cent-563.notion.site/SNUBH-f9d3bcbf89a7403fb9cdc21f23298808) (Kor)

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


## 2021-05 Methods changed
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

### regex/
- Check regex set and csv file with ['note_id'] ['note_text'] PHI_columns e.g. ['날짜'] ['의료진이름'] ['환자이름']
- Sample code to detect simple type 1 and type 2 errors.
- `PHI_Hopital.ipynb` is the actual example applying checkPHI.py

## 2021-08 Labeling to apply KoBERT-NER
- [KoBERT-NER](https://github.com/monologg/KoBERT-NER)
- `labeling/*` file contains labeling code in stages.
- To cover different context expressions such as `판독의` `from` etc, make corresponding formula step by step.
- Not for automation but for checking.
