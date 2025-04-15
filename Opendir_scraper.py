import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Trova il Desktop dell'utente e crea la cartella "sample"
desktop = os.path.join(os.path.expanduser("~"), "Desktop", "sample")
os.makedirs(desktop, exist_ok=True)

def get_links(current_url, root_url=None, visited=None):
    if visited is None:
        visited = set()
    if root_url is None:
        root_url = current_url
    # Assicuriamoci che root_url termini con '/' per il confronto
    if not root_url.endswith('/'):
        root_url += '/'
    
    if current_url in visited:
        return []
    visited.add(current_url)
    
    links = []
    try:
        response = requests.get(current_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and not href.startswith('?'):
                full_url = urljoin(current_url, href)
                # Filtra i link che non appartengono all'albero di partenza
                if not full_url.startswith(root_url):
                    continue
                if full_url not in visited:
                    links.append(full_url)
                    if full_url.endswith('/'):
                        links.extend(get_links(full_url, root_url, visited))
    except Exception as e:
        print(f"Errore nell'accesso a {current_url}: {e}")
    
    return links

def download_files(urls):
    for url in urls:
        # Salta le directory
        if url.endswith("/"):
            continue  
        file_name = os.path.join(desktop, os.path.basename(url))
        try:
            print(f"Scaricando {url}...")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Salvato in {file_name}")
        except Exception as e:
            print(f"Errore scaricando {url}: {e}")

def scan_file(file_path, api_key):
    vt_url = "https://www.virustotal.com/api/v3/files"
    headers = {"x-apikey": api_key}
    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            print(f"Caricando {file_path} su VirusTotal...")
            response = requests.post(vt_url, headers=headers, files=files)
            response.raise_for_status()
            analysis_id = response.json()["data"]["id"]
            print(f"File {file_path} caricato. Analysis ID: {analysis_id}")
    except Exception as e:
        print(f"Errore durante il caricamento di {file_path}: {e}")
        return None

    # Poll per ottenere il risultato dell'analisi
    analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    while True:
        try:
            analysis_response = requests.get(analysis_url, headers=headers)
            analysis_response.raise_for_status()
            analysis_data = analysis_response.json()["data"]
            status = analysis_data["attributes"]["status"]
            if status == "completed":
                stats = analysis_data["attributes"].get("stats", {})
                print(f"Risultato analisi per {file_path}: {stats}")
                return stats
            else:
                print(f"Analisi in corso per {file_path}... attendo 15 secondi...")
                time.sleep(15)
        except Exception as e:
            print(f"Errore nel recuperare l'analisi per {file_path}: {e}")
            return None

def scan_downloaded_samples(api_key):
    results = {}
    print("Inizio scansione dei file scaricati in Desktop/sample ...")
    for file in os.listdir(desktop):
        file_path = os.path.join(desktop, file)
        if os.path.isfile(file_path):
            stats = scan_file(file_path, api_key)
            if stats is not None:
                results[file_path] = stats
    return results

def rename_malicious_files(results, threshold):
    for file_path, stats in results.items():
        # Consideriamo il conteggio "malicious" per il confronto
        malicious_count = stats.get("malicious", 0)
        if malicious_count >= threshold:
            base, ext = os.path.splitext(file_path)
            new_file = base + ".mal"
            try:
                os.rename(file_path, new_file)
                print(f"File {file_path} rinominato in {new_file} (malicious: {malicious_count})")
            except Exception as e:
                print(f"Errore nel rinominare {file_path}: {e}")
        else:
            print(f"File {file_path} non supera la soglia (malicious: {malicious_count})")

if __name__ == "__main__":
    opendir_url = input("Inserisci l'URL della OpenDir: ").strip()
    if not opendir_url.endswith('/'):
        opendir_url += '/'
    
    links = get_links(opendir_url)
    
    print("Tutti i link trovati:")
    for link in links:
        print(link)
    
    download = input("Vuoi scaricare i file? (s/n): ").strip()
    if download.lower() == 's':
        download_files(links)
    
    vt_scan = input("Vuoi caricare i file scaricati su VirusTotal per la scansione? (s/n): ").strip()
    vt_results = {}
    if vt_scan.lower() == 's':
        api_key = input("Inserisci la tua API key di VirusTotal: ").strip()
        vt_results = scan_downloaded_samples(api_key)
    
    rename_choice = input("Vuoi rinominare i file in base a una soglia di detection? (s/n): ").strip()
    if rename_choice.lower() == 's':
        try:
            threshold = int(input("Inserisci la soglia di detection (numero intero): ").strip())
        except ValueError:
            print("Valore non valido. Operazione annullata.")
            threshold = None
        if threshold is not None:
            if not vt_results:
                print("Non sono disponibili risultati da VirusTotal per effettuare il confronto.")
            else:
                rename_malicious_files(vt_results, threshold)
