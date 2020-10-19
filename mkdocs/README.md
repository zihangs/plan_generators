# Documentation built with MkDocs

My Development Environment: Ubuntu_20.04 LTS, with python 3.8.2

1. Install MkDocs

```sh
$ pip install mkdocs
```

2. Build a new MkDocs project

```sh
# mkdocs new <project_name>
$ mkdocs new mkdocs
```

This command only run at the first time, if you clone this repo, you don't need to run this

3. Writing documents in MkDocs project

```sh
# move to mkdocs project
$ cd mkdocs

# list this directory
$ ls
$ docs  mkdocs.yml
```

There is a directory ``docs/`` and a file ``mkdocs.yml``, all Markdown files need to be stored in ``docs/`` and we also need to config ``mkdocs.yml`` accordingly. More details see the official website [here](https://www.mkdocs.org/).

In this doc project, material theme is used, [instruction for installing](https://squidfunk.github.io/mkdocs-material/getting-started/).

4. Test and deploy

When writing a Markdown file, we can get a real time preview by running the command below

```sh
$ mkdocs serve
```

Then, we can access the local testing URL: http://127.0.0.1:8000. Once you saved your changes locally, this webpage will automatically reload and display the changes.

5. Deploy on GitHub Pages

Save all the changes you made, then run the command below

```sh
$ mkdocs gh-deploy
```

Then the documentations are public available via this URL: https://zihangs.github.io/plan_generators/ (this URL is only for this MkDocs project). If you build you own MkDocs project and host it with GitHub Pages, you can check the URL in you GitHub repo> Settings > GitHub Pages

