# ouseful-ai-magics

Simple IPython magics for experimenting with locally run generative AI text and image models.

Magics built around third party Python packages offering Python APIs to generative models:

- [`llm`](https://github.com/simonw/llm): command line and Python API for `gpt4all` text models
- [`sdkit`](https://github.com/easydiffusion/sdkit): Python API for locally run Stable Diffusion

Only tested on Mac M2. Dependencies may vary for other platforms (check original package repos for details; please post an issue with differing dependency requirements for other platforms etc.)

## Installation

`pip install git+https://github.com/innovationOUtside/ouseful-ai-magics.git`

or

`pip install https://github.com/innovationOUtside/ouseful-ai-magics/archive/refs/heads/main.zip`

## Getting Started

Load the magics:

- `%load_ext ouseful_ai_magics`
- `%reload_ext ouseful_ai_magics`

## Text generation

You can connect to an `llm` model as:

`%llm_connect llama-2-7b-chat` (default)
`%llm_connect ggml-replit-code-v1-3b`

If the model is not available it will be automatically downloaded. *Run the command line command `llm models list` to list the available models.*

Display current model name and status:

`%llm_show_model`

Deallocate the model:

`%llm_clear`

Use the `llm` package to generate text via the `%%llm` cell block magic:

```text
%%llm
Tell me a funny knock knock joke
```

This works from a cold start and does not require a model to be explicitly loaded (the default model is automatically loaded if no loaded model is found).

### System prompts

You can pass in a system prompt (`-s / --system`) which will be applied if the model accepts it:

```python
%%llm -s "You are a welsh comedian. You see everything as a joke and have a thick welsh accent."
What is the weather like?
```

You can also pass in a system prompt via a variable:

```python
prompt = """"You are a welsh comedian.
You see everything as a joke and have a thick welsh accent."""

%%llm -s "$prompt"
What is the weather like?
```

### Conversations

Conversations carry over previous prompts and responses.

```python
prompt = """You are not an AI model, you are teacher called Lemmy. You are a computer sceince expert and a teacher who provides helpful explanations with code examples using Python. The code should be in triple backticked markdown blocks."""

%%llm_conversation -s "$prompt"
What is your name?
````

You can then carry on the conversation

```python
%%llm_conversation
What did you say your name was?
```

Start a new conversation with `-n/--new`:

```python
%%llm_conversation -n True -s "Your name is Ozzy"
```

Clear a conversation:

`%llm_clear_conversation`

### Working with code

*This is WIP en route to seeing if we can get code into a code cell etc.*

The `%%llm_code` cell magic works similarly but adds a sentence to the end of the prompt:

`%llm_code R code for factorial`

```text
"""
Please display any code in triple backticked fence posts with a python label.
If any code is returned, also provide an explanation for how the code works.
"""
```

### Resetting conversations and clearing models

Clear a conversation:

`%llm_clear_conversation`

Deallocate the model:

`%llm_clear`

## Image generation

Use the `sdkit` package to generate Stable Diffusion models:

- download a model: `%sdkit_download_model` (default is *stable-diffusion `v1-5-pruned`*); optional arguments `-t / --type` (e.g. `stable-diffusion` (default)), `-v / --version` (eg `1-5-pruned` (default), `2.1-512-ema-pruned`)
- connect to a model: `%sdkit_connect`; same options as `sdkit_download_model`; if the model has not been downloaded previously, an attempt will be made to download it;
- clear down a model: `%sdkit_clear`
- generate image: `%%sdkit` cell block magic; (this will autoconnect the default model if it is not already connected); see examples below for additional switches.

## `%%sdkit` image generation

Example of using the `%%sdkit` cell magic:

```python
%%sdkit -n "Disney; Game of Thrones" --width 256
A fairy tale castle.
A dragon flies overhead.
```

The following option switches are available in the `%%sdkit` cell magic:

- `--negative_prompt / -n`, default='', negative prompt; (not supported for Stable Diffusion 1.5).
- `--height / -h`, type=int, default=512, height of image (must be divisible by 8; default: 512).
- `--width / -w`, type=int, default=512, width of image (must be divisible by 8; default: 512).
- `--seed / -s`,` type=int, default=42, random seed (default: 42).
- `--num_inference_steps / -i`, type=int, default=25, number of inference steps (default: 25).
- `--guidance_scale / -g`, type=float, default=7.5, guidance scale (default: 7.5).
- `--init_image / -I`, default=None, initial image (string (path to file), or PIL.Image or a base64-encoded string).
- `--prompt_strength / -p`, type=float, default=0.8, prompt strength (default: 0.8).

Show status of loaded model:

`%sdkit_about`

Deallocate the model:

`%sdkit_clear`

Example models:

- `stable-diffusion, 1-5-pruned` (default)
- `stable-diffusion, 2.1-512-ema-pruned`

For a full list, see https://github.com/easydiffusion/sdkit/tree/main/sdkit/models/models_db

## BUILD and INSTALL

Build as:

`python3 -m build`

Install as:

`python3 -m pip install .`
