##%pip install sdkit
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)

import sdkit
from sdkit.models import load_model
from sdkit.generate import generate_images

from sdkit.utils import log
import logging
from diffusers import logging as loggingd
import torch

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning) 
log.setLevel(logging.CRITICAL)
loggingd.set_verbosity_error()

@magics_class
class SDKitMagics(Magics):
    "Stable Diffusion magics that holds connection"

    def __init__(self, shell):
        super(SDKitMagics, self).__init__(shell)
        self.context = None
        self.download_path = ".cache/sdkit/"
        self.model_path = '.cache/sdkit/stable-diffusion/v1-5-pruned.ckpt'

    def _sdkit_connect(self, model=None):
        # TO DO  - model not yet handled  - always use default
        context = sdkit.Context()

        # No CUDA on Mac
        #%env CUDA_VISIBLE_DEVICES=""
        # Need to find a way to reliably default to cuda if we can
        if torch.backends.mps.is_available():
            context.device = "mps"
            #context.device = "cpu"

        # set the path to the model file on the disk (.ckpt or .safetensors file)
        context.model_paths['stable-diffusion'] = self.model_path
        load_model(context, 'stable-diffusion')
        self.context = context
        

    @line_magic
    def sdkit_download_model(self, line):
        from sdkit.models import download_model
        #The following ckpt file is a 7.17GB download
        download_model("stable-diffusion", "1.5-pruned",
                        download_base_dir=self.download_path,
                        download_config_if_available=False)
    
    @line_magic
    def sdkit_connect(self, line):
        "Set up model connection"
        self._sdkit_connect(line)

    @line_cell_magic
    def sdkit(self, line, cell=None):
        "Stable Diffusion cell magic"
        if not self.context:
            self._sdkit_connect()
        if cell:
            images = generate_images(self.context, prompt=cell, seed=42, width=512, height=512)
        elif line:
            images = generate_images(self.context, prompt=line, seed=42, width=512, height=512)
        return images[0]
        
def load_ipython_extension(ipython):
    magics = SDKitMagics(ipython)
    ipython.register_magics(magics)
