#!/bin/bash
docker run -d --name llm-app \
    --env-file .env \
    --network host \
    -v "$(pwd)/documents:/app/documents" \
    -v "$(pwd)/vectorstore:/app/vectorstore" \
    llm-security:0.0.1-SNAPSHOT

