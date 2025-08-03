import argparse
import csv
import json
from typing import List, Dict
from src.scraper.tender_scraper import scrape_all_tenders
from src.database.database import init_db, save_to_db

# Сохранить в файл JSON
def save_to_json(data: List[Dict], filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Сохранить в файл CSV
def save_to_csv(data: List[Dict], filename: str):
    if not data:
        return
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

# Основная точка входа CLI 
def main():
    parser = argparse.ArgumentParser(description="Scrape tenders from rostender.info")
    parser.add_argument("--max", type=int, default=100, help="Maximum number of tenders to scrape")
    parser.add_argument("--format", type=str, choices=["json", "csv"], default="json", help="Output file format")
    parser.add_argument("--output", type=str, default="tenders.json", help="Output filename")

    args = parser.parse_args()

    print("Initializing database...")
    init_db()

    print(f"Scraping up to {args.max} tenders...")
    tenders = scrape_all_tenders(args.max)
    print(f"Scraped {len(tenders)} tenders.")

    # Сохранить в БД
    print("Saving to database...")
    save_to_db(tenders)

    # Сохранить в файл (json/csv)
    if args.format == "json":
        save_to_json(tenders, args.output)
    else:
        save_to_csv(tenders, args.output)

    print(f"Saved to {args.output} and tenders.db")

if __name__ == "__main__":
    main()
