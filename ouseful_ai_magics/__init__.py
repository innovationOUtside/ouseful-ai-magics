from .llm_magic import LLMMagics
from .sd_magic import SDMagics

def load_ipython_extension(ipython):
    magics = LLMMagics(ipython)
    ipython.register_magics(magics)

    magics = SDMagics(ipython)
    ipython.register_magics(magics)