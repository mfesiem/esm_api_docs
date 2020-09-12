
import argparse
import shlex
import subprocess
import re
import os
import tempfile
import urllib.parse
import shutil
from string import Template
from .scrape import scrape

def parse_args():
    parser = argparse.ArgumentParser(description="""Create a PDF of the McAfee SIEM API documentation.""", prog="python3 -m esm_api_docs_to_pdf", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( '--url', help="SIEM API help URL.", required=True )
    parser.add_argument( '--out', help="Output PDF.", default="McAfee_SIEM_API_documentation.pdf" )
    parser.add_argument( '--wkhtmltopdf_args', help="wkhtmltopdf arguments as String. You should include the defaults arguments.  ", 
        default=" --disable-external-links --no-stop-slow-scripts ")
    args = parser.parse_args()
    return(args)

if __name__=="__main__":
    args = parse_args()
    print("Crawling SIEM API ressources docs...")
    # Call scrapy
    items = scrape('esm_api_docs', spider_kwargs={'url':args.url}, additionnal_settings={'LOG_LEVEL':'ERROR'})

    # Sort items
    urls = [ i['url'] for i in items ]
    summary = items.pop(0)
    methods = sorted([i for i in items if '/help/types/' not in i['url']], key=lambda k: k['url'])
    types = sorted([i for i in items if '/help/types/' in i['url']], key=lambda k: k['url'])
    
    #  Creating wkhtmltopdf Command
    wkhtmltopdf_cmd = ["wkhtmltopdf"]
    if args.wkhtmltopdf_args:
        wkhtmltopdf_cmd += shlex.split(args.wkhtmltopdf_args)
    hostname=urllib.parse.urlparse(args.url).netloc

    # Remove all references to the ESM hostname and replace with "ESM_URL"
    script=Template("""
var elems = document.getElementsByTagName('p');
var i;
for (i = 0; i < elems.length; i++) {
    if (elems[i].innerText.indexOf('$hostname') !== -1 ) {
        elems[i].innerText = elems[i].innerText.replace('$hostname', 'ESM_URL'); 
    }
}
""").substitute(hostname=hostname)
    wkhtmltopdf_cmd += ['--run-script', script]
    wkhtmltopdf_cmd += [ summary['url'] ] + [ m['url'] for m in methods ] + [ t['url'] for t in types ] + [ args.out ]
    print("Running: {}".format(wkhtmltopdf_cmd))
    print("This script will be executed on all pages to replace your ESM URL with 'ESM_URL':\n{}".format(script))
    print("Generating PDF file...")
    
    p = subprocess.run(args=wkhtmltopdf_cmd, timeout=300, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode!=0:
        raise(RuntimeError('{}\n{}'.format(p.stdout, p.stderr)))
        
    print("Done, the file {} has been generated. ".format(args.out))