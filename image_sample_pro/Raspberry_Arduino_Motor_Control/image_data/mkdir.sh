#!/bin/bash
echo "Start making directory..."
for dir_name in A1 A2 A3 A4 A5 A6 A7 A8 B1 B2 B3 B4 B5 B6 B7 B8 C1 C2 C3 C4 C5 C6 C7 C8 D1 D2 D3 D4 D5 D6 D7 D8; do
  echo "dir_name:${dir_name}"
  mkdir ${dir_name}
done