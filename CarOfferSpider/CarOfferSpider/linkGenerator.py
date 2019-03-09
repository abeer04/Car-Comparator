# This is a very basic link generator, we will have to modify it to get the correct results

def pakwheelsURL(query):
    prefix = 'https://www.pakwheels.com/used-cars/search/-/?q='

    words = query.split(' ')

    suffix = ''
    for i in range(len(words)):
        if i == 0:
            suffix += words[0]
        else:
            suffix += '+' + words[i]

    url = prefix + suffix

    return url

def olxURL(query):
    prefix = 'https://www.olx.com.pk/vehicles_c5/q-'

    words = query.split(' ')

    suffix = ''
    for i in range(len(words)):
        if i == 0:
            suffix += words[0]
        else:
            suffix += '-' + words[i]

    url = prefix + suffix

    return url

def gariUrl(query):
    prefix = 'http://www.gari.pk/used-cars/'
    
    words = query.split(' ')

    suffix = ''