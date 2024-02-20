#!/bin/bash
mkdir -p ssh
rm ssh/id_rsa ssh/id_rsa.pub
ssh-keygen -f ssh/id_rsa -N ''
