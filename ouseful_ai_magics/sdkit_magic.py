##%pip install sdkit
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
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
        self.typ = "stable-diffusion"
        self.version = "1.5-pruned"
        #2.1-512-ema-pruned

    def _create_model_path(self):
        #HACKFIX
        _version = self.version
        if _version=="2.1-512-ema-pruned":
            _version = "2-1_512-ema-pruned"
        return f"{self.download_path}{self.typ}/v{_version}.ckpt"

    def _sdkit_connect(self):
        # TO DO  - model not yet handled  - always use default
        context = sdkit.Context()

        self.model_path = self._create_model_path()
    
        # No CUDA on Mac
        #%env CUDA_VISIBLE_DEVICES=""
        # Need to find a way to reliably default to cuda if we can
        if torch.backends.mps.is_available():
            context.device = "mps"
            #context.device = "cpu"

        # set the path to the model file on the disk (.ckpt or .safetensors file)
        context.model_paths['stable-diffusion'] = self.model_path
        # TO DO: find a better way of checking we have a downloaded model...
        try:
            load_model(context, 'stable-diffusion')
        except:
            self._download_model()
            load_model(context, 'stable-diffusion')
        self.context = context
        self._about()

    def _download_model(self):
        from sdkit.models import download_model
        #The default ckpt file is a 7.17GB download
        download_model(self.typ, self.version,
                       download_base_dir=self.download_path,
                       download_config_if_available=False)
        
    def _about(self):
        context = self.context == None
        model_path = self.model_path
        typ = self.typ
        version = self.version
        display(f"Model type: {typ}; model version: {version}; path: {model_path}; context loaded: {context}")

    @line_magic
    @magic_arguments()
    @argument('--type', '-t', default='stable-diffusion', help='Model type (default: stable-diffusion).')
    @argument('--version', '-v', default='1.5-pruned', help='Model version (default: 1.5-pruned).')
    def sdkit_download_model(self, line):
        """Download model magic."""
        args = parse_argstring(self.sdkit_download_model, line)
        self.typ = args.type
        self.version = args.version
        self._download_model()
    
    @line_magic
    @magic_arguments()
    @argument('--type', '-t', default='stable-diffusion', help='Model type (default: stable-diffusion).')
    @argument('--version', '-v', default='1.5-pruned', help='Model version (default: 1.5-pruned).')
    def sdkit_connect(self, line):
        "Set up model connection"
        args = parse_argstring(self.sdkit_connect, line)
        self.typ = args.type
        self.version = args.version
        self._sdkit_connect()

    @line_magic
    def sdkit_clear(self, line):
        "Clear down model connection"
        self.context = None

    @line_magic
    def sdkit_about(self, line):
        "Info about the connection"
        self._about()

    @cell_magic
    @magic_arguments()
    @argument('--negative_prompt', '-n', default='', help='Negative prompt.')
    @argument('--height', '-h', type=int, default=512, help='Height of image (must be divisible by 8; default: 512).')
    @argument('--width', '-w', type=int, default=512, help='Width of image (must be divisible by 8; default: 512).')
    @argument('--seed', '-s', type=int, default=42, help='Random seed (default: 42).')
    @argument('--num_outputs', '-o', type=int, default=1, help='Number of outputs (default: 1).')
    @argument('--num_inference_steps', '-i', type=int, default=25, help='Number of inference steps (default: 25).')
    @argument('--guidance_scale', '-g', type=float, default=7.5, help='Guidance scale (default: 7.5).')
    @argument('--init_image', '-I', default=None, help='Initial image (string (path to file), or PIL.Image or a base64-encoded string).')
    @argument('--prompt_strength', '-p', type=float, default=0.8, help='Prompt strength (default: 0.8).')
    def sdkit(self, line, cell):
        "Stable Diffusion cell magic"
        args = parse_argstring(self.sdkit, line)
        if not self.context:
            self._sdkit_connect()
        images = generate_images(self.context, prompt=cell,
                                 negative_prompt=args.negative_prompt,
                                 seed=args.seed, width=args.width, height=args.height,
                                 num_outputs = args.num_outputs, # TO DO - multiple images not working?
                                 num_inference_steps = args.num_inference_steps,
                                 guidance_scale=args.guidance_scale,
                                 init_image=args.init_image, # TO DO if this is a web URL, grab image as PIL image
                                 prompt_strength=args.prompt_strength)
        return images[0] #TO DO fix when we can generate multiple images

def load_ipython_extension(ipython):
    magics = SDKitMagics(ipython)
    ipython.register_magics(magics)
