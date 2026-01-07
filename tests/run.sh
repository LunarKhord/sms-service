#!/bin/bash

# Define ANSI Color Codes for enhanced visual clarity
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Header
printf "${BLUE}=====================================${NC}\n"
printf "${BLUE}   SMS GATEWAY TEST ORCHESTRATOR     ${NC}\n"
printf "${BLUE}=====================================${NC}\n"

# 2. Infrastructure Check (Implicitly provides feedback)

echo -e "🔧 ${GREEN}Test start....${NC}"
printf "${BLUE}=====================================${NC}\n"
pytest -s
printf "${BLUE}=====================================${NC}\n"
echo -e "✅ ${GREEN}All tests completed.${NC}"
printf "${BLUE}=====================================${NC}\n"
