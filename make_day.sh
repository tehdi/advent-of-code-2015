#!/bin/bash

dayId=day$1

mkdir $dayId
touch $dayId/input.txt
touch $dayId/test_input.txt
cp main.py $dayId/main.py
