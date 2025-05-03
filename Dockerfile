FROM python:3.11-slim

# Install curl for UV installation
RUN apt-get update && apt-get install -y curl

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
COPY . .

# Install dependencies
RUN uv sync

# Add this line with your app's port
EXPOSE 3005  

# Run tests first
RUN uv run pytest -v -s --cov=.

# Run the app
CMD ["uv", "run", "flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "8000"]