#!/bin/bash

if [ -d rootfs ]; then
	echo "rootfs already extracted"
	exit 1
fi

if [ "$#" -ne 1 ]; then
	echo "usage $0 MOUNTED_ROOT"
	exit 1
fi

MOUNTED_ROOT=$1

if [ ! -d "$1" ]; then
	echo "$MOUNTED_ROOT does not exist"
	exit 1
fi

set -x

mkdir rootfs
cd $MOUNTED_ROOT
tar --preserve-permissions --preserve-order -c usr/include usr/lib usr/share lib opt/vc | tar -x -C $OLDPWD/rootfs
cd -
