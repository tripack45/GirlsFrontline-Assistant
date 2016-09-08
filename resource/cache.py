import image
import resource
cache = {}


def cacheLoadImage(scene, key):
    global cache
    if (scene, key) in cache:
        return cache[(scene, key)].copy()
    im = image.loadResourceImage(resource.images[scene][key])
    cache[(scene, key)] = im
    return im

