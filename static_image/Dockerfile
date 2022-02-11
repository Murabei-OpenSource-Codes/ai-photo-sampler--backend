FROM nginx:1.21.1
COPY static/ /usr/share/nginx/static/
RUN rm /etc/nginx/conf.d/*
COPY nginx/* /etc/nginx/conf.d/
RUN chown -R nginx:nginx /usr/share/nginx/static
