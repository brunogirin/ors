#!/bin/sh
git clone https://github.com/DamonHD/OpenTRV.git damonhd-opentrv
git clone https://github.com/DamonHD/OTRadioLink.git damonhd-otradiolink
git clone https://github.com/opentrv/OTProtocolCC.git opentrv-otprotocolcc
cd damonhd-opentrv
git checkout 20150803-DV
cd ../damonhd-otradiolink
git checkout 20150803-DV
cd ../opentrv-otprotocolcc
git checkout 20150803-DV

