PYTHON="python3"
CC="gcc"

if [ $# == 0 ]; then
  echo "Usage: bash build.sh <file_name>"
  exit 1;
fi

FILE=$1
echo "Running $FILE"
python3 teeny.py $FILE && $CC ./out.c && ./a.out

