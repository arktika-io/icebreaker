# Versioning

The [versioning](../../../src/icebreaker/versioning) package implements project version discovery mechanisms facilitating standardized language-neutral versioning across projects.

## Version File Based
[VersionFileBased](../../../src/icebreaker/versioning/_version_file_based.py) versioning strategy allows for a single file to act as the source of truth for the version of your project. The file in question should contain nothing but a single string (regardless of the versioning scheme used) denoting the version of the project. It's recommended that the file be placed in the root of your repository if using a version control system such as git, and committed together with the code. The VersionFileBased versioning strategy will automatically discover the file when the `resolve_version` function is called.

Please note that you must take into consideration the version file when packaging your project. Ensure the version file is copied into the right location(s) before packaging the project up.
