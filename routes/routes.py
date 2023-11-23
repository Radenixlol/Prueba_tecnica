from fastapi import APIRouter
from models.user_model import User
from datetime import datetime
from config.config import db
from google.cloud.firestore_v1.base_query import FieldFilter, BaseCompositeFilter
from schemas.user import userObject, usersObject

user = APIRouter()


@user.post('/register/entry')
async def register_entry(user: User):
    new_user = dict(user)
    entry = datetime.now()
    collection = db.collection("user").document(str(new_user["ci"]))
    query = collection.get()
    if query.exists:
        collection.update({"entry": entry, "exit": None})
    else:
        new_user["entry"] = entry
        new_user["exit"] = None
        new_user["category"] = "visitante"
        collection.set(new_user)
        query = collection.get()
        if query.exists:
            return(query.to_dict())
        else:
            print('El documento no existe')

@user.put('/register/exit')
async def register_exit(user: User):
    new_user = dict(user)
    exit = datetime.now()
    collection = db.collection("user").document(str(new_user["ci"]))
    collection.update({"exit": exit})
    query = collection.get()
    if query.exists:
        visitante = query.to_dict()
        if visitante["category"] == "visitante":
            total_time= (visitante["exit"] - visitante["entry"]).total_seconds()/3600
            price= total_time*5
            visitante["price"] = price
            return(visitante)
        elif visitante["category"] == "socio":
            total_time= ((visitante["exit"] - visitante["entry"]).total_seconds()/3600) + visitante["acumulado"]
            collection.update({"acumlado": total_time})
            return(visitante)
        elif visitante["category"] == "empleado":
            print("soy un empleado")
    else:
        print('El documento no existe')

@user.put('/contract/employee')
async def contract_employee(user: User):
    new_user = dict(user)
    collection = db.collection("user").document(str(new_user["ci"]))
    query = collection.get()
    if query.exists:
        visitante = query.to_dict()
        if visitante["category"] == "empleado":
            return("EL visitante ya es un empleado")
        else:
            new_user["acumulado"] = 0
            collection_e = db.collection("empleado").document(str(new_user["ci"]))
            collection_e.set(new_user)
            query = collection_e.get()
            collection.update({"category": "empleado"})
            if query.exists:
                return(query.to_dict())
            else:
                print('El documento no existe')
    else:
        new_user["entry"] = None
        new_user["exit"] = None
        new_user["category"] = "empleado"
        collection.set(new_user)
        data = {"ci": new_user["ci"], "acumulado": 0}
        collection_e = db.collection("empleado").document(str(new_user["ci"]))
        collection_e.set(data)
        query = collection_e.get()
        if query.exists:
            return(query.to_dict())
        else:
            print('El documento no existe')

@user.put('/society')
async def new_society(user: User):
    new_user = dict(user)
    collection = db.collection("user").document(str(new_user["ci"]))
    query = collection.get()
    if query.exists:
        visitante = query.to_dict()
        if visitante["category"] == "socio":
            return("EL visitante ya es un socio")
        else:
            new_user["acumulado"] = 0
            collection_e = db.collection("socio").document(str(new_user["ci"]))
            collection_e.set(new_user)
            query = collection_e.get()
            collection.update({"category": "socio"})
            if query.exists:
                return(query.to_dict())
            else:
                print('El documento no existe')
    else:
        new_user["entry"] = None
        new_user["exit"] = None
        new_user["category"] = "socio"
        collection.set(new_user)
        data = {"ci": new_user["ci"], "acumulado": 0}
        collection_e = db.collection("socio").document(str(new_user["ci"]))
        collection_e.set(data)
        query = collection_e.get()
        if query.exists:
            return(query.to_dict())
        else:
            print('El documento no existe')

@user.put('/reset')
async def reset_employee():
    collection_e = db.collection("empleado")
    collection = db.collection("user")
    info = collection_e.stream()
    listado = usersObject(info)
    for user in listado:
        empleado = collection_e.document(str(user["ci"]))
        empleado.update({"acumulado": 0})
        user = collection.document(str(user["ci"]))
        user.update({"entry": None, "exit": None} )

@user.get('/paid/member')
async def paid():
    collection_e = db.collection("socio").stream()
    listado = usersObject(collection_e)
    data = "Numero de cedula ----- Tiempo estacionado (hora) ----- Cantidad a pagar"
    for user in listado:
        data += f"""
{user["ci"]} ----- {round(user["acumulado"])} ----- {round(user["acumulado"])*2}"""
    return data