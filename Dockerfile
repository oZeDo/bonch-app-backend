FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/djangoapp/src

COPY Pipfile Pipfile.lock /opt/services/djangoapp/src/
WORKDIR /opt/services/djangoapp/src
RUN pip install pipenv && pipenv install --system
#ADD view.py /usr/local/lib/python3.6/site-packages/drf_yasg/inspectors/

COPY . /opt/services/djangoapp/src
RUN cd main && python manage.py collectstatic --no-input

EXPOSE 80
EXPOSE 5432
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":80", "--chdir", "main", "main.wsgi:application"]
