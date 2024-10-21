# Migration
The Python reimplementation provides the same endpoints as the old API, which are
largely functioning the same way. However, there are a few major deviations:

 * Use of typed JSON: e.g., when a value represents an integer, it is returned as integer.
 * Lists when multiple values are possible: if a field can have none, one, or multiple entries (e.g., authors), we always return a list.
 * Restriction or expansion of input types as appropriate.
 * Standardizing authentication and access messages, and consistently execute those checks
  before fetching data or providing error messages about the data.

The list above is not exhaustive. Minor changes include, for example, bug fixes and the removal of unnecessary nesting.
There may be undocumented changes, especially in edge cases which may not have occurred in the test environment.
As the PHP API was underspecified, the re-implementation is based on a mix of reading old code and probing the API.
If there is a behavioral change which was not documented but affects you, please [open a bug report](https://github.com/openml/server-api/issues/new?assignees=&labels=bug%2C+triage&projects=&template=bug-report.md&title=).

## All Endpoints
The following changes affect all endpoints.

### Error on Invalid Input
When providing input of invalid types (e.g., a non-integer dataset id) the HTTP header
and JSON content will be different.

```diff title="HTTP Header"
- 412 Precondition Failed
+ 422 Unprocessable Entity
```

```diff title="JSON Content"
- {"error":{"code":"100","message":"Function not valid"}}
+ {"detail":[{"loc":["query","_dataset_id"],"msg":"value is not a valid integer","type":"type_error.integer"}]}
```

!!! warning "Input validation has been added to many end points"

   There are endpoints which previously did not do any input validation.
   These endpoints now do enforce stricter input constraints.
   Constraints for each endpoint parameter are documented in the API docs.

### Other Errors
For any other error messages, the response is identical except that outer field will be `"detail"` instead of `"error"`:

```diff title="JSON Content"
- {"error":{"code":"112","message":"No access granted"}}
+ {"detail":{"code":"112","message":"No access granted"}}
```

In some cases the JSON endpoints previously returned XML ([example](https://github.com/openml/OpenML/issues/1200)), the new API always returns JSON.

```diff title="XML replaced by JSON"
- <oml:error xmlns:oml="http://openml.org/openml">
-   <oml:code>103</oml:code>
-   <oml:message>Authentication failed</oml:message>
- </oml:error>
+ {"detail": {"code":"103", "message": "Authentication failed" } }
```

## Datasets

### `GET /{dataset_id}`
 - Dataset format names are normalized to be all lower-case
   (`"Sparse_ARFF"` ->  `"sparse_arff"`).
 - Non-`arff` datasets will not incorrectly have a `"parquet_url"` ([openml#1189](https://github.com/openml/OpenML/issues/1189)).
 - If `"creator"` contains multiple comma-separated creators it is always returned
   as a list, instead of it depending on the quotation used by the original uploader.
 - For (some?) datasets that have multiple values in `"ignore_attribute"`, this field
   is correctly populated instead of omitted.
 - Processing date is formatted with a `T` in the middle:
  ```diff title="processing_date"
  - "2019-07-09 15:22:03"
  + "2019-07-09T15:22:03"
  ```
 - Fields which may contain lists of values (e.g., `creator`, `contributor`) now always
  returns a list (which may also be empty or contain a single element).
 - Fields without a set value are no longer automatically removed from the response.

### `GET /data/list/{filters}`

The endpoint now accepts the filters in the body of the request, instead of as query parameters.
```diff
-  curl -d '' 127.0.0.1:8002/api/v1/json/data/list/status/active
+ curl -X 'POST' 'http://localhost:8001/v1/datasets/list' \
+  -H 'Content-Type: application/json' \
+  -d '{}'
```
This endpoint is now also available via a `POST` request, and will exhibit the same behavior
regardless of how it is accessed.

When accessing this endpoint when authenticated as administrator, it now correctly
includes datasets which are private.

The `limit` and `offset` parameters can now be used independently, you no longer need
to provide both if you wish to set only one.

### `POST /datasets/tag`
When successful, the "tag" property in the returned response is now always a list, even if only one tag exists for the entity.
For example, after tagging dataset 21 with the tag `"foo"`:
```diff
{
   data_tag": {
      "id": "21",
-      "tag": "foo"
+      "tag": ["foo"]
   }
}
```

## Studies

### `GET /{id_or_alias}`

Old-style "legacy" studies which are solely based on tags are no longer supported.

??? info "Affected Legacy Studies"

    Only 24 old studies were affected by this change, listed below.
    There is currently not yet a migration plan for these studies.

    | id	| name|
    | --: | :-- |
    |1	|A large-scale comparison of classification algorit...|
    |2	|Fast Algorithm Selection using Learning Curves|
    |3	|Multi-Task Learning with a Natural Metric for Quan...|
    |5	|Local and Global Feature Selection on Multilabel T...|
    |7	|Massive machine learning experiments using mlr and...|
    |8	|Decision tree comparaison|
    |10|	Collaborative primer|
    |11|	Having a Blast: Meta-Learning and Heterogeneous En...|
    |12|	Subspace Clustering via Seeking Neighbors with Min...|
    |13|	Meta-QSAR: learning how to learn QSARs|
    |17|	Subgroup Discovery|
    |20|	Mythbusting data mining urban legends through larg...|
    |22|	Identifying critical paths in undergraduate progra...|
    |24|	OpenML R paper|
    |25|	Bernd Demo Study for Multiclass SVMs OML WS 2016|
    |27|	Compare three different SVM versions of R package ...|
    |30|	OpenML Paper Study|
    |31|	Iris Data set Study|
    |32|	Data Streams and more|
    |34|	Massively Collaborative Machine Learning|
    |37|	Speeding up Algorithm Selection via Meta-learning ...|
    |38|	Performance of new ctree implementations on classi...|
    |41|	ASLib OpenML Scenario|
    |50|	Hyper-parameter tuning of Decision Trees|
    |51|	ensemble on diabetes	|

## Flows

### `GET /flow/exists/{name}/{external_version}/`
Behavior has changed slightly. When a flow is found:

```diff
- { "flow_exists": { "exists": "true", "flow_id": "123" } }
+ { "flow_id": 123 }
```

and when a flow is not found:
```diff
- { "flow_exists": { "exists": "false", "flow_id": "-1" } }
+ { "detail": "Flow not found." }
```
and the HTTP header status code is `404` (NOT FOUND) instead of `200` (OK).

In the future the successful case will more likely just return the flow immediately instead (see #170).

## Others

### `GET /estimationprocedure/list`
The `ttid` field has been renamed to `task_type_id`.
All values are now typed.
Outer levels of nesting have been removed.

#### `GET /evaluationmeasures/list`
Outer levels of nesting have been removed.
