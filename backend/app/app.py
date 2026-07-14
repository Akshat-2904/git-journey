from core.api.db import Session,get_db_Session
from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.ext.asyncio import  AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select,MetaData
import json




app=FastAPI()

def reflect_schema(sync_connection) -> dict:
    """Reflects database tables synchronously inside run_sync."""
    metadata = MetaData()
    metadata.reflect(bind=sync_connection)
    
    schema_dump = {}
    for table_name, table in metadata.tables.items():
        schema_dump[table_name] = {
            "columns": [
                {
                    "name": col.name,
                    "type": str(col.type),
                    "nullable": col.nullable,
                }
                for col in table.columns
            ],
            "primary_keys": [pk.name for pk in table.primary_key.columns],
        }
    return schema_dump

@app.get("/database")
async def get_data(session:AsyncSession=Depends(get_db_Session))->dict:

    try:
        connection= await session.connection()
        
        
        return{
             "status":"sucsess",             
             "schema":await connection.run_sync(reflect_schema)

        }
       


    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Failed to reflect database metadata using session: {str(e)}"
        )
    
@app.get("/download_metadata")
async def download_metedata(session:AsyncSession=Depends(get_db_Session))->dict:
       try:
            connection=await session.connection()
            schema_data=await connection.run_sync(reflect_schema)

            with open("schema_data","w",encoding="utf-8") as f:
                 json.dump(schema_data,f,indent=4)
            return{
                 "schema_data":schema_data
            }     
       except Exception as e:
           raise HTTPException(
            status_code=500,
            detail=f"Failed to save database metadata: {str(e)}"
        )
