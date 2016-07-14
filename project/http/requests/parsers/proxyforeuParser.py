from project.http.requests.parsers.UrlParser import UrlParser
import requests
from bs4 import BeautifulSoup

class proxyforeuParser(UrlParser):

    def __init__(self, web_url, bandwithdh=None):
        UrlParser.__init__(self, web_url, bandwithdh)

    def parse_proxyList(self):
        curr_proxy_list = []
        content = requests.get(self.get_URl()).content
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table", attrs={"class": "proxy_list"})

        # The first tr contains the field names.
        headings = [th.get_text() for th in table.find("tr").find_all("th")]

        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            datasets.append(dataset)

        for dataset in datasets:
            # Check Field[0] for tags and field[1] for values!
            proxy = "http://"
            proxy_straggler = False
            for field in dataset:
                # Discard slow proxies! Speed is in KB/s
                if field[0] == 'Speed':
                    if float(field[1]) < self.get_bandwidthLimit():
                        proxy_straggler = True
                if field[0] == 'IP':
                    proxy = proxy + field[1] + ':'
                elif field[0] == 'Port':
                    proxy = proxy + field[1]
            # Avoid Straggler proxies
            if not proxy_straggler:
                curr_proxy_list.append(proxy.__str__())
                # print "{0:<10}: {1}".format(field[0], field[1])
        # print "ALL: ", curr_proxy_list
        return curr_proxy_list

    def __str__(self):
        return "ProxyForEU Parser of '{0}' with bandwidth limit at '{1}' KBs" \
            .format(self.url, self.bandwidth_limit_in_KBs)