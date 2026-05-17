FROM node:20-slim

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend source code
COPY . .

EXPOSE 5173

# Start the Vite development server and expose it to the Docker network
CMD ["npm", "run", "dev", "--", "--host"]