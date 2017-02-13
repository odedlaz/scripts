#!/usr/bin/zsh
set -e
echo "Unmounting iPhone..."
/usr/bin/fusermount -u /media/$USER/iPhone
echo "Unpairing iPhone..."
/usr/local/bin/idevicepair unpair
echo "Done!"
