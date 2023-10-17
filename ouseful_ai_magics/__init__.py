from .llm_magic import LLMMagics
from .sdkit_magic import SDKitMagics

def load_ipython_extension(ipython):
    magics = LLMMagics(ipython)
    ipython.register_magics(magics)

    magics = SDKitMagics(ipython)
    ipython.register_magics(magics)