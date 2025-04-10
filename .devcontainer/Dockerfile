FROM python:3.13-alpine

# Update apk and install system-level dependencies (like build tools if needed)
RUN apk update && apk add --no-cache build-base

# Set the working directory in the container
WORKDIR /app

# Copy your project files into the container
COPY . .

# Upgrade pip and install your project dependencies including mcp[cli]
RUN pip install --upgrade pip && pip install .

# Optionally, specify a default command (often left for VS Code to manage in dev containers)
