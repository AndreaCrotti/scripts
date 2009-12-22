#!/usr/bin/env bash
# usage cluster.sh <command> 
# gives you the first possible shell launching the optional command

NC="/opt/local/bin/nc"
FPING="/opt/local/sbin/fping"

function get_first_shell {
  for host in $(lab5)
  do
    echo "analyzing $host"
    # FIXME fping over a big list is almost double as fast
    if $FPING -t50 $host > /dev/null
      then 
      if $NC -z -w 1 $host 22 > /dev/null
      then
        open_shell $host $1 && break
      fi
    fi
  done
}

function open_shell {
  # -t useful lo launch remote interpreters
  ssh -t $1 $2; return
}

function lab5 {
  for ((i=1; $i < 40; i=$i+1))
  do
    echo "a104pc$(printf '%02d' $i)"
  done
}

get_first_shell $1