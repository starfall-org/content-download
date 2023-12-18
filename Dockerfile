FROM python:latest

RUN useradd -m -u 1000 user 
WORKDIR /home/user/content
COPY ./ .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN chown -R user:user /home/user/content

USER user 
EXPOSE 8080
ENTRYPOINT ["bash", "start.sh"]