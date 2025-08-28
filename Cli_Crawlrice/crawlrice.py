#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, json, time, urllib.parse as urlparse
import requests
import os
import argparse
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Tuple
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# BASE_URL = "http://example.com"
CRAWL_MAX_PAGES = 500
REQUEST_TIMEOUT = 15

@dataclass
class Endpoint:
    method: str
    url: str
    path: str
    query: Dict[str, List[str]]
    body: Dict[str, Any]
    status: int = 0
    source: str = "html"
    normalized_key: str = ""

def full_url(u: str, base_url: str) -> str:
    if u.startswith("http"):
        return u
    return base_url.rstrip("/") + "/" + u.lstrip("/")

def split_url(u: str) -> Tuple[str, str, Dict[str, List[str]]]:
    p = urlparse.urlparse(u)
    q = urlparse.parse_qs(p.query)
    return u, p.path, q

def make_session(cookies: Dict[str,str], base_url: str) -> requests.Session:
    s = requests.Session()
    for k,v in cookies.items():
        s.cookies.set(k, v, domain=urlparse.urlparse(base_url).hostname)
    s.headers.update({"User-Agent":"IDOR-Scanner/0.1"})
    return s

def selenium_login_get_cookies(username:str, password:str, login_url: str) -> Dict[str,str]:
    print(f"  Mencoba login sebagai '{username}'...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(login_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME,"username")))
        driver.find_element(By.NAME,"username").send_keys(username)

        if password:
            try:
                password_field = driver.find_element(By.NAME, "password")
                password_field.send_keys(password)
                print("    Password diisi.")
            except NoSuchElementException:
                print("    Field password tidak ditemukan, melanjutkan tanpa password.")
        else:
            print("    Tidak ada password yang diberikan, mencoba login hanya dengan username.")

        driver.find_element(By.CSS_SELECTOR,"button[type=submit],input[type=submit],.btn-login").click()
        time.sleep(2) # Beri waktu untuk redirect
        return {c["name"]:c["value"] for c in driver.get_cookies()}
    finally:
        driver.quit()

def mutate_post_data_for_idor(ep: Endpoint, victim_ref_ids: List[str] = None) -> List[Dict[str, Any]]:
    victim_ref_ids = victim_ref_ids or ["1","2","3","10","99"]
    muts = []
    id_like_keys = [k for k in ep.body.keys() if "id" in k.lower() or "user" in k.lower() or "project" in k.lower()]
    if not id_like_keys:
        muts.append(ep.body)
        return muts
    for key in id_like_keys:
        for vid in victim_ref_ids:
            new_body = {k:v for k,v in ep.body.items()}
            new_body[key] = vid
            muts.append(new_body)
    seen = set()
    uniq = []
    for b in muts:
        k = json.dumps(b, sort_keys=True)
        if k not in seen:
            seen.add(k)
            uniq.append(b)
    return uniq[:10]

def crawl_hybrid(session_cookies: Dict[str,str], start_paths: List[str], base_url: str) -> List[Endpoint]:
    print("🚀 Memulai crawler hybrid...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    endpoints: List[Endpoint] = []
    visited_urls = set()
    paths_to_crawl = list(start_paths)
    try:
        driver.get(base_url)
        for k, v in session_cookies.items():
            driver.add_cookie({"name": k, "value": v, "domain": urlparse.urlparse(base_url).hostname})
        while paths_to_crawl and len(visited_urls) < CRAWL_MAX_PAGES:
            path = paths_to_crawl.pop(0)
            url = full_url(path, base_url)
            if url in visited_urls:
                continue
            print(f"  Crawling: {url}")
            visited_urls.add(url)
            try:
                driver.get(url)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                html = driver.page_source
            except Exception as e:
                print(f"    [!] Gagal mengunjungi {url}: {e}")
                continue
        
            try:
                current_url, current_path, current_query = split_url(driver.current_url)
                endpoints.append(Endpoint(method="GET", url=current_url, path=current_path, query=current_query, body={}))
            except Exception as e:
                print(f"    [!] Gagal mem-parsing URL saat ini: {driver.current_url}, error: {e}")
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if not href or href.startswith("#") or href.startswith("javascript:"):
                    continue
                
                next_url = full_url(href, base_url)
                
                if urlparse.urlparse(next_url).netloc == urlparse.urlparse(base_url).netloc:
                    parsed_url = urlparse.urlparse(next_url)
                    path = parsed_url.path
                    query = urlparse.parse_qs(parsed_url.query)
                    
                    endpoints.append(Endpoint(method="GET", url=next_url, path=path, query=query, body={}, status=0))
                    
                    if next_url not in visited_urls and len(visited_urls) + len(paths_to_crawl) < CRAWL_MAX_PAGES:
                        path_to_crawl = path
                        if parsed_url.query:
                            path_to_crawl += "?" + parsed_url.query
                        paths_to_crawl.append(path_to_crawl)
            for form in soup.find_all("form"):
                action = form.get("action") or url
                method = (form.get("method") or "POST").upper()
                if method not in ["GET","POST","PUT","DELETE","PATCH"]:
                    method = "POST"
                body = {inp.get("name"): "test_value" for inp in form.find_all("input") if inp.get("name")}
                ep = Endpoint(method=method, url=full_url(action, base_url), path=urlparse.urlparse(action).path, query={}, body=body, status=0)
                endpoints.append(ep)
                for mutated_body in mutate_post_data_for_idor(ep):
                    endpoints.append(Endpoint(method=method, url=ep.url, path=ep.path, query={}, body=mutated_body, status=0))
    finally:
        driver.quit()
    unique_endpoints = list({(ep.method, ep.path, json.dumps(ep.query, sort_keys=True), json.dumps(ep.body, sort_keys=True)): ep for ep in endpoints}.values())
    print(f"✅ Crawling selesai. Ditemukan {len(unique_endpoints)} endpoint unik.")
    return unique_endpoints

def diff_candidates_raw(victim_eps: List[Endpoint], attacker_eps: List[Endpoint]) -> List[Endpoint]:
    atk_paths = {(e.method, e.path, json.dumps(e.query, sort_keys=True)) for e in attacker_eps}
    candidates = []
    for e in victim_eps:
        key = (e.method, e.path, json.dumps(e.query, sort_keys=True))
        if key not in atk_paths:
            candidates.append(e)
    return candidates

def probe_with_session(session: requests.Session, ep: Endpoint, base_url: str) -> Dict[str, Any]:
    url = full_url(ep.path, base_url)
    try:
        if ep.method.upper() == "GET":
            r = session.get(url, params=ep.query, timeout=REQUEST_TIMEOUT, allow_redirects=False)
        elif ep.method.upper() in ["POST", "PUT", "PATCH", "DELETE"]:
            r = session.request(ep.method.upper(), url, data=ep.body, params=ep.query,
                                timeout=REQUEST_TIMEOUT, allow_redirects=False)
        else:
            return {"error": f"Method {ep.method} tidak didukung"}
        return {
            "status": r.status_code, "len": len(r.content or b""), "location": r.headers.get("Location"),
            "snippet": (r.text[:200] if r.headers.get("Content-Type", "").startswith("text/") else "")
        }
    except Exception as e:
        return {"error": str(e)}

def render_html(report: Dict[str, Any]) -> str:
    html = f"""
    <!DOCTYPE html>..."""
    return html

def run(base_url, attacker_user, attacker_pass, victim_user, victim_pass):
    """Fungsi utama yang menerima semua konfigurasi sebagai argumen."""
    login_url = f"{base_url.rstrip('/')}/login"
    start_paths = ["/", "/dashboard", "/profile"]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(script_dir, '..', 'Gui_Crawlrice', 'reports')
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    domain_name = urlparse.urlparse(base_url).netloc.replace(':', '_')
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_filename = f"report_{domain_name}_{timestamp}"

    print("🔹 Login attacker...")
    atk_cookies = selenium_login_get_cookies(attacker_user, attacker_pass, login_url)
    print(f"  Cookies attacker: {atk_cookies}")

    print("🔹 Login victim...")
    vic_cookies = selenium_login_get_cookies(victim_user, victim_pass, login_url)
    print(f"  Cookies victim: {vic_cookies}")

    print("\n🔹 Crawling endpoint Attacker dengan metode hybrid...")
    all_attacker_eps = crawl_hybrid(atk_cookies, start_paths, base_url)
    
    print("\n🔹 Crawling endpoint Victim dengan metode hybrid...")
    all_victim_eps = crawl_hybrid(vic_cookies, start_paths, base_url)

    candidates = diff_candidates_raw(all_victim_eps, all_attacker_eps)
    print(f"\n🔹 Candidate cross-access: {len(candidates)} endpoint")
    if not candidates:
        print("  Tidak ada kandidat yang ditemukan. Proses selesai.")
        return

    atk_sess = make_session(atk_cookies, base_url)
    print(f"\n🔹 Memeriksa {len(candidates)} kandidat dengan sesi Attacker...")
    findings = []
    for i, ep in enumerate(candidates):
        print(f"  Testing [{i+1}/{len(candidates)}]: {ep.method} {ep.path} {ep.query}")
        result = probe_with_session(atk_sess, ep, base_url)
        vulnerable = isinstance(result.get("status"), int) and 200 <= result["status"] < 400
        findings.append({ "endpoint": asdict(ep), "result": result, "vulnerable": vulnerable })

    vuln_findings = [f for f in findings if f["vulnerable"]]
    print(f"\n✨ Ditemukan {len(vuln_findings)} potensi kerentanan!")

    report = {
        "base_url": base_url,
        "actors": {
            "attacker": { "username": attacker_user },
            "victim": { "username": victim_user }
        },
        "summary": {
            "total_attacker_eps": len(all_attacker_eps),
            "total_victim_eps": len(all_victim_eps),
            "candidates_cross_access": len(candidates),
            "vulnerabilities_found": len(vuln_findings),
        },
        "findings": vuln_findings
    }
    report["tested_at"] = datetime.now().isoformat()
    
    report_json_path = os.path.join(reports_dir, f"{base_filename}.json")
    html_path = os.path.join(reports_dir, f"{base_filename}.html")
    
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"✅ Laporan JSON ditulis ke {report_json_path}")

    html_report = render_html(report)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_report)
    print(f"✅ Laporan HTML ditulis ke {html_path}")

def main():
    """Fungsi utama untuk parsing argumen dan menjalankan scan."""
    formatter = argparse.ArgumentDefaultsHelpFormatter

    parser = argparse.ArgumentParser(
        description="🚀 Alat pemindai IDOR/BAC otomatis dengan crawling berbasis Selenium.",
        epilog="""
Contoh Penggunaan:
  1. Scan dengan password lengkap:
     python %(prog)s -u http://127.0.0.1:5000 -au attacker -ap password -vu victim -vp password

  2. Scan di mana akun attacker tidak memiliki password:
     python %(prog)s -u http://target.com -au attacker -vu admin -vp adminpass
""",
        formatter_class=formatter
    )
    
    required_args = parser.add_argument_group('Argumen Wajib')
    required_args.add_argument(
        "-u", "--url", 
        required=True, 
        metavar='URL_TARGET',
        help="URL dasar dari aplikasi web yang akan diuji."
    )
    required_args.add_argument(
        "-au", "--attacker-user", 
        required=True, 
        metavar='NAMA_USER',
        help="Username untuk akun penyerang (privilese rendah)."
    )
    required_args.add_argument(
        "-vu", "--victim-user", 
        required=True, 
        metavar='NAMA_USER',
        help="Username untuk akun korban (privilese tinggi)."
    )
    
    optional_args = parser.add_argument_group('Argumen Opsional')
    optional_args.add_argument(
        "-ap", "--attacker-pass", 
        default="", 
        metavar='PASSWORD',
        help="Password untuk akun penyerang."
    )
    optional_args.add_argument(
        "-vp", "--victim-pass", 
        default="", 
        metavar='PASSWORD',
        help="Password untuk akun korban."
    )

    args = parser.parse_args()
    
    run(
        base_url=args.url,
        attacker_user=args.attacker_user,
        attacker_pass=args.attacker_pass,
        victim_user=args.victim_user,
        victim_pass=args.victim_pass
    )

if __name__ == "__main__":
    main()