# Project overview

The Python-based REST API serves several groups of endpoints:

 - `/old/`: serves the old-style JSON format, this should mimic the PHP responses exactly with the only deviations recorded in the [migration guide](../migration.md).
 - `/mldcat_ap/`: serves datasets in [MLDCAT_AP](https://semiceu.github.io/MLDCAT-AP/releases/1.0.0/) format.
 - `/*`: serves new-style JSON format. At this point it is intentionally similar to the old-style format.

The endpoints are specified in subdirectories of `src/routers`.
They pull data from the database through the `src/database` module.
The schemas for each entity, and possible conversions between them, are defined in the `src/schemas` directory.

!!! Failure ""

    Instructions are incomplete. Please have patience while we are adding more documentation.
