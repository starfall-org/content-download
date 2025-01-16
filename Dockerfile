FROM python

RUN useradd -m -u 1000 user
RUN apt-get update && apt install -y git expect wget
WORKDIR /content
COPY . .
RUN pip install --upgrade -r requirements.txt
RUN chown -R user:user /content

USER user
RUN curl --create-dirs -o $HOME/.postgresql/root.crt 'https://cockroachlabs.cloud/clusters/7616fc22-317d-43cf-bf87-4a51d4f339b6/cert'
RUN chmod +x start.sh

EXPOSE 8080
WORKDIR /content
ENTRYPOINT ["/content/start.sh"]
