

def userObject(data) -> dict:
    return{
        "ci": int(data["ci"]),
        "acumulado": round(data["entry"])
    }

def usersObject(collection) -> list:
    listado = []
    for user in collection:
        listado.append(user.to_dict())
    return listado