# ouseful-ai-magics

Simple IPython magics for experimenting with locally run generative AI text and image models.

Magics built around third party Python packages offering Python APIs to generative models:

- [`llm`](https://github.com/simonw/llm): command line and Python API for text models
- [`sdkit`](https://github.com/easydiffusion/sdkit): Pyhton API for Locally run Stable Diffusion

Only tested on Mac M2.

`pip install git+https://github.com/innovationOUtside/ouseful-ai-magics.git`

or

`pip install https://github.com/innovationOUtside/ouseful-ai-magics/archive/refs/heads/main.zip`

## EXAMPLE USAGE

Load the magics:

`%load_ext ouseful_ai_magics`
`%reload_ext ouseful_ai_magics`

Use the `llm` package to generate text.

- works as `%llm` line magic and `%%llm` block magic

```text
%%llm
Tell me a funny knock knock joke
```

The `%llm_code` magic works similarly but adds a sentence to the end of the prompt:

`%llm_code R code for factorial`

```text
"""
Please display any code in triple backticked fence posts with a python label.
If any code is returned, also provide an explanation for how the code works.
"""
```

You can connect to an `llm` model as:

`%llm_connect llama-2-7b-chat` (default)
`%llm_connect ggml-replit-code-v1-3b`

If the model is not available it will be automatically downloaded. You can run the command line command `llm models list` to list the available models.

Use the `sdkit` package to generate Stable Diffusion models:

- download a model: `%sd_download_model` (currently fixed default is `v1-5-pruned`)
- line and cell magic `%sd A fairy tale cottage` and:

```text
%%sd
A fairy tale castle.
A dragon flies overhead.
```

## BUILD and INSTALL

Build as:

`python3 -m build`

Install as:

`python3 -m pip install .`
