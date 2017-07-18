FROM python:2.7.13

WORKDIR /usr/src/app

# install maya pip dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# install node 4.x
RUN wget -qO- https://deb.nodesource.com/setup_4.x | bash - \
	&& apt-get -y install nodejs

# copy maya source
COPY . .

# dir for actual plugin code (to be mounted as volume)
RUN mkdir /usr/src/plugin-repo
WORKDIR /usr/src/plugin-repo

ENTRYPOINT [ "python", "/usr/src/app/maya-runner.py" ]
