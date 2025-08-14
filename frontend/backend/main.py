from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Tuple, Union
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # keep private

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Allow frontend requests (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

table_name = "vdot_data"


class SubmitPayload(BaseModel):
    value: str


# --- Time parsing helpers ---

def parse_time_to_seconds(value: str) -> Optional[float]:
    # Accept formats: "25" (minutes), "25.5" (minutes), "mm:ss", "hh:mm:ss"
    s = value.strip()
    if not s:
        return None
    if ":" in s:
        parts = s.split(":")
        try:
            parts = [float(p) for p in parts]
        except ValueError:
            return None
        if len(parts) == 2:
            minutes, seconds = parts
            return minutes * 60 + seconds
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return hours * 3600 + minutes * 60 + seconds
        return None
    # No colon: treat as minutes (allow float)
    try:
        minutes = float(s)
        return minutes * 60
    except ValueError:
        return None


def try_parse_db_time_to_seconds(raw: Union[str, int, float]) -> Optional[float]:
    if raw is None:
        return None
    # If string, try mm:ss or hh:mm:ss, otherwise try float minutes
    if isinstance(raw, str):
        if ":" in raw:
            return parse_time_to_seconds(raw)
        # string number: treat as minutes
        try:
            return float(raw) * 60
        except ValueError:
            return None
    # Numeric: decide likely unit by magnitude
    try:
        number = float(raw)
    except Exception:
        return None
    # Heuristic: typical 5k seconds 800-3600; minutes 13-60
    if number >= 100:  # likely seconds
        return number
    # else assume minutes
    return number * 60


def query_row_closest_by_race_5km(value: str) -> Optional[Dict[str, Any]]:
    # Convert the input to seconds
    target_seconds = parse_time_to_seconds(value)
    if target_seconds is None:
        return None

    client = supabase
    if client is None:
        # Supabase environment is not configured
        return None

    # Fetch rows where race_5km is not null. Depending on your data size,
    # you may want to further restrict or paginate the query.
    try:
        # Fetch rows; we'll filter out null race_5km values in Python for simplicity
        response = client.table(table_name).select("*").limit(1000).execute()
    except Exception as e:
        print(f"Supabase query failed: {e}", flush=True)
        return None

    rows: List[Dict[str, Any]] = getattr(response, "data", []) or []
    if not rows:
        return None

    best: Tuple[float, Optional[Dict[str, Any]]] = (float("inf"), None)
    for row in rows:
        raw = row.get("Estimated 5km")
        seconds = try_parse_db_time_to_seconds(raw)
        if seconds is None:
            continue
        dist = abs(seconds - target_seconds)
        if dist < best[0]:
            best = (dist, row)

    return best[1] if best[1] is not None else None


@app.post("/submit")
def submit(payload: SubmitPayload):
    def pick_first_existing(row: Dict[str, Any], keys: List[str]) -> Optional[Any]:
        for k in keys:
            if k in row and row[k] is not None:
                return row[k]
        return None

    def select_fields(row: Dict[str, Any]) -> Dict[str, Any]:
        # Normalize and expose only the requested fields
        return {
            "vdot": pick_first_existing(row, ["vdot"]),
            "race_half_marathon": pick_first_existing(
                row, ["Estimated Half marathon"]
            ),
            "easy_pace_per_mile": pick_first_existing(
                row, ["Easy_long_pace_Mile"]
            ),
            "easy_pase_per_km": pick_first_existing(
                row, ["Easy_long_pace_km"],
            ),
            "marathon_pace_per_mile": pick_first_existing(
                row, ["marathon_pace_Mile"],
            ),
            "marathon_pace_per_km": pick_first_existing(
                row, ["Marathon_pace_km"],
            ),
            "threshold_pace_per_km": pick_first_existing(
                row, ["Threshold_pace_km"],
            ),
            "threshold_pace_per_mile": pick_first_existing(
                row, ["Threshold_pace_Mile"],
            ),
        }

    row = query_row_closest_by_race_5km(payload.value)
    if row is None:
        print(f"No row found near race_5km ≈ {payload.value}", flush=True)
        return {"received": payload.value, "row": None}

    selected = select_fields(row)
    # Print only the requested fields in a readable form
    printable = (
        f"vdot={selected.get('vdot')}, "
        f"race_half_marathon={selected.get('race_half_marathon')}, "
        f"easy_pace_per_mile={selected.get('easy_pace_per_mile')}, "
        f"easy_pase_per_km={selected.get('easy_pase_per_km')}, "
        f"marathon_pace_per_mile={selected.get('marathon_pace_per_mile')}, "
        f"marathon_pace_per_km={selected.get('marathon_pace_per_km')}, "
        f"threshold_pace_per_km={selected.get('threshold_pace_per_km')}, "
        f"threshold_pace_per_mile={selected.get('threshold_pace_per_mile')}"
    )
    print(f"Closest row for race_5km ≈ {payload.value}: {printable}", flush=True)
    return {"received": payload.value, "row": selected}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)