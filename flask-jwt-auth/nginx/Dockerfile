FROM nginx:latest

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/nginx.conf

RUN rm /etc/nginx/conf.d/default.conf
COPY default.conf /etc/nginx/conf.d