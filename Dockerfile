# Use Python base image
FROM python:3.9-slim

# This copies everything in your current directory to the /app directory in the container.
COPY . /app

# This sets the /app directory as the working directory for any RUN, CMD, ENTRYPOINT, or COPY instructions that follow.
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (if needed)
EXPOSE 8501

# This command creates a .streamlit directory in the home directory of the container.
#RUN mkdir ~/.streamlit

# This copies your Streamlit configuration file into the .streamlit directory you just created.
#RUN cp config.toml ~/.streamlit/config.toml

# Similar to the previous step, this copies your Streamlit credentials file into the .streamlit directory.
#RUN cp credentials.toml ~/.streamlit/credentials.toml

# This sets the default command for the container to run the app with Streamlit.
ENTRYPOINT ["streamlit", "run"]

# This command tells Streamlit to run your app.py script when the container starts.
CMD ["app.py"]