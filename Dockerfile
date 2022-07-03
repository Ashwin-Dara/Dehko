FROM ubuntu

WORKDIR /mnt/c/Users/amdar/Desktop/UG/Projects/Dehko

COPY . dehko_app
SHELL ["/bin/bash", "-c"]

ENV VIRTUAL_ENV=/utils/venv

RUN apt-get update -y && apt-get install -y python3 && \
    apt-get -y install python3-pip && pip3 install virtualenv && apt-get -y install python3.10-venv

RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./utils/requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT ["python3 /mnt/c/Users/amdar/Desktop/UG/Projects/Dehko/utils/CLIParser.py"]
