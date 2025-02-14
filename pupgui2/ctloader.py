import pkgutil
import importlib
import requests

from .resources import ctmods

class CtLoader:
    
    ctmods = []
    ctobjs = []

    def __init__(self, rs : requests.Session = None):
        self.rs = rs
        self.load_ctmods()

    def load_ctmods(self) -> bool:
        """
        Load ctmods
        Return Type: bool
        """
        for _, mod, _ in pkgutil.iter_modules(ctmods.__path__):
            if mod.startswith('ctmod_'):
                try:
                    ctmod = importlib.import_module('pupgui2.resources.ctmods.' + mod)
                    if ctmod is None:
                        print('Could not load ctmod', mod)
                        continue
                    self.ctmods.append(ctmod)
                    self.ctobjs.append({
                        'name': ctmod.CT_NAME,
                        'launchers': ctmod.CT_LAUNCHERS,
                        'description': ctmod.CT_DESCRIPTION,
                        'installer': ctmod.CtInstaller(rs=self.rs)
                    })
                    print('Loaded ctmod', ctmod.CT_NAME)
                except Exception as e:
                    print('Could not load ctmod', mod, ':', e)
        return True

    def get_ctmods(self, launcher=None, advanced_mode=True):
        """
        Get loaded ctmods, optionally sort by launcher
        Return Type: []
        """
        if launcher == None:
            return self.ctmods

        ctmods = []
        for ctmod in self.ctmods:
            if launcher in ctmod.CT_LAUNCHERS:
                if 'advmode' in ctmod.CT_LAUNCHERS and not advanced_mode:
                    continue
                ctmods.append(ctmod)
        return ctmods

    def get_ctobjs(self, launcher=None, advanced_mode=True):
        """
        Get loaded compatibility tools, optionally sort by launcher
        Return Type: List[dict]
        Content(s):
            'name', 'launchers', 'installer'
        """
        if launcher == None:
            return self.ctobjs

        ctobjs = []
        for ctobj in self.ctobjs:
            if launcher in ctobj['launchers']:
                if 'advmode' in ctobj['launchers'] and not advanced_mode:
                    continue
                ctobjs.append(ctobj)
        return ctobjs
