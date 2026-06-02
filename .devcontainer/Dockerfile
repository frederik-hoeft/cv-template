FROM debian:trixie-slim

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y \
    curl \
    git \
    vim \
    ca-certificates \
    python3-minimal \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates

ENV DISPLAY=host.docker.internal:0

# Create non-root user
RUN useradd --create-home --shell /bin/bash dev

USER dev
WORKDIR /home/dev

# Add user's local bin to PATH
ENV PATH="/home/dev/.local/bin:$PATH"

CMD ["/bin/bash"]