import sys
from urllib import response
import requests
import json
import argparse
import logging

logging.basicConfig(level=logging.INFO)

class AdguardhomeRewriteManagement:
    def __init__(self) -> None:
        parse = argparse.ArgumentParser(
            usage="%(prog)s [OPTION] [FILE]...",
            description="Add users to adguard"
        )
        parse.add_argument(
            "-a", "--adguard-servers", help="Array of Adguard Servers (list seperated by comma)", required=True
        )
        parse.add_argument(
            "-d", "--domain", help="Domain to add the IPs to", required=True
        )
        parse.add_argument(
            "-u", "--user", help="Adguard Username", required=True
        )
        parse.add_argument(
            "-p", "--password", help="Adguard Password", required=True
        )
        parse.add_argument(
            "-f", "--file", help="File containing IPs to add", required=True
        )
        args = parse.parse_args()
        self.adguard_servers = args.adguard_servers.split(',')
        self.domain = args.domain
        self.username = args.user
        self.password = args.password
        self.address_file = args.file
        with open(self.address_file) as file:
            self.address_records = json.load(file)
    
    def api_post(self, domain, path, payload):
        auth = requests.auth.HTTPBasicAuth('admin', 'admin')
        url = domain + '/' + path
        response = requests.post(url, auth=auth, json=payload)
        return response

    def api_get(self, domain, path):
        auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        url = domain + '/' + path
        response = requests.get(url, auth=auth)
        return response.content

    def check_record_exists(self, server, domain, answer):
        current_records = json.loads(self.api_get(server, 'control/rewrite/list'))
        result = False
        for record in current_records:
            current_domain = record.get('domain')
            current_answer = record.get('answer')
            if current_domain == domain and current_answer == answer:
                result = True
        return result

    @property
    def servers(self):
        return self.adguard_servers

    @property
    def records(self):
        return self.address_records

if __name__ == '__main__':
    client = AdguardhomeRewriteManagement()
    for s in client.servers:
        logging.info('Working with server %s', s)
        for device, v in client.records.items():
            fqdn = f'{device}.{client.domain}'
            ip_address = v['ip_address']
            mac_address = v['mac_address']
            if not client.check_record_exists(s, fqdn, ip_address):
                payload = {
                    "domain": fqdn,
                    "answer": ip_address
                }

                response = client.api_post(s, 'control/rewrite/add', payload)
                if response.status_code == 200:
                    logging.info('Record %s added!', fqdn)
            else:
                logging.info('Record %s already in place.', fqdn)
