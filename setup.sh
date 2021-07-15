#!/bin/bash
chmod 744 ~/.rcSim/rcSim.py
sudo rm -rf /usr/bin/rcsim
sudo ln -s ~/.rcSim/rcSim.py /usr/bin/rcsim