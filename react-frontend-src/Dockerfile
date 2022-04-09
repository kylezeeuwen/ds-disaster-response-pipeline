FROM node:14

COPY . /usr/app/
WORKDIR /usr/app/

RUN npm install

# Set docker basics
ENTRYPOINT ["npm"]
CMD ["run", "build"]