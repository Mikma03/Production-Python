<!-- TOC -->

- [Manual Execution](#manual-execution)
- [Updating Pre-Commit](#updating-pre-commit)
- [Conclusion](#conclusion)
- [YouTube videos](#youtube-videos)

<!-- /TOC -->
    rev: v3.4.0
    hooks:
    -   id: check-yaml
    -   id: end-of-file-fixer
    -   id: trailing-whitespace


Once you've set up your `.pre-commit-config.yaml`, you can install the git hook scripts with the following command:

```bash
pre-commit install
```

Now, `pre-commit` will run automatically on `git commit`.

## Manual Execution

You can also run your hooks manually without making a commit using the following command:

```bash
pre-commit run --all-files
```

## Updating Pre-Commit

To upgrade to the latest version, you can use pip:

```bash
pip install --upgrade pre-commit
```

## Conclusion

`Pre-commit` is a valuable tool for maintaining high code quality. It checks your code for any issues or errors before the code makes its way into your main codebase, allowing you to catch and fix issues before they become bigger problems. By incorporating `pre-commit` into your development process, you can save time and ensure that your project maintains a high level of code quality.

## YouTube videos

Here are some YouTube videos related to `pre-commit` in Python:

1. [The easy way to keep your repos tidy](https://www.youtube.com/watch?v=psjz6rwzMdk) by mCoding
    
    - Description: Catch simple issues before code review using pre-commit. Pre-commit uses git hooks in order to catch your little typos before they…

2. [Python Pre-Commit Hooks Setup in a single video!](https://www.youtube.com/watch?v=Wmw-VGSjSNg) by Haydn Murray
    
    - Description: Hey everyone! A one-stop-shop for setting up and configuring Python Pre-commit git hooks in one video. Adding it to a repo,…

3. [Increase Python code quality with pre-commit](https://www.youtube.com/watch?v=XFyLzr5Ehf0) by Pybites
    
    - Description: In this video we show you how we use pre-commit to automatically run black, flake8, isort and pyupgrade before committing any…

4. [Precommit Hooks Are Bad](https://www.youtube.com/watch?v=RAelLqnnOp0) by Theo - t3․gg
    
    - Description: Precommit hooks are the actual worst thing and I hope this convinces y'all to use them less. ALL MY CONTENT IS FILMED LIVE…

5. [Configuring Pre-Commit Hooks to Automate Python Testing and Linting in vscode (Visual Studio Code)](https://www.youtube.com/watch?v=moVieAAk_xo) by John Solly
    
    - Description: In this video tutorial, I'll show you how to set up pre-commit hooks to automatically run Python tests and linting checks every time…
