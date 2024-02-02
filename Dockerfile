# Base image for Node.js port v1.0.1 is commit 7712f26
# docker build for testing on local computer
# docker build --progress=plain --no-cache -t port:uva-v1.0.1  . 
# docker run -p3000:3000 port:uva-v1.0.1 
#
# TODO:  nodejs production build is totally broken or messed up without clear separation of dev and prod builds 
FROM docker.io/node:18-bookworm@sha256:084b3c822003a20d41f793237286e112d1b5a1c0c7b8b04cb53a17a963a76ed7 as node-base
WORKDIR /code/

# Node.js setup
FROM node-base as setup-node
COPY package.json package-lock.json ./
RUN npm ci
COPY . .

# Run linter (Node.js)
FROM setup-node as lint-node
RUN npm run lint --verbose 

# Python setup and build
FROM docker.io/python:3.11.7-bookworm@sha256:396abfa55bae5d59681d756c99ebba84c7e8d9bd2efea15b6dc5c623ba04648f as build-py
WORKDIR /py
RUN python -m pip install poetry
COPY src/framework/processing/py /py
RUN poetry install

RUN poetry build --format wheel
RUN ls /py/dist


# Final stage for release
FROM setup-node as release

ARG release_tag=release
ARG build_type=release

RUN apt-get update && apt install -y zip python3 python3-pip python-is-python3 python3-poetry
COPY --from=build-py /py/dist/* public/
RUN npm install -g npm-run-all ts-standard

RUN npx --no-cache update-browserslist-db@latest
RUN npm run dev:build
#RUN npm run archive
#RUN npm run lint --verbose

RUN chown -R  node:node /code
USER node
EXPOSE 3000

ENTRYPOINT ["npm", "run"]
CMD ["dev:start"]
