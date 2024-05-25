# EmailCollector
<pre>
███████╗███╗   ███╗ █████╗ ██╗██╗          ██████╗ ██████╗ ██╗     ██╗     ███████╗ ██████╗████████╗ ██████╗ ██████╗ 
██╔════╝████╗ ████║██╔══██╗██║██║         ██╔════╝██╔═══██╗██║     ██║     ██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
█████╗  ██╔████╔██║███████║██║██║         ██║     ██║   ██║██║     ██║     █████╗  ██║        ██║   ██║   ██║██████╔╝
██╔══╝  ██║╚██╔╝██║██╔══██║██║██║         ██║     ██║   ██║██║     ██║     ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
███████╗██║ ╚═╝ ██║██║  ██║██║███████╗    ╚██████╗╚██████╔╝███████╗███████╗███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝     ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
A tool for collecting and validating emails via SMTP
https://github.com/larinskiy/emailcollector
Check -h for futher information
Based on tools: Phonebook.cz -> SMTP
</pre>

## Installation

`pip install -r requirements.txt` - install libraries for EmailCollector usage.

## Get Phonebook.cz token

To get a Phonebook.cz token to use this tool, register on the service Intelx.io and then make a request to a non-existent domain on the site Phonebook.cz. The token will be located in the URL of the POST request `https://2.intelx.io/phonebook/search?k={YOUR_TOKEN}`. After first token usage it will be cached in `.token` file.

## Usage examples

`python emailcollector.py` - run EmailCollector in interactive mode

`python emailcollector.py -d <DOMAIN>` - perform search for specified DOMAIN name via Phonebook.cz

`python emailcollector.py -t <DOMAIN FILE>` - perform search with specified TOKEN via Phonebook.cz

`python emailcollector.py -i <EMAIL FILE>` - perform email validation for addresses in EMAIL FILE without Phonebook.cz search

## Ouput files

Output files are:

`collected_emails_<DOMAIN>.txt` - list of emails collected on Phonebook.cz

`checked_emails_<DOMAIN>.txt` - list of emails after validating

## Bugs
If you find bugs in the operation of this program, be sure to let me know about them. This tool was developed spontaneously, but its support continues. Report bugs in this repository.