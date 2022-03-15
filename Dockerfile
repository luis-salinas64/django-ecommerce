FROM python:3.9.5
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /opt/back_end
COPY . /opt/back_end


# Dejamos las variables definidas para un entorno de desarrollo,
# debemos remplazarlas para un entorno productivo
ENV POSTGRES_DB=shop_db
ENV POSTGRES_USER=luiggi_user
ENV POSTGRES_PASSWORD=123Luiggi!
ENV POSTGRES_HOST=db

# Dejamos DEBUG=True para hacer los retoques antes de pasarlo a False para producción.

ENV DEBUG=True
ENV SECRET_KEY=django-insecure-s3l-&wp^7qg!##&yt7((9*wka1+vao2gbz%43aln77qo3l2xf#

RUN python shop/manage.py collectstatic --noinput
CMD gunicorn --chdir /opt/back_end/shop shop.wsgi:application --bind 0.0.0.0:$PORT
    