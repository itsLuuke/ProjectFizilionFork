# inherit prebuilt image
FROM prajwals3/projectfizilion:latest

# env setup
RUN mkdir /Fizilion && chmod 777 /Fizilion
ENV PATH="/Fizilion/bin:$PATH"
WORKDIR /Fizilion
RUN apk add megatools

# clone repo
RUN git clone https://github.com/AbOuLfOoOoOuF/ProjectFizilionFork -b pruhsuperlight /Fizilion

# Copies session and config(if it exists)
COPY ./sample_config.env ./userbot.session* ./config.env* /Fizilion/

# install required pypi modules
RUN pip3 install -r requirements.txt

# Finalization
CMD ["python3","-m","userbot"]
