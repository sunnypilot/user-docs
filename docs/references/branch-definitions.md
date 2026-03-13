|Branch | Definition | Supported Devices | Description | Stability/Readiness|
|:-: | --- | --- | --- | ---|
|`release-tizi` | Release branch | comma 3X | Stable release branch. After testing on `staging`, updates are pushed here and published publicly. | **Ready to Use:** Highly stable, recommended for most users.|
|`staging` | Staging branch | comma four/3X | Pre-release testing branch. Community feedback is essential to identify issues before public release. | **Varied Stability:** Generally stable, but intended for testing before public release.|
|`dev` | Development branch | comma four/3X | Experimental branch with the latest features and bug fixes brought in manually. Expect bugs and breaking changes. | **Experimental:** Least stable, suitable for testers and developers.|
|`master` | Primary development branch | comma four/3X | All Pull Requests are merged here for future releases. CI automatically strips, minifies, and pushes changes to `staging`. Running the `master` branch is suitable for development purposes but not recommended for non-development use. | **For Development Use:** Suitable for developers, may be unstable for general use.|
|`master-dev` | Development branch | comma four/3X | Using `master` as the base branch, this branch is set up for CI runs to merges any PR that has the `dev-c3` label on a Pull Request. This is the branch that builds the `dev` prebuilt. As it gets automatically rebased and force-pushed whenever there is a new commit on `master`, it is not recommended for general usage. | For CI Use: Not suitable for developers or general use. |
|`release-tici` | Release branch | comma three | Stable release branch. After testing on `staging-tici`, updates are pushed here and published publicly. | Not Yet Available ~~**Ready to Use:** Highly stable, recommended for most users.~~|
|`staging-tici` | Staging branch | comma three | Pre-release testing branch. Community feedback is essential to identify issues before public release. | **Varied Stability:** Generally stable, but intended for testing before public release.|

> [!tip]
>Your feedback is invaluable. Testers, even without software development experience, are encouraged to run `staging` or `dev` and report issues.
