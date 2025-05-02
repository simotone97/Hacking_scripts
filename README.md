# 🧠 Malware Analysis Toolkit by Simone Tonelli

A curated collection of Python scripts developed for real-world malware analysis and threat intelligence automation.  
These tools were built and used during investigations of active campaigns involving **Formbook/xLoader**, **TA558**, **Lumma Stealer**, **VenomRAT**, **AsyncRAT**, **XWorm**, and others.

> All scripts are for educational and research purposes only.

---

## 📁 Included Tools

### 🔹 `formbook_decoder.py`
Automatically extracts and decodes the **real C2** of **Formbook/xLoader** samples, bypassing decoy infrastructure.
- Parses captured network traffic or artifacts
- Identifies and decodes embedded C2 addresses

### 🔹 `decoder_TA558.py`
Extracts embedded malicious DLLs from **images** used in steganographic delivery by **TA558**.
- Extracts Base64 payloads embedded in image files
- Saves raw output for further static or dynamic analysis

### 🔹 `Opendir_scraper.py`
Recursively scrapes **open directories** and downloads all accessible files.
- Optional automatic **VirusTotal scan**
- Renames files based on detection threshold
- Useful for staging analysis and data triage

### 🔹 `download malware bazaar.py`
Downloads tagged samples directly from **MalwareBazaar**.
- Uses tag-based querying
- Decrypts password-protected archives
- Can clean up ZIPs post-extraction

### 🔹 `ftp_via_tor_purge_them_all.py`
Monitors an FTP server **via Tor**, downloads new files and purges them.
- Used to intercept and delete exfiltrated data
- Requires local Tor instance running on `localhost:9050`
- Fully anonymized traffic routing

### 🔹 `GitHub_Repos_Scraping.py`
Scrapes all raw file links from a given GitHub user’s public repositories.
- Useful for automated collection of scripts, configurations, or embedded malicious samples

---

## 🚀 Getting Started

1. Clone this repository:

```bash
git clone https://github.com/simotone97/malware-analysis-toolkit.git
cd malware-analysis-toolkit

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install any required packages (check script headers):

```bash
pip install -r requirements.txt
