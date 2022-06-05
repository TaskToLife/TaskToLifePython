# Convert snapshot return type to dictionary
def snapToDict(elem) -> dict:
    elem = elem.get()
    try:
        iter(elem)
        return {doc.id: doc.to_dict() for doc in elem}
    except TypeError:
        return {elem.id: elem.to_dict()}


# Generate random key that works with our database
def getKey(ref) -> str:
    return list(snapToDict(ref.document()).keys())[0]
