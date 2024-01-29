def cleanDecimals(inNumber : str) -> str:
    if "." in inNumber:
        return inNumber.split(".")[0] + "." + inNumber.split(".")[1][:2]
    else:
        return inNumber