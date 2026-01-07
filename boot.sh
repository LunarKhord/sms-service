#!/bin/bash

# Define ANSI Color Codes for enhanced visual clarity
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Header
printf "${BLUE}=====================================${NC}\n"
printf "${BLUE}   SMS GATEWAY BOOT ORCHESTRATOR     ${NC}\n"
printf "${BLUE}=====================================${NC}\n"

# 2. Infrastructure Check (Implicitly provides feedback)
echo -e "🔧 ${GREEN}Synchronizing environment with uv...${NC}"
uv sync

# Activate env
# source .venv/bin/activate
# echo -e "${GREEN} Environment entered...${NC}"
# 3. Execution Phase
echo -e "📡 ${GREEN}Launching FastAPI on http://127.0.0.1:8000${NC}"
echo "-------------------------------------"

# Using uv run ensures the 'src' layout is correctly in the PYTHONPATH
uvicorn src.sms-service.lifespan:app --reload
