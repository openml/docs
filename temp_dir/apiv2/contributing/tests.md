# Writing Tests

tl;dr:
 - Setting up the `py_api` fixture to test directly against a REST API endpoint is really slow, only use it for migration/integration tests.
 - Getting a database fixture and doing a database call is slow, consider mocking if appropriate.

## Overhead from Fixtures
Sometimes, you want to interact with the REST API through the `py_api` fixture,
or want access to a database with `user_test` or `expdb_test` fixtures.
Be warned that these come with considerable relative overhead, which adds up when running thousands of tests.

```python
@pytest.mark.parametrize('execution_number', range(5000))
def test_private_dataset_owner_access(
        execution_number,
        expdb_test: Connection,
        user_test: Connection,
        py_api: TestClient,
) -> None:
    fetch_user(ApiKey.REGULAR_USER, user_test)  # accesses only the user db
    get_estimation_procedures(expdb_test)  # accesses only the experiment db
    py_api.get("/does/not/exist")  # only queries the api
    pass
```

When individually adding/removing components, we measure (for 5000 repeats, n=1):

| expdb | user | api | exp call | user call | api get |  time (s) |
|-------|------|-----|----------|-----------|---------|----------:|
|  ❌   |  ❌  | ❌  | ❌      | ❌        | ❌      |      1.78 |
|  ✅   |  ❌  | ❌  | ❌      | ❌        | ❌      |      3.45 |
|  ❌   |  ✅  | ❌  | ❌      | ❌        | ❌      |      3.22 |
|  ❌   |  ❌  | ✅  | ❌      | ❌        | ❌      |    298.48 |
|  ✅   |  ✅  | ❌  | ❌      | ❌        | ❌      |      4.44 |
|  ✅   |  ✅  | ✅  | ❌      | ❌        | ❌      |    285.69 |
|  ✅   |  ❌  | ❌  | ✅      | ❌        | ❌      |      4.91 |
|  ❌   |  ✅  | ❌  | ❌      | ✅        | ❌      |      5.81 |
|  ✅   |  ✅  | ✅  | ✅      | ✅        | ✅      |    307.91 |

Adding a fixture that just returns some value adds only minimal overhead (1.91s),
so the burden comes from establishing the database connection itself.

We make the following observations:

- Adding a database fixture adds the same overhead as instantiating an entirely new test.
- Overhead of adding multiple database fixtures is not free
- The `py_api` fixture adds two orders of magnitude more overhead

We want our tests to be fast, so we want to avoid using these fixtures when we reasonably can.
We restrict usage of `py_api` fixtures to integration/migration tests, since it is very slow.
These only run on CI before merges.
For database fixtures

We will write some fixtures that can be used to e.g., get a `User` without accessing the database.
The validity of these users will be tested against the database in only a single test.

### Mocking
Mocking can help us reduce the reliance on database connections in tests.
A mocked function can prevent accessing the database, and instead return a predefined value instead.

It has a few upsides:
 - It's faster than using a database fixture (see below).
 - The test is not dependent on the database: you can run the test without a database.

But it also has downsides:
 - Behavior changes in the database, such as schema changes, are not automatically reflected in the tests.
 - The database layer (e.g., queries) are not actually tested.

Basically, the mocked behavior may not match real behavior when executed on a database.
For this reason, for each mocked entity, we should add a test that verifies that if the database layer
is invoked with the database, it returns the expected output that matches the mock.
This is additional overhead in development, but hopefully it pays back in more granular test feedback and faster tests.

On the speed of mocks, consider these two tests:

```diff
@pytest.mark.parametrize('execution_number', range(5000))
def test_private_dataset_owner_access(
        execution_number,
        admin,
+        mocker,
-        expdb_test: Connection,
) -> None:
+    mock = mocker.patch('database.datasets.get')
+    class Dataset(NamedTuple):
+        uploader: int
+        visibility: Visibility
+    mock.return_value = Dataset(uploader=1, visibility=Visibility.PRIVATE)

    _get_dataset_raise_otherwise(
        dataset_id=1,
        user=admin,
-        expdb=expdb_test,
+        expdb=None,
    )
```
There is only a single database call in the test. It fetches a record on an indexed field and does not require any joins.
Despite the database call being very light, the database-included test is ~50% slower than the mocked version (3.50s vs 5.04s).
