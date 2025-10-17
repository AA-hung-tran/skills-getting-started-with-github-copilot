# Tests for Mergington High School Activities API

This directory contains comprehensive tests for the FastAPI application.

## Test Structure

- `conftest.py` - Test configuration and fixtures
- `test_api.py` - API endpoint tests

## Running Tests

### Run all tests:
```bash
pytest tests/
```

### Run tests with verbose output:
```bash
pytest tests/ -v
```

### Run tests with coverage:
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Run tests with coverage HTML report:
```bash
pytest tests/ --cov=src --cov-report=html
```

## Test Coverage

The current test suite achieves 100% code coverage for the `src/app.py` file.

## Test Categories

### API Endpoint Tests (`test_api.py`)

1. **Root Endpoint Test**
   - Tests that the root URL serves the HTML page

2. **Activities Endpoint Tests**
   - Tests retrieving all activities
   - Validates activity data structure

3. **Signup Endpoint Tests**
   - Tests successful student registration
   - Tests duplicate registration prevention
   - Tests registration for non-existent activities

4. **Unregister Endpoint Tests**
   - Tests successful student unregistration
   - Tests unregistration of non-registered students
   - Tests unregistration from non-existent activities

5. **Integration Tests**
   - Tests activity capacity tracking
   - Tests multiple signups and removals
   - Tests end-to-end workflows

## Test Features

- **Data Reset**: Each test method resets the activities data to ensure test isolation
- **Error Handling**: Tests cover both success and error scenarios
- **HTTP Status Codes**: Validates proper HTTP response codes
- **Response Content**: Validates response message content and structure
- **State Verification**: Tests verify that operations actually change the application state