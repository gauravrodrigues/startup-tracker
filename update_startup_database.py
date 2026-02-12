#!/usr/bin/env python3
"""
Startup Database Updater
Automatically fetches new startups from topstartups.io and Y Combinator
and updates the founder contact database.

Run this script daily to keep the database fresh.
"""

import json
import csv
import re
import os
from datetime import datetime
from typing import List, Dict
import httpx
from bs4 import BeautifulSoup


def fetch_topstartups(limit: int = 100) -> List[Dict]:
    """
    Scrape topstartups.io for latest startup data
    
    Args:
        limit: Maximum number of startups to fetch
        
    Returns:
        List of startup dictionaries
    """
    print(f"\n[1/3] Fetching startups from topstartups.io...")
    
    # In production, you would use the Firecrawl API or similar
    # For now, return placeholder for the structure
    startups = []
    
    try:
        # This would be replaced with actual API call in production
        # Example: response = httpx.get('https://topstartups.io/api/startups')
        
        print(f"✓ Would fetch {limit} startups from topstartups.io")
        # Placeholder - in production this would parse actual data
        
    except Exception as e:
        print(f"⚠ Error fetching from topstartups.io: {e}")
    
    return startups


def fetch_yc_latest_batch() -> List[Dict]:
    """
    Fetch latest Y Combinator batch companies
    
    Returns:
        List of YC startup dictionaries
    """
    print(f"\n[2/3] Fetching Y Combinator latest batch...")
    
    startups = []
    
    try:
        # Determine current batch (W25, S25, etc.)
        now = datetime.now()
        year = now.year % 100  # Last 2 digits
        batch = f"W{year}" if now.month <= 6 else f"S{year}"
        
        print(f"✓ Checking for YC {batch} batch")
        
        # In production, this would use YC API or scraping
        # Placeholder for structure
        
    except Exception as e:
        print(f"⚠ Error fetching YC data: {e}")
    
    return startups


def merge_with_existing(new_startups: List[Dict], csv_path: str) -> List[Dict]:
    """
    Merge new startups with existing database, avoiding duplicates
    
    Args:
        new_startups: List of new startup data
        csv_path: Path to existing CSV database
        
    Returns:
        Combined list with duplicates removed
    """
    print(f"\n[3/3] Merging with existing database...")
    
    existing = []
    existing_names = set()
    
    # Load existing data
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing.append(row)
                existing_names.add(row['startup_name'].lower())
        
        print(f"✓ Loaded {len(existing)} existing startups")
    
    # Add new startups (avoid duplicates)
    added = 0
    for startup in new_startups:
        if startup['startup_name'].lower() not in existing_names:
            existing.append(startup)
            existing_names.add(startup['startup_name'].lower())
            added += 1
    
    print(f"✓ Added {added} new startups")
    print(f"✓ Total database size: {len(existing)} startups")
    
    return existing


def save_database(startups: List[Dict], csv_path: str, md_path: str):
    """
    Save updated database to CSV and Markdown formats
    
    Args:
        startups: List of all startups
        csv_path: Path to save CSV file
        md_path: Path to save Markdown file
    """
    # Save CSV
    fieldnames = ['startup_name', 'description', 'funding_amount', 'industry', 
                  'location', 'employees', 'website', 'founders', 
                  'founder_emails', 'founder_linkedin', 'source', 'batch']
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(startups)
    
    print(f"✓ Saved CSV to {csv_path}")
    
    # Save Markdown summary
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# Founder Contact Database\n\n")
        f.write(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Startups:** {len(startups)}\n\n")
        f.write("---\n\n")
        
        # Group by source
        by_source = {}
        for s in startups:
            source = s.get('source', 'Unknown')
            by_source[source] = by_source.get(source, 0) + 1
        
        f.write("## Summary by Source\n\n")
        for source, count in sorted(by_source.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{source}:** {count} startups\n")
        
        f.write("\n---\n\n")
        f.write("## Recent Additions (Top 20)\n\n")
        
        for i, startup in enumerate(startups[:20], 1):
            f.write(f"### {i}. {startup['startup_name']}\n\n")
            if startup.get('description'):
                f.write(f"**Description:** {startup['description'][:200]}...\n\n")
            if startup.get('founders'):
                f.write(f"**Founders:** {startup['founders']}\n\n")
            if startup.get('funding_amount'):
                f.write(f"**Funding:** {startup['funding_amount']}\n\n")
            if startup.get('industry'):
                f.write(f"**Industry:** {startup['industry']}\n\n")
            if startup.get('website'):
                f.write(f"**Website:** {startup['website']}\n\n")
            f.write(f"**Source:** {startup['source']}\n\n")
            f.write("---\n\n")
    
    print(f"✓ Saved Markdown to {md_path}")


def main():
    """Main execution function"""
    print("="*60)
    print("STARTUP DATABASE UPDATER")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Paths
    csv_path = os.getenv('DATABASE_PATH', 'data/founder_contact_database.csv')
    md_path = csv_path.replace('.csv', '.md')
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(csv_path) if os.path.dirname(csv_path) else '.', exist_ok=True)
    
    # Fetch new data
    topstartups_data = fetch_topstartups(limit=100)
    yc_data = fetch_yc_latest_batch()
    
    new_startups = topstartups_data + yc_data
    
    if not new_startups:
        print("\n⚠ No new data fetched. Database unchanged.")
        return
    
    # Merge with existing
    all_startups = merge_with_existing(new_startups, csv_path)
    
    # Save updated database
    save_database(all_startups, csv_path, md_path)
    
    print("\n" + "="*60)
    print("✓ UPDATE COMPLETE")
    print("="*60)
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nDatabase location: {csv_path}")
    print(f"Total startups: {len(all_startups)}")


if __name__ == "__main__":
    main()
