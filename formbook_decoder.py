import pyshark
import requests
from collections import defaultdict, Counter

# === CONFIG ===
pcap_file = 'formbook.pcapng'
timeout = 5

# === PARSING DEL PCAP ===
domain_uri_counter = defaultdict(Counter)

cap = pyshark.FileCapture(pcap_file, display_filter='http.request.method == "GET"')

for pkt in cap:
    try:
        http = pkt.http
        host = http.host
        uri = http.request_uri
        domain_uri_counter[host][uri] += 1
    except AttributeError:
        continue

cap.close()

# === SUSPICIOUS DOMAIN EXTRACTION === #
suspicious_domains = []

print("Possible C2 domains (same requests repeated):\n")

for domain, uri_counter in domain_uri_counter.items():
    for uri, count in uri_counter.items():
        if count > 1:
            print(f"[+] {domain} --> {uri} -> {count} volte")
            if domain not in suspicious_domains:
                suspicious_domains.append(domain)

# === CHECK HTTP LOREM IPSUM ===
print("\nChecking the homepage of the suspicious domains...\n")

for domain in suspicious_domains:
    try:
        url = f"http://{domain}"
        response = requests.get(url, timeout=timeout)
        if "lorem ipsum" in response.text.lower():
            print(f"{domain} contains 'Lorem Ipsum' → **HIGHLY PROBABLE C2 DOMAINS**")
        else:
            print(f"[ ] {domain} doesn't contain 'Lorem Ipsum'")
    except Exception as e:
        print(f"[x] Erroreì on {domain}: {e}")