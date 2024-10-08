"""Constants for andrews_arnold_quota."""

import json
from logging import Logger, getLogger
from pathlib import Path

LOGGER: Logger = getLogger(__package__)

MIN_HA_VERSION = "2024.5"

manifestfile = Path(__file__).parent / "manifest.json"
with open(file=manifestfile, encoding="UTF-8") as json_file:
    manifest_data = json.load(json_file)

DOMAIN = manifest_data.get("domain")
NAME = manifest_data.get("name")
VERSION = manifest_data.get("version")
ISSUEURL = manifest_data.get("issue_tracker")
MANUFACTURER = "@Andrew-CodeChimp"
ATTRIBUTION = "Data provided by https://www.aa.net.uk"
API_URL = "https://chaos2.aa.net.uk/broadband/"
