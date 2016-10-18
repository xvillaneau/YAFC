# YAFC - Yet Another Factorio Calculator

Tool intended for use with [Factorio](https://www.factorio.com/), a game about building a factory and making everything as automated as possible.

This tool aims to help computing the dimensions of a new production line: from an expected output flow of items, YAFC will find all the steps required from raw materials to the final product, then compute the flows of intermediate product at every step, then will finally output the required number of machines for the task.

## Versions

### v0.1 (WIP)

Initial basic POC. Only works for simple production schemes with the following constraints:

- No loops,
- Every item (outside raw materials) is the product of *one and only one* recipe,
- Recipes can only have one output product.

Consequently, this version is restricted mostly to the "Vanilla" game (most mods implement complex production schemes) and had to leave aside all aspects of oil processing. Other than that, all resources are present.

This is still WIP so there is no convenient CLI yet, but I intend to fix that.

### Further ideas

- Find an algorithm that works in more general product flows
- Get modules in there
- Mod support
- Some form of UI?

## Licensing

This source code is released under the MIT license.

Factorio is a game by Wube Software Ltd, all rights reserved.
(if you haven't played it yet, then you probably should)
