from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") # keep private

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or your frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# Query all rows from a table
table_name = "vdot_data"
response = supabase.table(table_name).select("*").execute() # response.data innehåller vdot_data tabellen

# Print the data
print(response.data)

@app.get("/filter")
def filter_data(time: float):
    # Example: select rows where 5k_time <= user input
    # lte = less than or equal to
    query = supabase.table("vdot_data") \
        .select("*") \
        .lte("5k_time", time) \
        .execute()
    return query.data
