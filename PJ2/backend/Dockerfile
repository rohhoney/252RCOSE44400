FROM python:3.11-slim
WORKDIR /app
COPY app.py .
RUN pip install flask datetime
RUN mkdir -p /data
EXPOSE 5001
CMD ["python", "app.py"]
