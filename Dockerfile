FROM python:2.7.13

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir /usr/src/plugin-repo
WORKDIR /usr/src/plugin-repo

ENTRYPOINT [ "python", "/usr/src/app/maya-runner.py" ]
