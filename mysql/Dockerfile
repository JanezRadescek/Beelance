FROM mysql:5.7.15

MAINTAINER me

ENV MYSQL_DATABASE=db \
    MYSQL_ROOT_PASSWORD=long_password_group45

ADD /sql/init.sql /docker-entrypoint-initdb.d

EXPOSE 3306
