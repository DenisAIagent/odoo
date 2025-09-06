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

# Copy startup script
COPY start.sh /usr/local/bin/start.sh

# Set proper permissions
RUN chown -R odoo:odoo /mnt/extra-addons
RUN chmod +x /usr/local/bin/start.sh

# Switch back to odoo user  
USER odoo

# Expose port
EXPOSE 8069

# Start with script that uses environment variables
CMD ["/usr/local/bin/start.sh"]