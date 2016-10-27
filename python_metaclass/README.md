# Metaclass Fun!

I was curious if it would be possible to create classes that could be
declared like:

```
class Apple(FruitBase):
    color = 'green'
    taste = 'great'
```

but... with the supplied attributes and values ending up as instance
variables instead of class variables.  In the above example, that
would allow multiple Apples to have different colors and tastes while
still supplying sensible defaults.