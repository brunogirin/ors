#!/bin/sh
scp V0p2_Main.cpp.hex devors:~/
scp avrdude.conf devors:~/

ssh devors '/usr/bin/avrdude -Cavrdude.conf -v -v -v -v -patmega328p -carduino -P/dev/ttyUSB0 -b4800 -D -Uflash:w:V0p2_Main.cpp.hex:i'
