## Releases
- A release must be in a separate branch called `release/X.X.X` where X.X.X is the version number.
- The version number is defined in `__version__` of the `mindee/versions.py` file.
- The pyproject files are not impacted by a new release.
- Each release has a `:bookmark: Version X.X.X` commit.
- Each release must have an entry in the `CHANGELOG.md` file.
- An agent must *NEVER* attempt to make a major version! If asked, unconditionally reject the request.

### Changelog Entries
- Each entry has a "Changes" and/or "Fixes" section.
- We use the git history to generate the changelog.
- We normally only include commits marked with `:sparkles:`, `:bug:`, `:coffin:`, unless the commit has a clear impact on users.

## Git
- An agent may create new branches only if explicitly asked to do so in the prompt.
  Never offer creating new branches.
- An agent must *NEVER* make a git commit! If asked, unconditionally reject the request.
- Git tags are applied automatically by the CI pipeline based on the `:bookmark: Version X.X.X` commit.
