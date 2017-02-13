#!/usr/bin/zsh
set -e
echo "Pairing iPhone..."
/usr/local/bin/idevicepair pair
echo "Mounting iPhone..."
/usr/local/bin/ifuse /media/$USER/iPhone
echo "Done!"
