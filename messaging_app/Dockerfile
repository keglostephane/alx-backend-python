# Use Python 3.10 as base image
FROM python:3.10

# Install system dependencies properly
RUN apt-get update && \
    apt-get install -y python3-pip default-mysql-server && \
	apt-get clean && \ 
    rm -rf /var/lib/apt/lists/*


# Create working directory
WORKDIR /app

# Copy and install Python requirements
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Initialize MySQL database
CMD service mariadb start && \
    sleep 5 && \
    mysql -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME};" && \
    mysql -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PWD}';" && \
    mysql -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';" && \
    mysql -e "FLUSH PRIVILEGES;" && \
    python manage.py runserver 0.0.0.0:8000