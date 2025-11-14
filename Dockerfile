FROM python:3.9-slim

# WARNING: The following SSH setup is for DEVELOPMENT ONLY.
# DO NOT use this in production as it introduces security risks.
# SSH access allows debugging and loading cron tasks, but exposes the container.
# Ensure to disable or remove in production builds.

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Setup SSH for development backdoor
RUN mkdir -p /var/run/sshd
RUN echo 'root:devpassword' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expose SSH port for development
EXPOSE 22

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 4222

ENTRYPOINT ["./entrypoint.sh"]