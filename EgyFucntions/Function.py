
def inline(list, add=None):

    new_list = [[list[i],list[i+1]] for i in range(0,len(list),2)] if len(list)%2 == 0 else [[list[i],list[i+1]] for i in range(0,len(list) - 1,2)] + [[list[len(list)-1]]]
    if add:
        new_list += add

    return new_list

cookies = [
    {
        "name": "JS_TIMEZONE_OFFSET",
        "path": "/",
        "value": "-7200"
    },
    {
        "name": "EGUDI",
        "path": "/",
        "value": "SLh6PzfCCX5VXth3.f049a5caaaad11a7496f18a11ec42bde0a2c5238d368ea0531a35d654ecf886151a93cb3d66d1d75574aedef48fb3f53922dc70c2d041b3e0207ca12d5de1b5c"
    },
    {
        "name": "b4445db4",
        "path": "/",
        "value": "thhhrBzUAecrhkDHGDDDHOFDDqrkRkrhrXVihrhkhrDkHewRRGIZWRRRDhrkrhriVwQhrhkhriLpsvDDVARkkeOUikjNShrhG-814ec38fed74de8b2e5f67fdd9d7da56"
    },
    {
        "domain": "giga.egybest.kim",
        "name": "push_subscribed",
        "path": "/",
        "value": "ignore"
    },
    {
        "name": "0d54a416",
        "path": "/",
        "value": "CNNNamAgNaNhNaSVgChIiCNCXgpAWNahaNagAseNaNhNaChqbLiPxZUfpLgXynVNahaNatiLRjraNhCyXCCCyMdCCVCCaNX-e641f25d1356c2f16cf0039ceb0b9de6"
    },
    {
        "name": "PSSID",
        "path": "/",
        "value": "P2pu246tCRpEc3wHLdE4NxfA1u8Ywdvvexl9INvgFifu1%2CJBHb0V32gmu9yKDTGK25TAFuRNr8FFl2iPxHo7AQdmlNnvXf6PKbu3Q4BS%2CGsGwW%2CVK6ENsMIXBLMocqZU"
    }
]
