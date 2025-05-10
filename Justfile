default:

dev port="8000":
    uvicorn app:create_app --reload --factory --host 0.0.0.0 --port {{port}}