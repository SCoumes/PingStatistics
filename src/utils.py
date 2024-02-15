def cleanDecimals(inNumber : str) -> str:
    """
    Clean a string representing a number to keep only two decimals.
    @param inNumber : The number to clean.
    @return : The cleaned number.
    """
    if "." in inNumber:
        return inNumber.split(".")[0] + "." + inNumber.split(".")[1][:2]
    else:
        return inNumber