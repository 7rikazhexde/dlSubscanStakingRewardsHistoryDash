# Specify the base Docker image
FROM python:3.10

# Set the working directory
WORKDIR /

# Specify Japanese locale
## Consider using a `--no-install-recommends` when `apt-get` installing packages.
RUN apt-get update && \
    apt-get -y --no-install-recommends install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 && \
    rm -rf /var/lib/apt/lists/*
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

# Set xterm as the terminal emulator
ENV TERM xterm

# Install Poetry
## https://python-poetry.org/docs/#installing-with-the-official-installer
### Linux, macOS, Windows (WSL)
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the path of Poetry with unix
## https://python-poetry.org/docs/#installing-with-the-official-installer
### Add Poetry to your PATH
ENV PATH /root/.local/bin:$PATH

# Disable Poetry from creating virtual environments
RUN poetry config virtualenvs.create false

# Set the working directory to /dlSubscanStakingRewardsHistoryDash
WORKDIR /dlSubscanStakingRewardsHistoryDash

# Copy dependencies for installation
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install

# Copy the application files
COPY ./app ./app
COPY ./tests ./tests
COPY ./ci ./ci
COPY README.md .

# Run the application
#CMD ["poetry", "run", "python", "app"]
