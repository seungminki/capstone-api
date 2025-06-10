FROM python:3.9

RUN python -m pip install --upgrade pip

WORKDIR /workspace

COPY ./requirements.txt /workspace

RUN pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

COPY . /workspace

RUN mkdir -p /tmp

# ENTRYPOINT [ "python3" ]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", ">", "uvicorn.log", "2>&1", "&"]
