from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython.display import Markdown

import llm

@magics_class
class LLMMagics(Magics):
    "LLM magics that holds connection"

    def __init__(self, shell):
        super(LLMMagics, self).__init__(shell)
        self.model = None
        self.model_name = "llama-2-7b-chat"
        self.post_qualify = "Please display any code in triple backticked fence posts with a python label. \
            If any code is returned, also provide an explanation for how the code works. \
            "

    def _llm(self, cell):
        response = self.model.prompt(cell)
        return Markdown(response.text())

    def _init_model(self, model=None):
        """Initialise model."""
        if model:
            self.model_name = model
        self.model = llm.get_model(self.model_name)

    @line_magic
    def llm_connect(self, line):
        "Set up model connection"
        self._init_model(line) 

    @line_cell_magic
    def llm(self, line, cell=None):
        "Allow model to be defined as part of the call"
        if self.model is None:
            self._init_model() 
        if cell:
            return self._llm(cell)
        elif line:
            return self._llm(line)
        
    @line_cell_magic
    def llm_code(self, line, cell=None):
        "Allow model to be defined as part of the call"
        if self.model is None:
            self._init_model() 
        
        if cell:
            prompt = f"{cell} {self.post_qualify}"
            return self._llm(prompt)
        elif line:
            prompt = f"{line} {self.post_qualify}"
            return self._llm(line)
        
def load_ipython_extension(ipython):
    magics = LLMMagics(ipython)
    ipython.register_magics(magics)
