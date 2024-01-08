FROM python:3.10-windowsservercore

RUN useradd -m -u 1000 user 
WORKDIR /home/user/content
COPY ./ .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN chown -R user:user /home/user/content
RUN chmod +x ./start.sh

USER user 
EXPOSE 8080
ENTRYPOINT ["./start.sh"]