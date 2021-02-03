#!/bin/bash
read -rsn1 key && if [[ $key == $(printf "\033") ]]; then read -rsn2 key; fi; echo $key
