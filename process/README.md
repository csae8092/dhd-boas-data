This folder contains (hopefully) quite generic scripts bulk process .dhc files

* config.py: holds project wide configurations to reduce code duplication
* teipy.py: provide helper function and classes to process TEI documents
* extract_teis.ipynb: extracts TEI files from .dhc archives and moves them into a TEI directory (images referenced in the TEI's are extracted and moved to IMG folder)
* fixed_encoding_issue_in_tei_address.ipyn: replaces corrupted notes with properly encoded ones
* analyze: Transform TEI-Docs into a hopefully useful pandas.DataFrame for further analysis, postprocessing, ....
