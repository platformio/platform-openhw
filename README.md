# OpenHW Group: development platform for [PlatformIO](http://platformio.org)

[![Build Status](https://github.com/platformio/platform-openhw/workflows/Examples/badge.svg)](https://github.com/platformio/platform-openhw/actions)

The OpenHW CV32E40P RISC-V core is the first open-source core for high-volume chips verified with the state-of-the-art process required for high-integrity, commercial SoCs.

* [Home](http://platformio.org/platforms/openhw) (home page in PlatformIO Platform Registry)
* [Documentation](http://docs.platformio.org/page/platforms/openhw.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = openhw
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/platformio/platform-openhw.git
board = ...
...
```

# Configuration

Please navigate to [documentation](http://docs.platformio.org/page/platforms/openhw.html).
