FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends ca-certificates curl gnupg \
    && curl --fail --silent --show-error --location \
        https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb \
        --output /tmp/packages-microsoft-prod.deb \
    && dpkg --install /tmp/packages-microsoft-prod.deb \
    && apt-get update \
    && apt-get install --yes --no-install-recommends powershell \
    && pwsh -NoLogo -NoProfile -NonInteractive -Command \
        "Set-PSRepository -Name PSGallery -InstallationPolicy Trusted; Install-Module dbatools -Scope AllUsers -Force" \
    && rm --force /tmp/packages-microsoft-prod.deb \
    && rm --recursive --force /var/lib/apt/lists/*

COPY backend/pyproject.toml backend/README.md ./
COPY backend/app ./app
COPY powershell /powershell
RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
