from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
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
        self.conversation = None

    def _llm(self, cell):
        response = self.model.prompt(cell)
        return Markdown(response.text())

    def _init_model(self, model=None):
        """Initialise model."""
        if model:
            self.model_name = model
        self.model = llm.get_model(self.model_name)
        self.conversation = None

    @line_magic
    def llm_connect(self, line):
        "Set up model connection"
        self._init_model(line) 

    @line_magic
    def llm_clear(self, line):
        "Clear down model connection"
        self.model = None 
        self.conversation = None

    @line_magic
    def llm_clear_conversation(self, line):
        "Clear down conversation"
        self.conversation = None

    @line_magic
    def llm_show_model(self, line):
        "Display model name"
        model_status = self.model is None
        conversation_status = self.conversation is None
        model_status = "unloaded" if model_status else "loaded"
        conversation_status = "not ongoing" if conversation_status else "ongoing"
        return f"{self.model_name}: {model_status}; conversation {conversation_status}"

    @cell_magic
    @magic_arguments()
    @argument('--system', '-s', default='', help='System prompt.')
    def llm(self, line, cell):
        "Allow model to be defined as part of the call"
        args = parse_argstring(self.llm, line)
        #display(f"system {args.system}")
        if self.model is None:
            self._init_model()
        if args.system:
            response = self.model.prompt(cell, system=args.system)
        else:
            response = self.model.prompt(cell)
        return Markdown(response.text())

    @cell_magic
    @magic_arguments()
    @argument('--system', '-s', default='', help='System prompt.')
    @argument('--new', '-n', default=False, help='New conversation.')
    def llm_conversation(self, line, cell):
        "Have a conversation."
        args = parse_argstring(self.llm_conversation, line)
        #display(f"system {args.system}")
        if self.model is None:
            self._init_model()
        if self.conversation is None or args.new:
            print("starting new convo")
            self.conversation = self.model.conversation()
        else:
            print("continuing convo")
        if args.system:
            response = self.conversation.prompt(cell, system=args.system)
        else:
            response = self.conversation.prompt(cell)
        return Markdown(response.text())

    @cell_magic
    @magic_arguments()
    @argument('--system', '-s', default='', help='System prompt.')
    def llm_code(self, line, cell):
        "Allow model to be defined as part of the call"
        args = parse_argstring(self.llm, line)
        if self.model is None:
            self._init_model() 
        
        if args.system:
            prompt = f"{cell} {self.post_qualify}"
            response = self.model.prompt(prompt)
        else:
            response = self.model.prompt(cell)
        return Markdown(response.text())
        
def load_ipython_extension(ipython):
    magics = LLMMagics(ipython)
    ipython.register_magics(magics)
