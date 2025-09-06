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

# Copy Railway-specific Odoo configuration (FIXED)
COPY ./docker/odoo.railway.fixed.conf /etc/odoo/odoo.conf

# Set proper permissions
RUN chown -R odoo:odoo /mnt/extra-addons
RUN chown odoo:odoo /etc/odoo/odoo.conf

# Switch back to odoo user
USER odoo

# Expose port
EXPOSE 8069

# Start command - Let Odoo handle DB creation via web interface
CMD ["odoo", "--config=/etc/odoo/odoo.conf"]