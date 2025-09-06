# Dockerfile for Railway deployment - MDMC Music Ads CRM
FROM odoo:17

# Install additional dependencies
USER root
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy custom addons
COPY ./odoo/addons /mnt/extra-addons

# Set proper permissions
RUN chown -R odoo:odoo /mnt/extra-addons

# Switch back to odoo user  
USER odoo

# Expose port
EXPOSE 8069

# Start command - Simple approach without DB config
CMD ["odoo", "--addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons", "--xmlrpc-port=8069", "--workers=0", "--log-level=info", "--list-db=True"]