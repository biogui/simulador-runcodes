#!/bin/bash
mkdir ~/rcsimulator
mv rcsimulator.py ~/rcsimulator
chmod 744 ~/rcsimulator/rcsimulator.py
sudo ln -s ~/rcsimulator/rcsimulator.py /usr/bin/rcsim
mv setup.sh ~/rcsimulator