#!/bin/sh

service apache2 start

service mysql start

mysql -u root -ppany8491 -e "CREATE DATABASE chatEval"
mysql -u root -ppany8491 chatEval < chatEval.sql
tail