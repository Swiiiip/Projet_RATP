def time_format(seconds: int) -> str:
    """
    Convertit un nombre de secondes en une chaîne de format heures, minutes, et secondes.

    Args:
        seconds (int): Le nombre de secondes.

    Returns:
        str: Une chaîne de format "X heures Y minutes et Z secondes".
    """
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    time = ""
    if hour > 0:
        time += f"{hour} heure{'s' if hour > 1 else ''}"

    if minutes > 0:
        if time:
            time += " "
        time += f"{minutes} minute{'s' if minutes > 1 else ''}"

    if seconds > 0:
        if time:
            time += " et "
        time += f"{seconds} seconde{'s' if seconds > 1 else ''}"

    return time
