
import argparse
import shlex
import subprocess
from .scrape import scrape

def parse_args():
    parser = argparse.ArgumentParser(description="""Create a PDF of the McAfee SIEM API documentation.""", prog="python3 -m esm_api_docs_to_pdf", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( '--url', help="SIEM API help URL.", required=True )
    parser.add_argument( '--out', help="Output PDF.", default="McAfee_SIEM_API_documentation.pdf" )
    parser.add_argument( '--wkhtmltopdf_args', help="wkhtmltopdf arguments as String", default=" --disable-external-links ")
    args = parser.parse_args()
    return(args)

if __name__=="__main__":
    args = parse_args()
    print("Getting SIEM API ressources URLs list...")
    items = scrape('esm_api_docs', spider_kwargs={'url':args.url}, additionnal_settings={'LOG_LEVEL':'ERROR'})
    urls = [ i['url'] for i in items ]
    summary = [ urls.pop(0) ]
    methods = sorted([u for u in urls if '/help/types/' not in u])
    types = sorted([u for u in urls if '/help/types/' in u])
    wkhtmltopdf_cmd = ["wkhtmltopdf"]
    if args.wkhtmltopdf_args:
        wkhtmltopdf_cmd += shlex.split(args.wkhtmltopdf_args)
    wkhtmltopdf_cmd += summary + methods + types + [args.out]
    print("Generating PDF file...")
    p = subprocess.run(args=wkhtmltopdf_cmd, timeout=300, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode!=0:
        raise(RuntimeError(p.stderr))
    print("Done, the file {} has been generated. ".format(args.out))