# McAfee SIEM API documentation to PDF

Create a clickable PDF of the McAfee SIEM API documentation.  

## Install

Install requirement: [wkhtmltopdf](https://wkhtmltopdf.org/index.html).  

Install python module.  
```
python3 -m pip install git+https://github.com/mfesiem/esm_api_docs_to_pdf.git
```

### Usage

Indicate your SIEM API help page URL and, optionnaly, the output file name.   
The program will crawl all your SIEM API documentation and pass the URLs to `wkhtmltopdf`.   
Also generate Javascript code to replace your ESM URL by "ESM_URL" in exemple calls.   
The rest of the links will be transformed to internal links by `wkhtmltopdf` or ignored.    

```
python3 -m esm_api_docs_to_pdf --url https://ESM_URL/rs/esm/v2/help --out API_v2_documentation.pdf
```

### Generate diff ESM API v1 v2
Install [pdf-diff](https://pypi.org/project/pdf-diff/), export v1.pdf and v2.pdf and run:   
```
pdf-diff -t "6.37" -s box,box v1.pdf v2.pdf > diff.png
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
                        wkhtmltopdf arguments as String. You should include
                        the defaults arguments. (default: --disable-external-
                        links --no-stop-slow-scripts )
```
