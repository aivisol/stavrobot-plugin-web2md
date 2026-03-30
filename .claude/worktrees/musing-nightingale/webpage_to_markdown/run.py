#!/usr/bin/env -S uv run
# /// script
# dependencies = ["requests"]
# ///

import json
import sys
import time
from pathlib import Path

import requests

APIFY_BASE = "https://api.apify.com/v2"
ACTOR_ID = "extremescrapes~webpage-to-markdown"
POLL_INTERVAL = 5  # seconds between status checks
MAX_WAIT = 270     # seconds total (fits within 5-min async timeout)


def main() -> None:
    config = json.loads(Path("../config.json").read_text())
    apify_token = config["apify_token"]
    params = json.load(sys.stdin)
    urls = [u.strip() for u in params["urls"].split(",") if u.strip()]

    headers = {"Authorization": f"Bearer {apify_token}"}

    # Launch the actor run
    run_resp = requests.post(
        f"{APIFY_BASE}/acts/{ACTOR_ID}/runs",
        headers=headers,
        json={"startUrls": [{"url": u} for u in urls], "maxRequestsPerCrawl": 100},
        timeout=30,
    )
    run_resp.raise_for_status()
    run_data = run_resp.json()["data"]
    run_id = run_data["id"]
    default_dataset_id = run_data["defaultDatasetId"]

    # Poll until the run finishes
    deadline = time.monotonic() + MAX_WAIT
    status = run_data.get("status", "RUNNING")
    while status not in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
        if time.monotonic() >= deadline:
            raise RuntimeError(f"Timed out waiting for Apify run {run_id}")
        time.sleep(POLL_INTERVAL)
        status_resp = requests.get(
            f"{APIFY_BASE}/acts/{ACTOR_ID}/runs/{run_id}",
            headers=headers,
            timeout=15,
        )
        status_resp.raise_for_status()
        status = status_resp.json()["data"]["status"]

    if status != "SUCCEEDED":
        raise RuntimeError(f"Apify run {run_id} ended with status: {status}")

    # Fetch the dataset output
    items_resp = requests.get(
        f"{APIFY_BASE}/datasets/{default_dataset_id}/items",
        headers=headers,
        params={"format": "json"},
        timeout=30,
    )
    items_resp.raise_for_status()
    items = items_resp.json()

    if not items:
        raise RuntimeError("Apify actor returned no output.")

    results = [{"url": item.get("url", ""), "markdown": item.get("markdown", "")} for item in items]
    json.dump({"results": results}, sys.stdout)


main()
