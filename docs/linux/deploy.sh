#!/usr/bin/expect
cd [file dirname $argv0]
set timeout 60
set ProjectName "air-quality-predict"
set AdminPassword "tanshiji"

spawn sh ./mac.sh
expect "WaitingGitFinish"

spawn scp -r /Users/quietsj/go/src/$ProjectName admin@39.108.12.40:/home/admin/go/src/
expect "password"
send "$AdminPassword\r"
expect "WaitingScpFinish"

spawn ssh admin@39.108.12.40
expect "password"
send "$AdminPassword\r"

expect "admin"
send "cd /home/admin/go/src/$ProjectName\r"
send "cp docs/linux/app.conf conf/\r"
send "go install $ProjectName\r"
send "sudo touch /var/log/supervisord/air-quality-predict.log\r"
send "sudo cp docs/linux/air-quality-predict.conf /etc/supervisord.conf.d/\r"
send "chmod 777 /var/log/supervisord/air-quality-predict.log\r"
send "chmod 777 /etc/supervisord.conf.d/air-quality-predict.conf\r"
send "sudo supervisorctl update\r"
send "exit\r"

interact

