#!/usr/bin/env bash
#source /home/john/miniconda3/etc/profile.d/conda.sh
#conda activate proxy_pool_env
#source ~/miniconda3/etc/profile.d/conda.sh
#conda init
#eval "$(conda shell.bash hook)"
#source ~/.bashrc
#conda activate proxy_pool_env
python proxyPool.py server &
python proxyPool.py schedule