************
Version 4.12
************

Release date: 2019-08-22

This release contains a number of bug fixes and new features since the release of pgAdmin4 4.11.

New features
************

| `Issue #4144 <https://redmine.postgresql.org/issues/4144>`_ -  Add support of Compound Triggers for EPAS 12+.
| `Issue #4333 <https://redmine.postgresql.org/issues/4333>`_ -  Add support for planner support functions in PostgreSQL 12+ functions.
| `Issue #4334 <https://redmine.postgresql.org/issues/4334>`_ -  Add support for generated columns in Postgres 12+.
| `Issue #4540 <https://redmine.postgresql.org/issues/4540>`_ -  Use the full tab space for CodeMirror instances on dialogues where appropriate.
| `Issue #4549 <https://redmine.postgresql.org/issues/4549>`_ -  Allow a banner to be displayed on the login and other related pages showing custom text.
| `Issue #4566 <https://redmine.postgresql.org/issues/4566>`_ -  Allow enhanced cookie protection to be disabled for compatibility with dynamically addressed hosting environments.
| `Issue #4570 <https://redmine.postgresql.org/issues/4570>`_ -  Add an optimisation to the internal code responsible for searching for treeview nodes.
| `Issue #4574 <https://redmine.postgresql.org/issues/4574>`_ -  Display the row count in the popup message when counting table rows, not just in the properties list.

Housekeeping
************

| `Issue #4554 <https://redmine.postgresql.org/issues/4554>`_ -  Add Reverse Engineered SQL tests for Trigger Functions.
| `Issue #4555 <https://redmine.postgresql.org/issues/4555>`_ -  Add Reverse Engineered SQL tests for Exclusion Constraint.
| `Issue #4560 <https://redmine.postgresql.org/issues/4560>`_ -  Add a --modules option to the RE-SQL test suite to allow testing of specific object types.

Bug fixes
*********

| `Issue #4179 <https://redmine.postgresql.org/issues/4179>`_ -  Fix generation of reverse engineered SQL for tables with Greenplum 5.x.
| `Issue #4229 <https://redmine.postgresql.org/issues/4229>`_ -  Update wcDocker to allow the browser's context menu to be used except in tab strips and panel headers.
| `Issue #4401 <https://redmine.postgresql.org/issues/4401>`_ -  Ensure type names are properly encoded in the results grid.
| `Issue #4414 <https://redmine.postgresql.org/issues/4414>`_ -  Fix generation of reverse engineered SQL for partition table, partitions were shown as a child of indexes.
| `Issue #4489 <https://redmine.postgresql.org/issues/4489>`_ -  Update wcDocker to prevent window state loading creating blank dialogues.
| `Issue #4490 <https://redmine.postgresql.org/issues/4490>`_ -  Fix accessibility issue for checkbox in IE11.
| `Issue #4492 <https://redmine.postgresql.org/issues/4492>`_ -  Ensure the Query Tool doesn't throw an error when viewing the contents of a table with no columns.
| `Issue #4496 <https://redmine.postgresql.org/issues/4496>`_ -  Ensure columns can be created when they are IDENTITY fields with the CYCLE option enabled.
| `Issue #4497 <https://redmine.postgresql.org/issues/4497>`_ -  Ensure purely numeric comments can be saved on new columns.
| `Issue #4508 <https://redmine.postgresql.org/issues/4508>`_ -  Fix accessibility issue for Datetime cell in backgrid.
| `Issue #4520 <https://redmine.postgresql.org/issues/4520>`_ -  Ensure the query tool will work with older versions of psycopg2 than we officially support, albeit without updatable resultsets.
| `Issue #4525 <https://redmine.postgresql.org/issues/4525>`_ -  Ensure command tags are shown in the messages tab of the Query Tool.
| `Issue #4536 <https://redmine.postgresql.org/issues/4536>`_ -  Fix load on demand in View/Edit data mode.
| `Issue #4552 <https://redmine.postgresql.org/issues/4552>`_ -  Fix some errors thrown on the JS console when dragging text in the Query Tool.
| `Issue #4559 <https://redmine.postgresql.org/issues/4559>`_ -  Ensure triggers should be updated properly for EPAS server.
| `Issue #4565 <https://redmine.postgresql.org/issues/4565>`_ -  Fix the reverse engineered SQL for trigger functions with the WINDOW option selected.
| `Issue #4578 <https://redmine.postgresql.org/issues/4578>`_ -  Ensure enable trigger menu should be visible when trigger is disabled.
| `Issue #4581 <https://redmine.postgresql.org/issues/4581>`_ -  Ensure the comment on a Primary Key constraint can be edited under the Table node.
| `Issue #4582 <https://redmine.postgresql.org/issues/4582>`_ -  Fix console error when changing kind(SQL/BATCH) for pgAgent job step.
| `Issue #4585 <https://redmine.postgresql.org/issues/4585>`_ -  Fix double click issue to expand the contents of a cell if the resultset was not editable.
| `Issue #4586 <https://redmine.postgresql.org/issues/4586>`_ -  Fix generation of reverse engineered SQL for Rules.