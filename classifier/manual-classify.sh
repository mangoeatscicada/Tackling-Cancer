#!/bin/bash

mkdir -p cancer blood other
echo -n "Press a key, (C)ancer, (B)lood, (O)ther, (Q)uit: "

for jpg in *.jpg; do
	CMD="display -title ${jpg} -immutable ${jpg}"
	${CMD} &
	sleep 0.2
	wmctrl -a Terminal
	read -s -n1
	pkill -f "${CMD}"

	case ${REPLY} in
		q)	echo Quitting; exit 0 
			;;
		c)	git mv ${jpg} ../images/extract-automatic/cancer
			;;
		b)	git mv ${jpg} ../images/extract-automatic/blood
			;;
		o)	git mv ${jpg} ../images/extract-automatic/other
			;;
	esac

done
