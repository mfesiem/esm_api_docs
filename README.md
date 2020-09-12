# McAfee SIEM API documentation to PDF

Create a clickable PDF of the McAfee SIEM API documentation.  

## Install

Install requirement: [wkhtmltopdf](https://wkhtmltopdf.org/index.html).  

Install python module.  
```
python3 -m pip install git+https://github.com/mfesiem/esm_api_docs_to_pdf.git
```

### Usage

Indicate your SIEM API help page URL.  

```
python3 -m esm_api_docs_to_pdf --url https://ESM_URL/rs/esm/v2/help
```

### Help

```
usage: python3 -m esm_api_docs_to_pdf [-h] --url URL [--out OUT]
                               [--wkhtmltopdf_args WKHTMLTOPDF_ARGS]

Create a PDF of the McAfee SIEM API documentation.

optional arguments:
  -h, --help            show this help message and exit
  --url URL             SIEM API help URL. (default: None)
  --out OUT             Output PDF. (default:
                        McAfee_SIEM_API_documentation.pdf)
  --wkhtmltopdf_args WKHTMLTOPDF_ARGS
                        wkhtmltopdf arguments as String (default: --disable-
                        external-links )
```
