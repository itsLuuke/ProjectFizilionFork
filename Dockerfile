FROM ghcr.io/qubitdimensions/fizilion:squashed
RUN mkdir /Fizilion && chmod 777 /Fizilion && git clone https://github.com/itsLuuke/ProjectFizilionFork -b pruh /Fizilion
WORKDIR /Fizilion
CMD ["python3","-m","userbot"]
