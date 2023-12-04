FROM python:latest

RUN useradd -m -u 1000 user 

COPY requirements.txt . 

RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /home/user/content-download

RUN chown -R user:user /home/user/content-download

USER user 

COPY --chown=1000 ./ /home/user/content-download 

EXPOSE 7860

ENTRYPOINT ["bash", "start.sh"]