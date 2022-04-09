import pywavefront

class OBJReader:
    @staticmethod
    def Read(path: str):
        scene = pywavefront.Wavefront(path, collect_faces=True)
        return scene
