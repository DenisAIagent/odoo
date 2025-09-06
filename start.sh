#!/bin/bash

# Script de démarrage Odoo pour Railway
# Utilise les variables d'environnement Railway

echo "Starting Odoo with Railway environment variables..."
echo "DATABASE_HOST: $DATABASE_HOST"
echo "DATABASE_PORT: $DATABASE_PORT" 
echo "DATABASE_USER: $DATABASE_USER"

exec odoo \
    --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons \
    --xmlrpc-port=8069 \
    --workers=0 \
    --log-level=info \
    --list-db=True \
    --db_host="$DATABASE_HOST" \
    --db_port="$DATABASE_PORT" \
    --db_user="$DATABASE_USER" \
    --db_password="$DATABASE_PASSWORD"