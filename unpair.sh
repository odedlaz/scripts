#!/bin/bash
set -e
echo "Unmounting iPhone..."
fusermount -u /media/iPhone
echo "Unpairing iPhone..."
idevicepair unpair
echo "Done!"
