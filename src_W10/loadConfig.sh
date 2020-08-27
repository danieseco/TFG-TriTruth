#!/bin/bash


if [ $# == 2 ]
then
	comPort=$1
	user=$2
else
	echo "${0}  <Puerto COM> <Id deportista>"
	echo "Introduzca puerto COM"
	read comPort
	echo "Introduzca ident de usuario"
	read user
fi

if [ -z ${TargetPath} ]
then
	TargetPath=`pwd`
fi

ampy -p /dev/ttyS${comPort} put ${TargetPath}/wireless.conf
ampy -p /dev/ttyS${comPort} put ${TargetPath}/connZone.conf
ampy -p /dev/ttyS${comPort} put ${TargetPath}/safeZone.conf

rm -f user.conf
echo $user >> user.conf
ampy -p /dev/ttyS${comPort} put user.conf

rm user.conf

echo "Proceso finalizado"