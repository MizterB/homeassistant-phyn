# homeassistant-phyn

Home Assistant custom component for interfacing with [Phyn](https://www.phyn.com) Smart Water Assistant.

This integration currently provides the following capabilities:

- Daily water usage (compatible with Energy dashboard)
- Average water temperature, pressure, and flow (realtime not available)
- Shutoff valve control

# Installation via HACS

This custom component can be integrated into [HACS](https://github.com/hacs/integration), so you can track future updates. If you have do not have have HACS installed, please see [their installation guide](https://hacs.xyz/docs/installation/manual).

1. Select HACS from the left-hand navigation menu.

2. Click _Integrations_.

3. Click the three dots in the upper right-hand corner and select _Custom Repositories_.

4. Paste "https://github.com/MizterB/homeassistant-phyn" into _Repository_, select "Integration" as _Category_, and click Add.

5. Close the Custom repositories dialog after it updates with the new integration.

6. "Phyn Smart Water Assistant" will appear in your list of repositories. Click to open, click the following Download buttons.

# Configuration

Add the following to your `configuration.yaml`:

```yaml
climate:
  - platform: infinitude
    host: <infinitude_hostname_or_ip>
    port: <optional, defaults to 3000>
    zone_names:
      - Custom Zone Name 1
      -
      - Custom Zone Name 3
      - ...
```

Custom zone names are optional, and are applied in ascending order (zones 1-8). If a blank name is provided (like in the second entry above), the zone name is retrieved from the thermostat itself.

## Changelog

_0.7.2_

- Updated installation instructions for HACS
- Include version number in manifest

_0.7.1_

- Extend ClimateEntity, rather than ClimateDevice

_0.7_

- Submit changes via POST to be compatible with latest Infinitude API ([see commit](https://github.com/MizterB/infinitude/commit/a0c3b7a58c1c3535a0811001bcfed2c43c672906))
- Handle timezone offsets being inconsistently passed in localTime.
- Make custom zone names optional, and with ability to only override specific zones

_0.6_

- Rewritten for compatibility with the new climate spec in HA .96
- New presets available to quickly change activities and manage hold settings:
  - 'Scheduled' preset restores the currently scheduled activity
  - 'Activity' presets override the currently scheduled activity until the next schedule change
  - 'Override' preset holds any setting changes until the next schedule change (automatically enabled on temperature & fan changes)
  - 'Hold' preset holds any setting changes indefinitely
- Service set_hold_mode is mostly replaced by presets, but can still be used for setting specific 'hold until' times

_0.5_

- New service 'infinitude.set_hold_mode' enables changing activities and corresponding hold settings.

_0.4_

- Added manifest.json
- Fixed temperature setting reversal while on Auto mode(thanks @ccalica!)

_0.3_

- Safely handle updates of values that might not exist on all thermostats
- Provide ability to override zone names

_0.2_

- Updated constants to be compatible with HA .89

_0.1_

- Initial release
