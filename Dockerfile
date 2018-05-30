FROM nginx:1.13.12-alpine


RUN apk update
RUN apk add supervisor
RUN apk add alpine-sdk linux-headers

RUN apk add --update \
	python \
	python-dev \
	py-pip \
	build-base \	
	&& pip install psutil  \
	&& pip install uwsgi


COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir /etc/nginx/servers

EXPOSE 80




# Add demo app
COPY ./app /app
WORKDIR /app

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
