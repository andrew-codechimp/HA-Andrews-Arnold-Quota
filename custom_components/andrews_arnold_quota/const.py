"""Constants for andrews_arnold_quota."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

MIN_HA_VERSION = "2025.10"


DOMAIN = "andrews_arnold_quota"
NAME = "Andrews & Arnold Quota"
MANUFACTURER = "@Andrew-CodeChimp"
ATTRIBUTION = "Data provided by https://www.aa.net.uk"
API_URL = "https://chaos2.aa.net.uk/broadband/"
