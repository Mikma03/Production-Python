<!-- TOC -->

- [Python Optimization](#python-optimization)
  - [Fred Baptiste course](#fred-baptiste-course)
    - [Interning, String Interning, Peephole](#interning-string-interning-peephole)
    - [Decimals: Performance Considerations](#decimals-performance-considerations)
  - [High Performance Python - Profiling to Find Bottlenecks](#high-performance-python---profiling-to-find-bottlenecks)
  - [Expert Python Programming - Code Optimization](#expert-python-programming---code-optimization)
- [Profiling Python code](#profiling-python-code)
- [WebPages \& Blogs](#webpages--blogs)
  - [PyO3 - Rust and Python](#pyo3---rust-and-python)
  - [Faster Python code](#faster-python-code)
- [Algorithm](#algorithm)
- [Liblaries](#liblaries)
  - [Profiling your Python code](#profiling-your-python-code)
  - [Make your Python code faster](#make-your-python-code-faster)

<!-- /TOC -->

# Python Optimization

## Fred Baptiste course

### Interning, String Interning, Peephole

> https://www.udemy.com/course/python-3-deep-dive-part-1/learn/lecture/7192348#overview

> https://www.udemy.com/course/python-3-deep-dive-part-1/learn/lecture/7368670#overview

> https://www.udemy.com/course/python-3-deep-dive-part-1/learn/lecture/7368672#overview

### Decimals: Performance Considerations

> https://www.udemy.com/course/python-3-deep-dive-part-1/learn/lecture/7649326#overview

## High Performance Python - Profiling to Find Bottlenecks

> https://learning.oreilly.com/library/view/high-performance-python/9781492055013/ch02.html

## Expert Python Programming - Code Optimization

> https://learning.oreilly.com/library/view/expert-python-programming/9781801071109/Text/Chapter_13.xhtml#_idParaDest-258

# Profiling Python code

- py-spy: Sampling profiler for Python programs
  - https://github.com/benfred/py-spy?fbclid=IwAR00zoutmVZYTOWxnEypGbXwQPpIYi9EVhnucC6z6uJW8gxJrO1d9Ls3Ies

# WebPages & Blogs

## PyO3 - Rust and Python

> https://pyo3.rs/v0.18.1/

## Faster Python code

> https://pythonspeed.com/

# Algorithm

How to approach Python optimization task.

1. Understand the problem: Analyze the problem you want to solve and determine the input-output relationship. Make sure you understand the requirements and constraints of the problem.

2. Write a baseline implementation: Write a simple, working implementation of the problem without focusing on optimization. This will help you to test and compare optimized versions later.

3. Profile the baseline code: Use Python profiling tools like cProfile, py-spy, or built-in Python timeit module to identify bottlenecks and parts of the code that consume the most time or resources.

Optimize the code:

- a. Algorithmic optimization: Analyze the algorithm used in your implementation and try to find more efficient algorithms to solve the problem. This can have the biggest impact on performance.

- b. Data structures: Choose appropriate data structures for the problem, such as sets, dictionaries, or lists, depending on the requirements.

- c. Pythonic optimizations: Apply Python best practices and optimizations such as list comprehensions, using the map() and filter() functions, or functools.lru_cache for caching results of expensive functions.

- d. Parallelism: Consider using parallelism to divide the problem into smaller tasks and execute them concurrently, using libraries like concurrent.futures, multiprocessing, or asyncio.

- e. External libraries: Look for third-party libraries that can help optimize specific parts of the code, such as NumPy for numerical computations or Cython for compiling Python code to C.

- f. Profiling-guided optimizations: Apply the learnings from the profiling step to specifically target the identified bottlenecks and optimize the relevant code sections.

Validate the optimized code: Ensure that the optimized code still provides correct results by comparing its output to the baseline implementation. Consider using unit tests to automate the validation process.

Measure performance improvements: Profile the optimized code and compare its performance to the baseline implementation. If the performance improvement is not satisfactory, return to step 3 and iterate.

Document the optimization process: Keep a record of the optimizations applied, the performance improvements achieved, and any trade-offs made during the optimization process. This will help you and others to understand the rationale behind the changes and make future optimizations easier.

# Liblaries

## Profiling your Python code

1. `cProfile`: A built-in Python module for deterministic profiling of Python programs.

- https://docs.python.org/3/library/profile.html

2. `py-spy`: A sampling profiler for Python programs that can profile running processes without the need for modifying or restarting the code.

- https://github.com/benfred/py-spy

3. `line_profiler`: A line-by-line profiler to measure the execution time of individual lines of code.

- https://github.com/pyutils/line_profiler

4. `memory_profiler`: A module for monitoring memory usage of a Python program on a line-by-line basis.

- https://github.com/pythonprofilers/memory_profiler

5. `pstats`: A built-in Python module for processing data generated by the cProfile module.

- https://docs.python.org/3/library/profile.html#module-pstats

6. `snakeviz`: A web-based viewer for Python profiling data, which can visualize the output from cProfile or py-spy.

- https://jiffyclub.github.io/snakeviz/

## Make your Python code faster

1. NumPy: A powerful library for numerical computing with a focus on performance.

- https://numpy.org/

2. SciPy: A library built on NumPy for scientific and technical computing.

- https://www.scipy.org/

3. Polars: A high-performance library for data manipulation and analysis.

- https://github.com/pola-rs/polars

4. Cython: A programming language that makes writing C extensions for Python as easy as writing Python itself. It can significantly speed up Python code by compiling it to C.

- https://cython.org/

5. Numba: A Just-In-Time (JIT) compiler for Python that translates a subset of Python and NumPy code into fast machine code.

- http://numba.pydata.org/

6. Dask: A parallel computing library for out-of-core and distributed computing that can parallelize NumPy, Pandas, and other libraries.

- https://dask.org/

7. concurrent.futures: A built-in Python module for asynchronously executing callables, which can be used for parallelism.

- https://docs.python.org/3/library/concurrent.futures.html

8. multiprocessing: A built-in Python module for parallelism using multiple processes.

- https://docs.python.org/3/library/multiprocessing.html

9. asyncio: A built-in Python module for asynchronous I/O and concurrency using coroutines.

- https://docs.python.org/3/library/asyncio.html

10. joblib: A set of tools for lightweight pipelining and parallelism in Python.

- https://joblib.readthedocs.io/

11. PyO3: A library for writing Rust code that can be used in Python programs, which can help speed up performance-critical sections.

- https://pyo3.rs/
