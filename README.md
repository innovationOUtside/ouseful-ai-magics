# ouseful-ai-magics

*The __quickest__ way of getting started with locally run LLMs and Stable Diffusion image generation models in Juoyter notebooks...*

Simple IPython magics for experimenting with locally run generative AI text and image models.

Magics built around third party Python packages offering Python APIs to generative models:

- [`llm`](https://github.com/simonw/llm): command line and Python API for `gpt4all` `.gguf` format text models)
- [`sdkit`](https://github.com/easydiffusion/sdkit): Python API for locally run Stable Diffusion

Only tested on Mac M2. Dependencies may vary for other platforms (check original package repos for details; please post an issue with differing dependency requirements for other platforms etc.)

## Installation

`pip install git+https://github.com/innovationOUtside/ouseful-ai-magics.git`

or

`pip install https://github.com/innovationOUtside/ouseful-ai-magics/archive/refs/heads/main.zip`

For best performance, you should also regularly check that you are using the nmost recent versions of `llm` and `gpt4all`:

```bash
pip install --upgrade llm gpt4all
llm install -U llm-gpt4all
```

## Getting Started

Load the magics:

- `%load_ext ouseful_ai_magics`
- `%reload_ext ouseful_ai_magics`

## Finding and Downloading Models

The `gpt4all` package maintainers publish a list of recommended models available for use with the *GPT4All* application; run the command line command __`llm models list`__ to list the available models.

## Additional models

A wide range of additional models can be accessed by installing the appropriate [`llm` plugin](https://llm.datasette.io/en/stable/plugins/directory.html#plugin-directory).

### `llm-llama-cpp` plugin

The [`llm-llama-cpp`](https://github.com/simonw/llm-llama-cpp) plugin supports models that can be downloaded from HuggingFace.

Install (or update) the plugin with: `llm install -U llm-llama-cpp`. Note there is an additional dependency on`llm install llama-cpp-python` (or on Mac M1/M2: `CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 llm install llama-cpp-python`).

Download a model and provide an alis from the command line.

For models that support the *Llama 2 Chat* prompt format, use the `--llama2-chat` switch in a command of the form:

```bash
llm llama-cpp download-model \
  https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q6_K.gguf \
  --alias llama2-chat --alias l2c --llama2-chat
```

Connect to the model using the alias, for example: `%llm_connect l2c`.

### Manually downloading additional models from HuggingFace

You can manually download additional models from Hugging Face using the `huggingface-cli` command line tool shipped as part of the [`huggingface_hub`](https://github.com/huggingface/huggingface_hub) Python package:

```bash
#pip install --upgrade huggingface_hub
# huggingface-cli download HUGGINGFACE_REPO MODELNAME --local-dir DOWNLOAD_PATH
# Examples:
huggingface-cli download TheBloke/Llama-2-7b-Chat-GGUF llama-2-7b-chat.Q4_K_M.gguf --local-dir ~/.cache/gpt4all --local-dir-use-symlinks False

huggingface-cli download TheBloke/CodeLlama-7B-Python-GGUF codellama-7b-python.Q4_K_M.gguf --local-dir ~/.cache/gpt4all --local-dir-use-symlinks False

huggingface-cli download TheBloke/WizardCoder-Python-7B-V1.0-GGUF wizardcoder-python-7b-v1.0.Q4_K_M.gguf --local-dir ~/.cache/gpt4all --local-dir-use-symlinks False
```

*If the `--local-dir-use-symlinks True` flag is set (default), HuggingFace models are dowmnloaded to model specific directories on the path `~/.cache/huggingface/hub/`.*

Register the model with `llm` using a command-line command of the form:

`llm llama-cpp add-model ~/.cache/gpt4all/llama-2-7b-chat.Q4_K_M.gguf --alias llama2chat --llama2-chat`

Connect to the model using the alias, for example: `%llm_connect llama2chat`.

## Text generation

You can connect to an `llm` model that is available that is identified via the `llm models list` command as:

- `%llm_connect mistral-7b-instruct-v0` (default)
- `%llm_connect mistral-7b-openorca`

If the model is not available it will be automatically downloaded.

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

### Alternative prompts

Some models may require custom prompt styles. For example, the statling 7b model, dowmnloaded as: 

```text
!huggingface-cli download TheBloke/Starling-LM-7B-alpha-GGUF starling-lm-7b-alpha.Q4_K_M.gguf --local-dir ~/.cache/gpt4all --local-dir-use-symlinks False

!llm llama-cpp add-model ~/.cache/gpt4all/starling-lm-7b-alpha.Q4_K_M.gguf --alias starling7b

%llm_connect starling7b
```

requires (via the Hugging face model page) a prompt of the form: `GPT4 User: {{input}}<|end_of_turn|>GPT4 Assistant:`

Explicitly set the prompt style, being sure to include `{{input}` as part of the prompt, using the `--prompt-template / -p` switch:

`%%llm -p "GPT4 User: {{input}}<|end_of_turn|>GPT4 Assistant:"``

Alternatively, some custom prompt styles may be defined, as in this case, and be used by setting the `--prompt-style / -P` flag, for example:

`%%llm -P starling`

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
What is your name?
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

Models are dowmnloaded to model specific directories on the path `~/.cache/huggingface/hub/`

### `%%sdkit` image generation

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

We can also manipulate what is returned:

- `--file_path / -f`, save as file (give filename, eg `generated_img.png`, `path/to/generated_img.jpg` )
- `--return_object / -r`, default=False, return image object(s) (default: False).

Show status of loaded model:

`%sdkit_about`

Deallocate the model:

`%sdkit_clear`

Example models:

- `stable-diffusion, 1.5-pruned` (default)
- `stable-diffusion, 2.1-512-ema-pruned`

For a full list, see https://github.com/easydiffusion/sdkit/tree/main/sdkit/models/models_db

## `llava` multimodal (image to text) model

*NOT YET AVAILABLE - waiting in part on https://github.com/abetlen/llama-cpp-python/issues/813*
## BUILD and INSTALL

Build as:

`python3 -m build`

Install as:

`python3 -m pip install .`
