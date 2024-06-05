FROM php:7.4-apache

RUN docker-php-ext-install mysqli
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install paramiko

# Agregar el usuario www-data al grupo docker
RUN groupadd -g 999 docker
RUN usermod -aG docker www-data

COPY config/000-default.conf /etc/apache2/sites-available/000-default.conf

RUN a2enmod rewrite
