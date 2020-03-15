# ncov2019-updates

A simple Raspberry Pi python program to show nCOV2019 updates, two popular datasources are included.

## Usage:
1. clone lcddriver from https://github.com/the-raspberry-pi-guy/lcd/
2. modified for my LCD1602 address 0x3f (default is 0x2f)
3. put this file in
4. connect LCD to 40-pin GPIO: GND - PIN.9, Vcc - PIN.4, SCL - PIN.5, SDA - PIN.3
5. connect to network, easiest way is via on-board ethernet
6. python ncp.py

Note: It is too trouble to display Chinese on LCD1602, converted to Pinyin instead.