from IPython.core.magic import (
    Magics,
    magics_class,
    line_magic,
    cell_magic,
    line_cell_magic,
)
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import Markdown

import llm
import re

PROMPT_TYPES = {"starling": "GPT4 User: {input}<|end_of_turn|>GPT4 Assistant:"}


@magics_class
class LLMMagics(Magics):
    "LLM magics that holds connection"

    # Via chatGPT
    def extract_code_blocks(self, markdown_content):
        # Use a regular expression to find code blocks in triple backticks
        code_blocks = re.findall(r"```[^\n]*([\s\S]*?)```", markdown_content)
        return code_blocks

    def __init__(self, shell):
        super(LLMMagics, self).__init__(shell)
        self.model = None
        self.model_name = "mistral-7b-instruct-v0"
        self.code_qualify = "Please display any code in triple backticked fence posts with a python label. \
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

    def _get_response(self, args, cell):
        """Handle prompt and generate response."""
        if args.prompt_template and "{input}" in args.prompt_template:
            cell = args.prompt_template.format(input=cell)
        elif args.prompt_type and args.prompt_type.lower() in PROMPT_TYPES:
            cell = PROMPT_TYPES[args.prompt_type.lower()].format(input=cell)
        if args.system:
            response = self.model.prompt(cell, system=args.system)
        else:
            response = self.model.prompt(cell)
        return response

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
    @argument("--system", "-s", default="", help="System prompt.")
    @argument(
        "--prompt-template",
        "-p",
        default="",
        help="Prompt template, must include {{input}}.",
    )
    @argument(
        "--prompt-type",
        "-P",
        default="",
        help="Prompt style (default is llama2); alternatives: starling",
    )
    def llm(self, line, cell):
        "Allow model to be defined as part of the call"
        args = parse_argstring(self.llm, line)
        # display(f"system {args.system}")
        if self.model is None:
            self._init_model()
        response = self._get_response(args, cell)
        return Markdown(response.text())

    @cell_magic
    @magic_arguments()
    @argument("--system", "-s", default="", help="System prompt.")
    @argument("--new", "-n", default=False, help="New conversation.")
    @argument(
        "--prompt-template",
        "-p",
        default="",
        help="Prompt template, must include {{input}}.",
    )
    @argument(
        "--prompt-type",
        "-P",
        default="",
        help="Prompt style (default is llama2); alternatives: starling",
    )
    def llm_conversation(self, line, cell):
        "Have a conversation."
        args = parse_argstring(self.llm_conversation, line)
        # display(f"system {args.system}")
        if self.model is None:
            self._init_model()
        if self.conversation is None or args.new:
            print("starting new convo")
            self.conversation = self.model.conversation()
        else:
            print("continuing convo")

        response = self._get_response(args, cell)

        return Markdown(response.text())

    @cell_magic
    @magic_arguments()
    @argument("--system", "-s", default="", help="System prompt.")
    @argument(
        "--prompt-template",
        "-p",
        default="",
        help="Prompt template, must include {{input}}.",
    )
    @argument(
        "--prompt-type",
        "-P",
        default="",
        help="Prompt style (default is llama2); alternatives: starling",
    )
    def llm_code(self, line, cell):
        "Return code cell"
        args = parse_argstring(self.llm, line)
        if self.model is None:
            self._init_model()

        # if args.qualify:
        #    cell = f"{cell}\n{self.code_qualify}"

        response = self._get_response(args, cell)

        code_blocks = self.extract_code_blocks(response.text())
        header = "__GENERATED RESPONSE__"
        footer = ""
        if code_blocks:
            footer = "__GENERATED CODE ALSO APPEARS IN FOLLOWING NEW CODE CELL:__"
            self.shell.set_next_input(
                "##### GENERATED CODE #####\n" + "\n# ----------- \n".join(code_blocks),
                replace=False,
            )
        return Markdown(f"{header}:\n\n{response.text()}\n\n{footer}")


def load_ipython_extension(ipython):
    magics = LLMMagics(ipython)
    ipython.register_magics(magics)
