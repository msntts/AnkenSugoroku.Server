#!/bin/bash

RUN npm -g config set proxy ${HTTP_PROXY}
RUN npm -g config set https-proxy ${HTTP_PROXY}