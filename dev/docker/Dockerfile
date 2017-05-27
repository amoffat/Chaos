FROM ubuntu:trusty

RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8 

RUN rm -vf /var/lib/apt/lists/*
RUN apt-get -y update

# system dependencies
RUN apt-get -y install\
        git\
        mysql-server\
        nginx\
        python-software-properties\
        software-properties-common\
        supervisor\
        curl

# for python 3.6
RUN add-apt-repository ppa:fkrull/deadsnakes
RUN apt-get -y update

# python requirement dependencies
RUN apt-get -y install\
        python3.6\
        # dependencies for ansible's dependency module "cryptography"
        build-essential\
        libpython3.6-dev\
        libssl-dev\
        libffi-dev


RUN curl https://bootstrap.pypa.io/get-pip.py | python3.6 -
RUN pip install virtualenv

ENV venvs=/root/.virtualenvs
ENV venv=$venvs/chaos
ENV chaosdir=/root/workspace/Chaos

RUN mkdir -p $chaosdir
RUN mkdir $venvs
RUN virtualenv $venv

ENV PATH="$venv/bin:$PATH"

WORKDIR $chaosdir

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt

RUN rm /etc/nginx/sites-enabled/default

ENV start_chaos=/usr/local/bin/start_chaos.sh

# these are things we can only set up once our data volume (the repo code) has
# been mounted to the container upon running
RUN printf "\
    #!/bin/bash
    ln -sf $chaosdir/etc/chaos_supervisor.conf /etc/supervisor/conf.d/chaos.conf\n\
    ln -sf $chaosdir/etc/nginx/chaos_errors /etc/nginx/sites-available/\n\
    ln -sf /etc/nginx/sites-available/chaos_errors /etc/nginx/sites-enabled/\n\

    service supervisor start\n\
    service nginx start\n\

    sleep 1\n\

    tail -F /var/log/supervisor/chaos-*"\
    >> $start_chaos

RUN chmod +x $start_chaos
EXPOSE 80 8081
ENTRYPOINT $start_chaos
