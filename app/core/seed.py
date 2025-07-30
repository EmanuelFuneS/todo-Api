import asyncio
import os
from datetime import datetime  # Corregido: era from database import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Dict, Any
from dotenv import load_dotenv
from config import settings

load_dotenv()

class MongoSeeder:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.mongodb_url)
        self.db = self.client[settings.database_name]
    
    async def close_connection(self):

        self.client.close()

    async def clear_collection(self, collection_name: str):

       
        result = await self.db[collection_name].delete_many({})
        print(f"Deleted {result.deleted_count} documents in {collection_name}")
    
    async def seed_todos(self):  
       
        todos_data = [
            {
                "title": "Configurar entorno de desarrollo",
                "description": "Instalar Python, FastAPI y configurar MongoDB",
                "completed": True,
                "priority": "high"
            },
            {
                "title": "Crear API para gestión de tareas", 
                "description": "Implementar CRUD completo para todos con FastAPI",
                "completed": False,
                "priority": "high"
            },
            {
                "title": "Agregar validaciones",
                "description": "Implementar validaciones con Pydantic en todos los modelos",
                "completed": False,
                "priority": "medium"
            },
            {
                "title": "Escribir documentación",
                "description": "Documentar todos los endpoints en README",
                "completed": False,
                "priority": "low"
            },
            {
                "title": "Hacer testing",
                "description": "Crear tests unitarios para los endpoints principales",
                "completed": False,
                "priority": "medium"
            },
            {
                "title": "Implementar autenticación JWT",
                "description": "Crear sistema de login y registro con tokens JWT",
                "completed": False,
                "priority": "high"
            },
            {
                "title": "Deploy a producción",
                "description": "Configurar y desplegar la API en un servidor",
                "completed": False,
                "priority": "low"
            },
            {
                "title": "Optimizar performance",
                "description": "Revisar consultas y mejorar tiempos de respuesta",
                "completed": False,
                "priority": "medium"
            }
        ]
        
      
        collection_name = getattr(settings, 'collection_name', 'todos')
        collection = self.db[collection_name]
        
        existing_count = await collection.count_documents({})
        if existing_count == 0:
            result = await collection.insert_many(todos_data)
            print(f"Inserted {len(result.inserted_ids)} todos")
        else:
            print(f"Existing {existing_count} in Db")
        
        return len(todos_data)

async def main():
    
    seeder = MongoSeeder()
    
    try:

        await seeder.client.admin.command('ping')

        await seeder.seed_todos()
        
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        await seeder.close_connection()

async def reset_todos():
    
    seeder = MongoSeeder()
    
    try:
        collection_name = getattr(settings, 'collection_name', 'todos')
        await seeder.clear_collection(collection_name)
        
    except Exception as e:
        print(f"Error : {e}")
    
    finally:
        await seeder.close_connection()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        asyncio.run(reset_todos())
    else:
        asyncio.run(main())