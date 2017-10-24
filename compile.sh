#!/bin/sh

cd build
cmake ..
make
cp pylibviso2.so ../pylibviso2
cd ..
