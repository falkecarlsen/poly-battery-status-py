# poly-battery-status-py
Generates a pretty status-bar string for multi-battery systems on Linux. A port of [cogitantium/poly-battery-status](https://github.com/cogitantium/poly-battery-status).

To be upstreamed through AUR on [i3blocks-contrib](https://github.com/vivien/i3blocks-contrib).

## Features
- Uses sysfs for gathering batteries and values on these
- Calculates time-to-depleted and time-to-full from current power-draw
- Takes battery-thresholds, such as [TLP](https://github.com/linrunner/TLP), into account when calculating time-to-_full_. Defaults to 100% but is overrideable through arguments.
- Omits time-to-* when passive (specifically when sysfs delivers a status of `Unknown`)
- Takes a formatting string for percentage. Default is `.2%` rendering a percentage with two decimals.

## Usage
To run with defaults:
```
python poly_bay.py
```

Arguments are positional and parsed in a simple manner.
To set battery-threshold, pass a float as first arguments:
```
python poly_bat.py 0.42
```

To set a formatting string for percentage, pass a Python formatting string as the second argument (note that threshold passed is default):
```
python poly_bat.py 1.0 .0%
```
