This repository contains some initial work for Cisco SD-WAN automation. 
Cisco SD-WAN controller (vManage) provides a north-bound REST API interface which is going to be used for remote configuration and provisioning.

The overal idea is to have a separate lib with API calls (see restapicalls.py). So other scripts and modules could generate the corresponding payload for a call and utilise the lib methods to send it to a vManage controller.

Scripts directory contains some scripts used for a lab demo purpose. More examples will be included as available.
