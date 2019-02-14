#!/usr/bin/expect
cd [file dirname $argv0]
spawn sh ./mac.sh
#set AdminPassword "tanshiji"
#
#spawn scp app.conf admin@39.108.12.40:/home/admin/go/src/air-quality-predict/conf/
#expect "password"
#send "$AdminPassword\r"
#
#spawn ssh admin@39.108.12.40
#expect "password"
#send "$AdminPassword\r"
#
#expect "admin"
#send "ls\r"
#send "exit\r"

interact

