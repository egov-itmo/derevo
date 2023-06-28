# plants_api maintenance

Some examples on maintaining the database are described here.

## Replace limitation_factors layer [replace_limitation_factors](replace_limitation_factors.py)

API is capable of returning limitations (limitation factors, light types, etc.) geojson layer with identifiers.
    Those ids can be used to delete entities via delete api endpoint. After that the whole layer can be uploaded again.
    Obviously, it is better to delete and re-upload only those polygons which needs to be updated, so this is more like
    a usage example.
