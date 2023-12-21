# Kafka events
Simple kafka event based communication

# Requirements
- Python 3.11
- Docker compose
- Node JS 21

# Setup
1. Start kafka using command `docker-compose up -d`.
2. Create `.env` (You can use copy of `dev.env`)
3. Start flask server `python src/__init__.py`
4. Start function `python function/__init__.py`
5. Start frontend `npm start` in `frontend` folder

## Environment variables
|Name         |Meaning                  |
|-------------|-------------------------|
|KAFKA_ADDRESS|Kafka server address     |
|FLASK_PORT   |Flask server desired port|
