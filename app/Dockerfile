# ---- Base Node ----
FROM node:14 AS base
WORKDIR /app
COPY package*.json ./

# ---- Dependencies ----
FROM base AS dependencies
RUN npm install

# ---- Test ----
# Run tests
FROM dependencies AS test
COPY . .
RUN npm test

# ---- Release ----
FROM base AS release
COPY --from=dependencies /app/node_modules ./node_modules
COPY . .
CMD ["node", "app.js"]
