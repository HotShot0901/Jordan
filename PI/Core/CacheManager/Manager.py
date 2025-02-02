from ..Base import PI_VERSION

import os
import json
from tempfile import gettempdir

from typing import Dict, Any, List, Tuple

class Cache:
    __TempDirGenerated = False

    @staticmethod
    def InitLocalTempDirectory():
        if not Cache.__TempDirGenerated:
            os.makedirs(f"{gettempdir()}\\PI", exist_ok=True)
            os.makedirs("C:\\ProgramData\\PI", exist_ok=True)
            Cache.__TempDirGenerated = True

        return Cache

    @staticmethod
    def GetLocalTempDirectory():
        Cache.InitLocalTempDirectory()
        return f"{gettempdir()}\\PI"

    @staticmethod
    def GetLocalSaveDirectory():
        Cache.InitLocalTempDirectory()
        return "C:\\ProgramData\\PI"

class CacheLoadingError(Exception): pass

class LocalCache:
    __Fields: Dict[str, Any]

    @staticmethod
    def Init():
        LocalCache.__Fields = {}
        Cache.InitLocalTempDirectory()
        return LocalCache
    
    @staticmethod
    def GetData() -> Dict[str, Any]: return LocalCache.__Fields

    @staticmethod
    def SetProperty(name: str, value: Any):
        LocalCache.__Fields[name] = value
        return LocalCache

    @staticmethod
    def SetProperties(**NameValuePaires: Dict[str, Any]):
        for name, value in NameValuePaires.items(): LocalCache.__Fields[name] = value
        return LocalCache

    @staticmethod
    def SetPropertiesFromDict(nameValuePaires: Dict[str, Any]):
        for name, value in nameValuePaires.items(): LocalCache.__Fields[name] = value
        return LocalCache

    @staticmethod
    def GetProperty(name: str, default=None) -> Any: return LocalCache.__Fields.get(name, default)

    @staticmethod
    def GetProperties(*Names: List[str]) -> Dict[str, Any]:
        fields = {}
        for name in Names: fields[name] = LocalCache.__Fields.get(name, None)
        return fields

    @staticmethod
    def DeleteProperty(*properties: Tuple[str]):
        for property in properties:
            if property in LocalCache.__Fields.keys():
                del LocalCache.__Fields[property]
        return LocalCache

    @staticmethod
    def DumpFields():
        LocalCache.SetProperty("Version", PI_VERSION)
        with open(f"{Cache.GetLocalSaveDirectory()}\\LocalCache.json", 'w') as f: json.dump(LocalCache.__Fields, f)
        return LocalCache

    @staticmethod
    def __LoadFields(_depth: int=10):
        if _depth == 0: raise CacheLoadingError("Error loading cache. Max depth reached.")

        LocalCache.__Fields = {}
        try:
            with open(f"{Cache.GetLocalSaveDirectory()}\\LocalCache.json", 'r') as f:
                LocalCache.__Fields = json.load(f)
        except Exception as _:
            LocalCache.DumpFields()
            return LocalCache.__LoadFields(_depth-1)

        # Cache invalidation
        finally:
            version = LocalCache.GetProperty("Version", None)

            if not version: LocalCache.SetProperty("Version", PI_VERSION)
            elif version != PI_VERSION:
                # LocalCache.__Fields.clear()
                try: del LocalCache.__Fields["ProjectSettings"]
                except KeyError as _: pass

                LocalCache.DumpFields()
                return LocalCache.__LoadFields(_depth-1)

        return LocalCache

    @staticmethod
    def LoadFields(): return LocalCache.__LoadFields()

    @staticmethod
    def Shutdown():
        LocalCache.DumpFields()
        LocalCache.__Fields = {}
        return None

class ProjectCache:
    __Fields: Dict[str, Any]
    __DIR: str

    @staticmethod
    def SetProjectSaveDirectory(dir: str): ProjectCache.__DIR = dir + "\\Settings.json"

    @staticmethod
    def Init(dir: str):
        ProjectCache.__Fields = {}
        ProjectCache.SetProjectSaveDirectory(dir)
        return ProjectCache
    
    @staticmethod
    def GetData() -> Dict[str, Any]: return ProjectCache.__Fields

    @staticmethod
    def SetProperty(name: str, value: Any):
        ProjectCache.__Fields[name] = value
        return ProjectCache

    @staticmethod
    def SetProperties(**NameValuePaires: Dict[str, Any]):
        for name, value in NameValuePaires.items(): ProjectCache.__Fields[name] = value
        return ProjectCache

    @staticmethod
    def SetPropertiesFromDict(nameValuePaires: Dict[str, Any]):
        for name, value in nameValuePaires.items(): ProjectCache.__Fields[name] = value
        return ProjectCache

    @staticmethod
    def GetProperty(name: str, default=None) -> Any: return ProjectCache.__Fields.get(name, default)

    @staticmethod
    def GetProperties(*Names: List[str]) -> Dict[str, Any]:
        fields = {}
        for name in Names: fields[name] = ProjectCache.__Fields.get(name, None)
        return fields

    @staticmethod
    def DeleteProperty(*properties: Tuple[str]):
        for property in properties:
            if property in ProjectCache.__Fields.keys():
                del ProjectCache.__Fields[property]
        return ProjectCache

    @staticmethod
    def DumpFields():
        ProjectCache.SetProperty("Version", PI_VERSION)
        with open(ProjectCache.__DIR, 'w') as f: json.dump(ProjectCache.__Fields, f)
        return ProjectCache

    @staticmethod
    def __LoadFields(_depth: int=10):
        if _depth == 0: raise CacheLoadingError("Error loading cache. Max depth reached.")

        ProjectCache.__Fields = {}
        try:
            with open(ProjectCache.__DIR, 'r') as f:
                ProjectCache.__Fields = json.load(f)
        except Exception as _:
            ProjectCache.DumpFields()
            return ProjectCache.__LoadFields(_depth-1)

        # Cache invalidation
        finally:
            version = ProjectCache.GetProperty("Version", None)

            if not version: ProjectCache.SetProperty("Version", PI_VERSION)
            elif version != PI_VERSION:
                del ProjectCache.__Fields
                ProjectCache.__Fields ={}

                ProjectCache.DumpFields()
                return ProjectCache.__LoadFields(_depth-1)

        return ProjectCache

    @staticmethod
    def LoadFields(): return ProjectCache.__LoadFields()

    @staticmethod
    def Shutdown():
        ProjectCache.DumpFields()
        ProjectCache.__Fields = {}
        return None
