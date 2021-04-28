There are basically two ways to solve the reference cyle problem in PyOP2:

1) Keep parloops as combined symbolics and data objects and cache the compiled code globally with some cache key, making sure that the cache key does not depend on any data references.
This means that parloops are disposable/cannot be cached but the generated code can still be reused.
However, it is undesirable to be doing frequent cache lookups and we would like to avoid global caches where possible.

2) Transform parloops into purely symbolic objects with the data passed in via a mapping at compute time.
This is great for Firedrake as it allows us to cache the parloops where we like and reuse them for different data structures.
Also, lookup from a global cache can be avoided.
However, this worsens the experience for users of the PyOP2 API because they now need to pass in a mapping at compute-time when previously this was not needed.

In rough summary: option 1 resolves the problem in an optimal way for PyOP2 users (who use parloops directly) whereas option 2 resolves it optimally for Firedrake developers (who want to cache parloops).

But. There is a way to combine the two and get the best of both worlds! This is achieved in two steps:

1) Change how we instantiate parloops such that `iterset` and `args` hold *weak* references to data.

2) Make the data mapping passed in at compute-time *optional*.
If it is not provided default to using the weak references stored on the `Arg` objects.

This means that if you are a PyOP2 user, where you are using parloops directly, you can continue to use them as before.
However, if you are a Firedrake developer, caching parloops is now easy because they no longer hold onto data references and the input and output data structures can be modified at compute-time.