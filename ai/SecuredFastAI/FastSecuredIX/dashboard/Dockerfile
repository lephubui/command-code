FROM node:18

WORKDIR /app

# Install vite globally first — always available in PATH
RUN npm install -g vite

# Then install project dependencies
COPY package*.json ./
RUN npm install
RUN sleep 15
COPY . .

CMD ["vite", "--host", "0.0.0.0", "--port", "3000"]