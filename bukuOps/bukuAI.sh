#!/usr/bin/expect
##  bukuAI.sh : automatic answers to buku --ai prompts

spawn buku --ai
expect "Add parent folder names as tags? (y/n):"
send "y\r"
expect "Import bookmarks from google chrome? (y/n):"
send "y\r"
expect "Import bookmarks from chromium? (y/n):"
send "y\r"
expect "Import bookmarks from Firefox? (y/n):"
send "y\r"
expect eof
