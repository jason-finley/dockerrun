# Declare parent image
FROM python:3.9

# Download rdkit
RUN pip install rdkit

# Set working directory
WORKDIR C:\Users\finja\OneDrive\Desktop\pycharm

# Copy script
COPY TestsandCalcs.py .

# Make ./data directory
RUN mkdir -p ./data

# Set default file name if not declared in env.list
ENV TARGET="None"
ENV COMPARE="None"
ENV FNAME="/data/output.txt"

# Run script
CMD python TestsandCalcs.py --target-mol $TARGET --compare-mol $COMPARE --fname $FNAME --tests $TESTS