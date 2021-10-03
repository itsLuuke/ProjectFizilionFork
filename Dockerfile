FROM ghcr.io/coldkube/kubedock:latest

RUN mkdir /Fizilion && chmod 777 /Fizilion && git clone https://github.com/AbOuLfOoOoOuF/ProjectFizilionFork -b pruh /Fizilion
ENV PATH="/Fizilion/bin:$PATH"
WORKDIR /Fizilion

CMD ["python3","-m","userbot"]
