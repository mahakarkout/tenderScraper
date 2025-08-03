import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import argparse
import json
import csv
import os

BASE_URL = "https://rostender.info"
LIST_URL = f"{BASE_URL}/extsearch"

def fetch_html(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_tenders(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    tender_articles = soup.select("article.tender-row")
    tenders = []

    for article in tender_articles:
        tender = {}

        tender["tender_id"] = article.get("id", "").strip()

        title_tag = article.select_one(".tender-info__description")
        tender["title"] = title_tag.get_text(strip=True) if title_tag else ""
        relative_url = title_tag.get("href") if title_tag else ""
        tender["url"] = f"{BASE_URL}{relative_url}" if relative_url else ""

        start_date = article.select_one(".tender__date-start")
        tender["start_date"] = start_date.get_text(strip=True).replace("от", "") if start_date else ""

        end_date = article.select_one(".tender__date-end .black")
        tender["end_date"] = end_date.get_text(strip=True) if end_date else ""

        end_time = article.select_one(".tender__countdown-container")
        tender["end_time"] = end_time.get_text(strip=True) if end_time else ""

        region_tag = article.select_one(".tender__region-link")
        tender["region"] = region_tag.get_text(strip=True) if region_tag else ""

        city_tag = article.select_one(".tender-address")
        tender["city"] = city_tag.get_text(strip=True) if city_tag else ""

        price_tag = article.select_one(".starting-price--price")
        tender["price"] = price_tag.get_text(strip=True) if price_tag else "—"

        categories = article.select(".list-branches__link")
        tender["categories"] = [c.get_text(strip=True) for c in categories]
        tender["category_urls"] = [BASE_URL + c.get("href") for c in categories if c.get("href")]

        tenders.append(tender)

    return tenders

def scrape_all_tenders(max_tenders: int = 100) -> List[Dict]:
    page = 1
    all_tenders = []

    while len(all_tenders) < max_tenders:
        url = f"{LIST_URL}?page={page}"
        html = fetch_html(url)
        tenders = parse_tenders(html)

        if not tenders:
            break  # No more pages

        remaining = max_tenders - len(all_tenders)
        all_tenders.extend(tenders[:remaining])

        if len(tenders) < 20:
            break  # Last page likely reached

        page += 1

    return all_tenders
