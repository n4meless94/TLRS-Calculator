
import json
import threading
import queue
import urllib.request
import re
import datetime as dt
from pathlib import Path
from typing import Dict, Optional, Callable, Any

# Define cache schema version
CACHE_VERSION = 1

class HolidayService:
    def __init__(self, cache_dir: str = "."):
        self.cache_dir = Path(cache_dir)
        self.base_url = "https://sabah.gov.my/ms/public-holidays"
        
    def get_cache_path(self, year: int) -> Path:
        return self.cache_dir / f"holiday_cache_{year}.json"

    def load_from_cache(self, year: int) -> Optional[Dict[str, Any]]:
        path = self.get_cache_path(year)
        if not path.exists():
            return None
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # Validate schema
            if data.get("version") != CACHE_VERSION:
                return None
            if data.get("year") != year:
                return None
                
            return data
        except Exception:
            return None

    def save_to_cache(self, year: int, holidays_dict: Dict[dt.date, str]):
        path = self.get_cache_path(year)
        data = {
            "version": CACHE_VERSION,
            "year": year,
            "state": "Sabah",
            "fetched_at": dt.datetime.now().isoformat(),
            "holidays": {d.isoformat(): name for d, name in holidays_dict.items()}
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Failed to save cache: {e}")

    def fetch_holidays_sync(self, year: int) -> Dict[dt.date, str]:
        """Blocking fetch from URL."""
        # This logic parses the Sabah gov website
        # Reusing the parsing logic from tlrs.py (adapted slightly)
        
        try:
            with urllib.request.urlopen(self.base_url, timeout=10) as resp:
                body = resp.read().decode("utf-8", errors="ignore")
        except Exception as e:
            raise RuntimeError(f"Network error: {e}")

        # Parsing logic (Same as original but more robust if needed)
        holidays_dict = {}
        
        # Remove script/style
        body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL | re.IGNORECASE)
        body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL | re.IGNORECASE)
        
        # Date Pattern: 1 January 2026
        date_pattern = r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})'
        
        lines = body.split('\n')
        for i, line in enumerate(lines):
            date_match = re.search(date_pattern, line)
            if date_match:
                date_str = date_match.group(0)
                try:
                    parsed_date = dt.datetime.strptime(date_str, "%d %B %Y").date()
                except ValueError:
                    continue
                
                if parsed_date.year == year:
                    # Find name (look back 5 lines)
                    holiday_name = "Public Holiday" # Default
                    for j in range(max(0, i - 5), i + 1):
                        check_line = lines[j]
                        clean_line = re.sub(r'<[^>]+>', '', check_line)
                        clean_line = re.sub(r'\s+', ' ', clean_line).strip()
                        
                        # Exclude date strings
                        if date_str in clean_line: continue
                        if re.search(r'\d{1,2}\s+[A-Za-z]+', clean_line): continue # Ignore "30 May", "1 May"
                        
                        if len(clean_line) < 5 or clean_line.isdigit(): continue
                        if clean_line.lower() in ['cuti', 'tarikh', 'edit', 'holiday', 'date']: continue
                        
                        if clean_line:
                            holiday_name = clean_line
                            break
                    
                    # Clean name
                    holiday_name = re.sub(r'\s+\d{4}$', '', holiday_name).strip()
                    # Remove any remaining date-like prefixes
                    holiday_name = re.sub(r'^\d{1,2}\s+[A-Za-z]+\s*', '', holiday_name)
                    
                    if parsed_date in holidays_dict:
                        if holiday_name not in holidays_dict[parsed_date]:
                            holidays_dict[parsed_date] += f" / {holiday_name}"
                    else:
                        holidays_dict[parsed_date] = holiday_name
                        
        if not holidays_dict:
            raise RuntimeError("No holidays found for this year (parsing failed or no data).")
            
        return holidays_dict


    def fetch_holidays_async(
        self, 
        year: int, 
        on_success: Callable[[Dict[dt.date, str], str], None], 
        on_error: Callable[[str], None],
        force_refresh: bool = False
    ):
        """
        Starts a thread to fetch holidays.
        on_success(holidays_dict, source)
        on_error(error_message)
        """
        def worker():
            # 1. Try Cache first (unless forced)
            if not force_refresh:
                cached = self.load_from_cache(year)
                if cached:
                    holidays = {dt.date.fromisoformat(d): n for d, n in cached["holidays"].items()}
                    fetched_at = cached.get("fetched_at", "Unknown")
                    # Post to main thread (simulated via direct callback for now, 
                    # but caller should ensure thread safety or use root.after)
                    # Ideally we pass a queue, but here we just call the callback 
                    # and let the UI handle the "call from thread" issue via queue or after_idle
                    # best practice: just run logic here, UI wrapper handles the dispatch
                    
                    # We will return data, caller handles threading context
                    return ("success", holidays, f"Cache ({fetched_at})")

            # 2. Fetch from Network
            try:
                holidays = self.fetch_holidays_sync(year)
                self.save_to_cache(year, holidays)
                return ("success", holidays, "Live Fetch")
            except Exception as e:
                return ("error", str(e))

        def thread_target():
            status, *args = worker()
            if status == "success":
                on_success(args[0], args[1])
            else:
                on_error(args[0])

        threading.Thread(target=thread_target, daemon=True).start()

