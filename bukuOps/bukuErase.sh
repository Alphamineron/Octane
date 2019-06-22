#!/usr/bin/expect
##  bukuOps.sh : automatic answers to buku --ai prompts

spawn buku -d
expect "Remove ALL bookmarks? (y/n):"
send "y\r"
expect eof
