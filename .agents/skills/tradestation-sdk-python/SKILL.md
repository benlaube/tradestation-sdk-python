```markdown
# tradestation-sdk-python Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches you the core development patterns and workflows used in the `tradestation-sdk-python` repository. The codebase is a Python SDK for interacting with TradeStation APIs, focusing on clear model definitions, contract testing, and maintainable code organization. You'll learn about file naming, import/export styles, commit conventions, and how to safely update API models and their tests.

## Coding Conventions

### File Naming
- Use **snake_case** for all Python files.
  - Example: `order_executions.py`, `test_pydantic_contract.py`

### Import Style
- Use **relative imports** within the package.
  - Example:
    ```python
    from .models.orders import OrderModel
    from .order_executions import execute_order
    ```

### Export Style
- Use **named exports** (explicitly import/export classes, functions, etc.).
  - Example:
    ```python
    # In tradestation/models/orders.py
    class OrderModel(BaseModel):
        ...
    ```

### Commit Patterns
- Use **conventional commits** with the `fix` prefix for bug fixes.
  - Example commit message:
    ```
    fix: handle optional fields in streaming model (closes #42)
    ```

## Workflows

### Update Model and Contract Test
**Trigger:** When you need to support new response shapes or optional fields in API/streaming models.  
**Command:** `/update-model-contract-test`

1. **Edit the relevant Pydantic model** to accept new or optional fields.
    - Example:
      ```python
      # tradestation/models/orders.py
      class OrderModel(BaseModel):
          id: int
          status: str
          # Add new optional field
          execution_time: Optional[datetime] = None
      ```
2. **Update or add logic** in the implementation to handle the new model behavior.
    - Example:
      ```python
      # tradestation/order_executions.py
      if order.execution_time:
          log_execution_time(order.execution_time)
      ```
3. **Update or add contract tests** to verify the new/changed model behavior.
    - Example:
      ```python
      # tests/test_pydantic_contract.py
      def test_order_model_accepts_execution_time():
          order = OrderModel(id=1, status="filled", execution_time="2024-06-01T12:00:00Z")
          assert order.execution_time is not None
      ```

**Files Involved:**
- `tradestation/models/orders.py`
- `tradestation/models/streaming.py`
- `tradestation/order_executions.py`
- `tests/test_pydantic_contract.py`

**Frequency:** ~2x/month

## Testing Patterns

- **Test File Naming:** Use `*.test.*` pattern (e.g., `test_pydantic_contract.py`).
- **Testing Framework:** Not explicitly specified; likely uses standard Python testing tools (e.g., `pytest` or `unittest`).
- **Test Focus:** Contract tests ensure Pydantic models accept new/optional fields and that changes are covered.

**Example Test:**
```python
def test_streaming_model_handles_optional_field():
    model = StreamingModel(required_field="foo", optional_field="bar")
    assert model.optional_field == "bar"
```

## Commands

| Command                       | Purpose                                                          |
|-------------------------------|------------------------------------------------------------------|
| /update-model-contract-test    | Update Pydantic models and contract tests for new/changed fields |
```
