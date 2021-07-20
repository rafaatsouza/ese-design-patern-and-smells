# /bin/sh
set -e

YELLOW='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

if [ -z "$1" ]; then
  echo "${RED}Argument tool is required\n${NC}"
  exit
fi

if [ -z "$2" ]; then
  echo "${RED}Argument folder path is required\n${NC}"
  exit
fi

PARENT_FOLDER=$( cd "$(dirname "${2}")" ; pwd )
TARGET_FOLDER=$PARENT_FOLDER/$( basename $2 )

if [ -d TARGET_FOLDER ]; then
  echo "${RED}Argument folder path should be a valid\n NOT: $2${NC}"
  exit
fi

echo "${YELLOW}Running parser...${NC}"
echo "${GREEN}Target folder: ${TARGET_FOLDER}\n${NC}"

FROM_TOOL=$1
COUNT_PROCESSED_FILES=0

for filename in $( ls $TARGET_FOLDER/*.xml ) ; do
    echo "${GREEN}Processing... $filename${NC}"
    python main.py --tool $FROM_TOOL --file $filename
    echo "${GREEN}Done!\n${NC}"
    COUNT_PROCESSED_FILES=$((COUNT_PROCESSED_FILES+1))
done

echo "${GREEN}\
Analyzed tool: ${FROM_TOOL}\n\
Total of files processed: ${COUNT_PROCESSED_FILES}\
${NC}"