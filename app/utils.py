from urllib.parse import parse_qs

def url_decode(s):
    """
    Décode une chaîne de requête URL
    """
    return MultiDict((k, v[0]) for k, v in parse_qs(s).items())