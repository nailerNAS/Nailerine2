FROM python
RUN mkdir -p /src/app/data
WORKDIR /src/app
COPY . .
RUN pip install -r requirements.txt
VOLUME /src/app/data
CMD python main.py