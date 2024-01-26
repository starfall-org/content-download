FROM python:latest

RUN useradd -m -u 1000 user 
RUN apt-get update && apt install -y git expect wget
WORKDIR /home/user/content
COPY . .
RUN wget -O lite.gz https://github.com/xxf098/LiteSpeedTest/releases/download/v0.15.0/lite-linux-amd64-v0.15.0.gz && gzip -d lite.gz
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN chown -R user:user /home/user/content
RUN chmod +x ./start.sh ./update.sh

USER user 
EXPOSE 8080
ENTRYPOINT ["./start.sh"]