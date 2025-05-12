#!/bin/bash

docker run -p 5000:5000 \
  -e SERVER_PORT='5000' \
  -e FLASK_DEBUG=true \
  -e GREETING='DOCKERIZED LLM-SECURITY' \
  llm-security:0.0.1-SNAPSHOT
