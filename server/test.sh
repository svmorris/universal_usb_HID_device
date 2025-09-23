#!/bin/bash

if [ $# -eq 0 ]; then
    curl http://172.237.117.207:31337/68d26871-87e0-8330-9f47-f4fafb389302/typedata
else
    curl -X POST http://172.237.117.207:31337/68d26871-87e0-8330-9f47-f4fafb389302/typedata   -H "Content-Type: application/json"   -d "{\"text\": \"$*\"}"
fi
