FROM python

RUN useradd -m -u 1000 user
RUN apt-get update && apt install -y git expect wget
WORKDIR /content
COPY . .
RUN pip install --upgrade -r requirements.txt
RUN chown -R user:user /content

USER user
RUN chmod +x start.sh

EXPOSE 8080
WORKDIR /content
ENTRYPOINT ["/content/start.sh"]
