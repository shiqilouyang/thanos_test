FROM python:3.8.0

WORKDIR ./thanos_test

ADD .. .

RUN pip install -i https://pypi.doubanio.com/simple/ -r requirements.txt

COPY ./thanos_test/plugin.py /usr/local/lib/python3.8/site-packages/pytest_html

CMD ["python", "./run.py"]