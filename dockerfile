FROM python:3.9-alpine
WORKDIR /project
ADD . /project
RUN pip install -r requirements.txt
# Set tracing library env var
CMD ["ddtrace-run", "python", "app.py"]