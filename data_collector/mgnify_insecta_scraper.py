"""MGnify Insecta biome data scraper.

This script automates the collection of sample run metadata for Insecta-related
biomes from the MGnify API. It produces a CSV containing the host scientific
name, run accession (Run ID), and experiment type for all analysed runs linked
to samples within the following biomes:

* root:Host-associated:Insecta
* root:Host-associated:Insecta:Digestive system

Usage
-----
python mgnify_insecta_scraper.py --output insecta_runs.csv
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.parse import quote

import requests

BASE_URL = "https://www.ebi.ac.uk/metagenomics/api/v1"
DEFAULT_OUTPUT = "insecta_runs.csv"
PAGE_SIZE = 100
REQUEST_TIMEOUT = (5, 30)  # (connect, read) seconds
MAX_RETRIES = 3
RETRY_BACKOFF = 2.5  # seconds
RATE_LIMIT_DELAY = 0.2  # delay between page fetches

BIOME_LINEAGES: Dict[str, str] = {
    "root:Host-associated:Insecta": "Insecta (excl. sub-lineages)",
    "root:Host-associated:Insecta:Digestive system": "Insecta – Digestive system",
}


@dataclass
class SampleRecord:
    biome_lineage: str
    biome_name: str
    sample_accession: str
    host_scientific_name: Optional[str]


@dataclass
class RunRecord:
    sample_accession: str
    run_accession: str
    experiment_type: Optional[str]


class MGnifyClient:
    """Lightweight helper around the MGnify JSON:API endpoints."""

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or requests.Session()

    def _request(self, method: str, url: str, *, params: Optional[Dict] = None) -> Dict:
        last_error: Optional[Exception] = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self.session.request(
                    method,
                    url,
                    params=params,
                    timeout=REQUEST_TIMEOUT,
                    headers={"User-Agent": "MGnifyInsectaScraper/1.0"},
                )
                response.raise_for_status()
                return response.json()
            except requests.RequestException as exc:
                last_error = exc
                if attempt == MAX_RETRIES:
                    break
                sleep_time = RETRY_BACKOFF * attempt
                print(
                    f"⚠️  Request failed ({exc}). Retrying in {sleep_time:.1f}s...",
                    file=sys.stderr,
                )
                time.sleep(sleep_time)
        raise RuntimeError(f"Failed to fetch {url}: {last_error}")

    def iter_biome_samples(
        self, biome_lineage: str, *, include_runs: bool = True
    ) -> Iterable[Tuple[List[Dict], List[Dict]]]:
        """Yield each page of samples (and optionally included runs) for a biome."""

        encoded_lineage = quote(biome_lineage, safe="")
        url = f"{BASE_URL}/biomes/{encoded_lineage}/samples"
        params: Optional[Dict] = {
            "page_size": PAGE_SIZE,
            "include": "runs" if include_runs else None,
        }

        while url:
            page = self._request("GET", url, params=params)
            samples = page.get("data", [])
            included = page.get("included", []) if include_runs else []
            yield samples, included

            next_url = page.get("links", {}).get("next")
            url = next_url
            params = None  # subsequent pages already include query params in URL
            time.sleep(RATE_LIMIT_DELAY)

    def fetch_sample_runs(self, runs_url: str) -> List[Dict]:
        """Fetch all runs for a given sample via the dedicated runs endpoint."""

        url = runs_url
        params = None
        runs: List[Dict] = []
        while url:
            page = self._request("GET", url, params=params)
            runs.extend(page.get("data", []))
            url = page.get("links", {}).get("next")
            params = None
            time.sleep(RATE_LIMIT_DELAY)
        return runs


def extract_host_scientific_name(sample: Dict) -> Optional[str]:
    metadata = sample.get("attributes", {}).get("sample-metadata", [])
    for entry in metadata:
        key = entry.get("key", "").strip().lower()
        if key == "host scientific name":
            return entry.get("value")
    return None


def build_run_index(included: List[Dict]) -> Dict[str, List[Dict]]:
    run_map: Dict[str, List[Dict]] = {}
    for item in included:
        if item.get("type") != "runs":
            continue
        sample_info = item.get("relationships", {}).get("sample", {}).get("data")
        if not sample_info:
            continue
        sample_id = sample_info.get("id")
        run_map.setdefault(sample_id, []).append(item)
    return run_map


def collect_records(client: MGnifyClient) -> List[Dict[str, Optional[str]]]:
    records: List[Dict[str, Optional[str]]] = []

    for lineage, biome_name in BIOME_LINEAGES.items():
        print(f"📥 Fetching samples for biome: {biome_name} ({lineage})")

        for samples, included in client.iter_biome_samples(lineage):
            if not samples:
                continue

            run_index = build_run_index(included)

            for sample in samples:
                sample_id = sample.get("id")
                attributes = sample.get("attributes", {})
                sample_accession = attributes.get("accession", sample_id)
                host_name = extract_host_scientific_name(sample)

                sample_record = SampleRecord(
                    biome_lineage=lineage,
                    biome_name=biome_name,
                    sample_accession=sample_accession,
                    host_scientific_name=host_name,
                )

                runs = run_index.get(sample_id, [])

                if not runs and sample.get("relationships", {}).get("runs", {}).get(
                    "links"
                ):
                    runs_link = sample["relationships"]["runs"]["links"].get("related")
                    if runs_link:
                        fetched_runs = client.fetch_sample_runs(runs_link)
                        runs = []
                        for run in fetched_runs:
                            run_attrs = run.get("attributes", {})
                            runs.append(
                                {
                                    "id": run.get("id"),
                                    "attributes": run_attrs,
                                    "relationships": run.get("relationships", {}),
                                }
                            )

                if not runs:
                    # No associated runs, skip sample (only analysed runs requested).
                    continue

                for run in runs:
                    run_attrs = run.get("attributes", {})
                    run_accession = run_attrs.get("accession") or run.get("id")
                    experiment_type = run_attrs.get("experiment-type")

                    records.append(
                        {
                            "biome_lineage": sample_record.biome_lineage,
                            "biome_name": sample_record.biome_name,
                            "sample_accession": sample_record.sample_accession,
                            "host_scientific_name": sample_record.host_scientific_name,
                            "run_accession": run_accession,
                            "experiment_type": experiment_type,
                        }
                    )

    if not records:
        raise RuntimeError(
            "No run records were collected. Please verify the API availability."
        )

    # Deduplicate records based on (sample, run)
    seen = set()
    unique_records: List[Dict[str, Optional[str]]] = []
    for record in records:
        key = (record["sample_accession"], record["run_accession"])
        if key in seen:
            continue
        seen.add(key)
        unique_records.append(record)

    return unique_records


def write_csv(records: List[Dict[str, Optional[str]]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "biome_lineage",
        "biome_name",
        "sample_accession",
        "host_scientific_name",
        "run_accession",
        "experiment_type",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in records:
            writer.writerow(row)

    print(f"✅ CSV saved to {output_path}")
    print(f"   Total records: {len(records)}")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape MGnify Insecta sample runs (host scientific name, run ID, experiment type)."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(DEFAULT_OUTPUT),
        help=f"Path to the CSV output file (default: {DEFAULT_OUTPUT}).",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    client = MGnifyClient()

    records = collect_records(client)
    write_csv(records, args.output)


if __name__ == "__main__":
    main()
