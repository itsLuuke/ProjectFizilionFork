FROM ghcr.io/qubitdimension/fizilion:latest
RUN git clone https://github.com/itsLuuke/ProjectFizilionFork -b pruh /Fizilion
CMD ["python3","-m","userbot"]
