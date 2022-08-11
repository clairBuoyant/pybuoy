# Contributing to `pybuoy`

Thank you for your interest in contributing!

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before you contribute, as being part of this community means that you agree to abide by it.

## Guidelines

Here are the guidelines we'd like you to follow:

- [Questions?](#question)
- [Issues and Bugs](#issue)
- [Feature Requests](#feature)
- [Submission Guidelines](#submit)

## <a name="question"></a> Got a Question?

Create an [issue](https://github.com/clairBuoyant/pybuoy/issues) with your questions.

## <a name="issue"></a> Found an Issue?

If you find a bug in the source code or a mistake in the documentation, you can help us by
submitting an issue [here](https://github.com/clairBuoyant/pybuoy/issues) or submit a Pull Request with a fix.

See [below](#submit) for additional guidelines.

## <a name="feature"></a> Want a Feature?

You can request a new feature by submitting a feature request [here](https://github.com/clairBuoyant/pybuoy/issues).

## <a name="submit"></a> Submission Guidelines

### Submitting a Pull Request

- Commit your changes using a descriptive commit message.

  ```shell
  git commit -a
  ```

  Note: the [optional commit `-a` command line option](https://git-scm.com/docs/git-commit#Documentation/git-commit.txt--a) will automatically "add" and "rm" edited files.

- Build your changes locally to ensure all the tests pass:

  ```shell
  poetry run test
  ```

- Push your branch to GitHub:

  ```shell
  git push -u origin my-local-branch
  ```

- Keep your branch updated with `main`:

  ```shell
  git rebase main
  ```

- If we suggest changes then:

  - Make the required updates.
  - Re-run the test suite to ensure tests are still passing.
  - Rebase your branch and force push to your GitHub repository (this will update your Pull Request):

    ```shell
    git rebase main -i
    git push origin my-local-branch -f
    ```

    Note: [`-i` is an optional flag](https://git-scm.com/docs/git-rebase#Documentation/git-rebase.txt--i) that generates a list of commits that are about to rebased.
