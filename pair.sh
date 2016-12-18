#!/bin/bash
set -e
echo "Pairing iPhone..."
idevicepair pair
echo "Mounting iPhone..."
ifuse /media/iPhone
echo "Done!"
