#!/bin/bash

# Script de démarrage Odoo pour Railway
# Utilise les variables d'environnement Railway

echo "Starting Odoo with Railway environment variables..."
echo "DATABASE_HOST: $DATABASE_HOST"
echo "DATABASE_PORT: $DATABASE_PORT" 
echo "DATABASE_USER: $DATABASE_USER"
echo "RAILWAY PORT: $PORT"

# Use Railway's PORT variable or default to 8069
ODOO_PORT=${PORT:-8069}
echo "Starting Odoo on port: $ODOO_PORT"

exec odoo \
    --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons \
    --xmlrpc-port="$ODOO_PORT" \
    --workers=0 \
    --log-level=info \
    --db_host="$DATABASE_HOST" \
    --db_port="$DATABASE_PORT" \
    --db_user="$DATABASE_USER" \
    --db_password="$DATABASE_PASSWORD"