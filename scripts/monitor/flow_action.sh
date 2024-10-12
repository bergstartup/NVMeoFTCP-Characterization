sudo ethtool -U ens9np0 flow-type tcp4 src-port $1 loc $2 action $3
