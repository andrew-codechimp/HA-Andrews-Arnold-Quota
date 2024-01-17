# Home Assistant Andrews & Arnold Quota Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]

[![Community Forum][forum-shield]][forum]

_Integration to get broadband quota from [Andrews & Arnold](https://www.aa.net.uk)._

![Andrews & Arnold Device Info](https://github.com/andrew-codechimp/HA-Andrews-Arnold-Quota/blob/main/images/screenshot.png "Andrews & Arnold Device Info")

**This integration will set up the following platforms.**

| Platform | Description                                |
|----------|--------------------------------------------|
| `sensor` | Show info from Andrews & Arnold Quota API. |

## Sensors

| Sensor                                  | Description     |
|:----------------------------------------|-----------------|
| `sensor.andrews_arnold_monthly_quota`   | Monthly Quota   |
| `sensor.andrews_arnold_quota_remaining` | Quota Remaining |
| `sensor.andrews_arnold_quota_status`    | Quota Status    |

## Installation

### HACS

This integration can be installed directly via HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=andrew-codechimp&repository=HA-Andrews-Arnold-Quota&category=Integration)

Or  
Search for `Andrews & Arnold Quota` in HACS and install it under the "Integrations" category.  
Restart Home Assistant  
In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Andrews & Arnold Quota"  

### Manual Installation

<details>
<summary>Show detailed instructions</summary>

Installation via HACS is recommended, but a manual setup is supported.

1. Manually copy custom_components/andrews_arnold_quota folder from the latest release to custom_components folder in your config folder.
1. Restart Home Assistant.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Andrews & Arnold Quota"

</details>

## No Configuration Necessary

As long as you are connecting via Andrews & Arnold this API will automatically return the quota for the current connection.

Data is refreshed every 30 minutes.

<!---->

## Contributions are welcome!

If you want to contribute to this repository, please read the [Contribution guidelines](CONTRIBUTING.md)

## Disclaimer

This integration is in no way approved, endorsed or supported by Andrews & Arnold Ltd.

***

[andrews_arnold_quota]: https://github.com/andrew-codechimp/HA-Andrews-Arnold-Quota
[commits-shield]: https://img.shields.io/github/commit-activity/y/andrew-codechimp/HA-Andrews-Arnold-Quota.svg?style=for-the-badge
[commits]: https://github.com/andrew-codechimp/HA-Andrews-Arnold-Quota/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/t/custom-component-andrews-arnold-uk-broadband-quota/595491
[license-shield]: https://img.shields.io/github/license/andrew-codechimp/HA-Andrews-Arnold-Quota.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/andrew-codechimp/HA-Andrews-Arnold-Quota.svg?style=for-the-badge
[releases]: https://github.com/andrew-codechimp/HA-Andrews-Arnold-Quota/releases
