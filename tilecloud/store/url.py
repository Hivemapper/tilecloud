from urllib2 import Request, urlopen

from tilecloud import TileStore



class URLTileStore(TileStore):

    def __init__(self, tile_layouts, headers=None):
        self.tile_layouts = tile_layouts
        self.headers = headers or {}

    def get_one(self, tile):
        tile_layout = self.tile_layouts[hash(tile.tilecoord) % len(self.tile_layouts)]
        url = tile_layout.filename(tile.tilecoord)
        request = Request(url, headers=self.headers)
        response = urlopen(url)
        info = response.info()
        if 'Content-Encoding' in info:
            tile.content_encoding = info['Content-Encoding']
        if 'Content-Type' in info:
            tile.content_type = info['Content-Type']
        tile.data = response.read()
        return tile
