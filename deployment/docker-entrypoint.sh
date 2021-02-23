#!/bin/bash

echo "Starting nginx server"
service nginx start

echo "Running command $@"
exec "$@"

echo "Exiting..."

echo "Stopping nginx"
service nginx stop

echo "Have a nice day!"
