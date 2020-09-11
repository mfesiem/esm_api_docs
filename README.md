# McAfee SIEM API documentation to PDF

Create a clickable PDF of the McAfee SIEM API documentation.  

Install

Clone this repository and run
```
python3 -m pip install -r requirements.txt
```
Additionnaly, install [wkhtmltopdf](https://wkhtmltopdf.org/index.html).  

Usage:
```
% python3 -m esm_api_docs --url https://ESM_URL/rs/esm/v2/help
```

