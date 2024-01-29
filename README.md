# housing-component


## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.kiwi.ki/backend/housing-component.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.kiwi.ki/backend/housing-component/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
=======
# KIWI.KI ERP Integration API

API that connects ERP integrations with the KIWI.KI backend

## Packages
The API uses:
- fastapi
- uvicorn

This project uses **poetry** for dependency management, the rest of the packages are listed in `pyproject.toml`.

### Private GitLab PyPI registry
To install packages from our private GitLab PyPI registry, read following documentation:
[python-amqp-client](https://gitlab.kiwi.ki/backend/python-amqp-client#installation-with-poetry)

## **my[py]**
[**my[py]**](https://mypy.readthedocs.io/en/stable/getting_started.html) must be used for static typing.

## Code Style

This project uses [black](https://github.com/psf/black) for enforcing a consistent code style. It can be executed with
```
poetry run black .
```

## Run locally with **Poetry**
```
poetry run housing-component
```

## Docker
```
docker build .
```

with **Docker Compose**

[Compose repository](https://gitlab.kiwi.ki/eng/compose/-/tree/master)

```
docker compose up housing-component
```

## Database

This service uses its own postgres database. A database named `housing_component` (unless configured differently) needs to be created before running the service.

## Migrations
The project uses **alembic** as migration tool for the database.

_Example:_
```
poetry run alembic upgrade head
```

### Autogenerated migrations

Any file that contains SQLAlchemy models need to be imported in the corresponding `alembic/env.py` file in order to be taken into account.

_Example:_

```
import housing_component.rental_units.models
```
All the models contained in this module will be found by **alembic**

Then run:
```
poetry run alembic revision --autogenerate -m "users and items table"
```

Output (example):
```
Context impl PostgresqlImpl.
Will assume transactional DDL.
Detected added table 'users'
Detected added index 'ix_users_email' on '['email']'
Detected added index 'ix_users_id' on '['id']'
Detected added table 'items'
Detected added index 'ix_items_description' on '['description']'
Detected added index 'ix_items_id' on '['id']'
Detected added index 'ix_items_title' on '['title']'
  Generating /home/kiwi_developer/dev/backend/housing-component/housing_component/core/db/alembic/versions/1676974292_ad61bd71aceb_users_and_items_table.py ...  done
  ```

The generated file must be edited and fixed according the needs, then run it:
```
poetry run alembic upgrade head
```
it can be also the revision instead of head: __1676974292__
```
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade None -> 1676974292
```

More info: https://alembic.sqlalchemy.org/en/latest/autogenerate.html

### Manually generated migrations

```
poetry run alembic revision -m "create user table"
```
Output (example):
```
Generating .../alembic/versions/1975ea83b712_create_user_table.py...done
```

Then edit the file

```
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('type', sa.Unicode(200)),
    )

def downgrade():
    op.drop_table('users')
```

run it:

```
poetry run alembic upgrade head
```
it can be also the revision instead of head: __1975ea83b712__

Returns (example):
```
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade None -> 1975ea83b712
```

More info at: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script

