#!/bin/bash

cd /app/image
ls $1 >& /dev/null
if [ $? -eq 0 ];then
    base=$(echo ${1} | sed 's/\.[^\.]*$//')
    if [ "`echo ${1} | grep '\.'`" ]; then
        ext=$(echo ${1} | sed 's/^.*\.\([^\.]*\)$/\1/')
        ext=".$ext"
    fi
    num=$(echo ${1} | sed 's/.*(\([0-9]*\)).*/\1/g')
    if expr "$num" : "[0-9]*$" >&/dev/null; then
        command='basename "$base" "($num)"'
        base=$(eval ${command})
        num=$(($num + 1))
        command="$base($num)$ext >&/dev/null"
    else
        command="$base(1)$ext >&/dev/null"
    fi
else
    echo "$1"
    exit 0
fi
/app/file.sh ${command}