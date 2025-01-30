# Home Assistant Oura Ring Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
[![Community Forum][forum-shield]][forum]

Home Assistant integration for Oura Ring that retrieves sleep, readiness, and activity scores.

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click the three dots in the top right corner
3. Select "Custom repositories"
4. Add this repository URL and select "Integration" as the category
5. Click "Install"

### Manual Installation

1. Download the latest release
2. Copy the `custom_components/oura` folder to your Home Assistant's `custom_components` folder
3. Restart Home Assistant

## Configuration

1. Obtain your Personal Access Token from [Oura Cloud Personal Access Tokens](https://cloud.ouraring.com/personal-access-tokens)
2. In Home Assistant, go to Configuration → Integrations
3. Click "+ ADD INTEGRATION"
4. Search for "Oura Ring"
5. Enter your Personal Access Token
6. Click Submit

## Available Sensors

This integration provides the following sensors:

- Sleep Score: Daily sleep quality score
- Readiness Score: Daily readiness score
- Activity Score: Daily activity score

Each sensor updates every 5 minutes by default.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

***

[releases-shield]: https://img.shields.io/github/release/0xvisualiris/ouraring-hass.svg
[releases]: https://github.com/0xvisualiris/ouraring-hass/releases
[commits-shield]: https://img.shields.io/github/commit-activity/y/0xvisualiris/ouraring-hass.svg
[commits]: https://github.com/0xvisualiris/ouraring-hass/commits/main
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/0xvisualiris/ouraring-hass.svg
