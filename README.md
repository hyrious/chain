## chain.py

Put the [chain.py](chain.py) file and [chain.pyi](chain.pyi) (for auto completion) to your project.

```py
from chain import chain, it
chain(range(10)).map(it * 2).filter(it > 3).to_list()
```

If you're a [pythonic](https://www.python.org/dev/peps/pep-0008/) man, you dislike this library and write:

```py
[t for i in range(10) if (t := i * 2) > 3]
```

Wow, so pythonic, but not me!

### License

MIT @ [hyrious](https://github.com/hyrious)
