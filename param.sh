#!/bin/bash
# Wifi Autopwner El Chapo Edition
# Forked from https://github.com/Mi-Al/WiFi-autopwner/blob/master/wifi-autopwner.sh

VERS="Wifi Autopwner El Chapo Edition"
IFACE=""

function firstrunSetup {
    source $(dirname $0)/settings.sh
    if [ ! -e "cracked.txt" ]; then
        echo "" > cracked.txt
    fi

    if [ ! -e "blacklist.txt" ]; then
        echo "" > blacklist.txt
    fi

    if [ ! -d "handshakes" ]; then
        mkdir handshakes
    fi

    if [ ! -d "hccapx" ]; then
        mkdir hccapx
    fi
}

function showMainMenu {
    if [[ "$(locale | grep LANG | grep -o ru)" == "ru" ]]; then
        LANGUAGE="Russian"
    else
        LANGUAGE="English"
    fi
    if [[ "$IFACE" ]]; then
        INF="${Lang[Strings27]} $IFACE"

        while read -r line ; do
        INF="${INF}${Lang[Strings28]} ${line}"
        done < <(sudo iw dev | grep -E -A5 "Interface $IFACE" | grep -E "type " | sed "s/       type //")   
    else
        INF=${Lang[Strings29]}
    fi

    echo "Information:"
    echo -e "\033[1m$INF\033[0m"

    cat lang/menu.txt
    }




while [ -n "$1" ]; do # while loop starts
    case "$1" in
    -h) showMainMenu ;;
    -b)
        param="$2"
        echo "-b option passed, with value $param"
        shift
        ;;
    -c) echo "-c option passed" ;;
    --)
        shift # The double dash makes them parameters
        break
        ;;
 
    *) echo "Option $1 not recognized" ;;
    esac
    shift
done