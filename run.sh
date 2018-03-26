#!/bin/bash

if [[ $1 == "zip" ]]; then
	zip xkubis13.zip solution.py solution_sat.py doc.pdf install.sh
	exit
fi

python3 solution.py