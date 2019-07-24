[![Build Status](https://travis-ci.com/Alexei-Kornienko/schematics_to_swagger.svg?branch=master)](https://travis-ci.com/Alexei-Kornienko/schematics_to_swagger)

# Usecase

* I have a REST API built using aiohttp and schematics.
* I want to provide Swagger spec for it and I use aiohttp-swagger.
* I'm too lazy to describe models for swagger docs so I want to build this information automatically

## Usage

```
import schematics_to_swagger

from your_package import models

definitions = schematics_to_swagger.read_models_from_module(models)
```
