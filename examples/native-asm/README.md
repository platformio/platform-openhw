How to build PlatformIO based project
=====================================

1. [Install PlatformIO Core](http://docs.platformio.org/page/core.html)
2. Download [development platform with examples](https://github.com/platformio/platform-openhw/archive/develop.zip)
3. Extract ZIP archive
4. Run these commands:

```shell
# Change directory to example
$ cd platform-openhw/examples/native-asm

# Build project
$ pio run

# Upload bitstream
$ pio run --target upload_bitstream

# Upload firmware
$ pio run --target upload

# Clean build files
$ pio run --target clean
```
