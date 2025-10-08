# Contributing to ANWB Road Events Predictor

Thank you for your interest in contributing to the ANWB Road Events Predictor! This document provides guidelines and instructions for contributing to this project.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing](#testing)
6. [Documentation](#documentation)
7. [Pull Request Process](#pull-request-process)

## Code of Conduct

This project is an academic collaboration. We expect all contributors to:
- Be respectful and constructive in discussions
- Focus on what is best for the project and community
- Show empathy towards other contributors
- Accept constructive criticism gracefully

## Getting Started

### Prerequisites

Before you begin, ensure you have:
- Python 3.10.12 installed
- PostgreSQL 12+ installed
- Git configured on your machine
- Familiarity with Django and machine learning concepts

### Setup Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/anwb-road-events-predictor.git
   cd anwb-road-events-predictor
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Install dependencies**
   ```bash
   poetry install
   poetry shell
   ```

4. **Set up pre-commit hooks** (optional but recommended)
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Development Workflow

### Branching Strategy

We use the following branch structure:
- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Urgent production fixes

### Workflow Steps

1. **Create an issue** describing the feature or bug
2. **Create a branch** from `develop`
3. **Make your changes** with clear, atomic commits
4. **Write tests** for your changes
5. **Update documentation** as needed
6. **Submit a pull request** to `develop`

### Commit Messages

Follow the conventional commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```bash
feat(model): add ensemble prediction method
fix(api): handle unknown street names gracefully
docs(readme): update installation instructions
```

## Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

- **Line Length**: 100 characters (not 79)
- **Quotes**: Double quotes for strings
- **Imports**: Organized in three groups (stdlib, third-party, local)

### Code Formatting

We use `black` for automatic formatting:

```bash
black model/ backend/ --line-length 100
```

### Type Hints

Use type hints for function arguments and return values:

```python
def predict_incident_probability(
    temperature: float,
    rain_intensity: float,
    streetname: str
) -> float:
    """Predict incident probability given conditions."""
    pass
```

### Docstrings

Follow Google-style docstrings:

```python
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess raw incident data for model training.
    
    This function performs data cleaning, feature engineering,
    and normalization on the input DataFrame.
    
    Args:
        df: Raw incident data with required columns
        
    Returns:
        Preprocessed DataFrame ready for model training
        
    Raises:
        ValueError: If required columns are missing
        
    Example:
        >>> df = load_data()
        >>> clean_df = preprocess_data(df)
    """
    pass
```

### Naming Conventions

- **Variables/Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`

```python
# Good
def calculate_risk_score(temperature: float) -> float:
    MAX_TEMPERATURE = 40.0
    return temperature / MAX_TEMPERATURE

class RoadEventPredictor:
    def _load_model(self):
        pass
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest model/tests/test_preprocessing.py

# Run with coverage
pytest --cov=model --cov-report=html
```

### Writing Tests

We use `pytest` for testing. Place tests in the appropriate `tests/` directory:

```python
# model/tests/test_preprocessing.py

import pytest
import pandas as pd
from model.preprocessing import remove_outliers

def test_remove_outliers():
    """Test outlier removal function."""
    df = pd.DataFrame({
        'accident_prob': [10, 50, 150, 90, 200]
    })
    
    result = remove_outliers(df)
    
    assert len(result) == 3
    assert result['accident_prob'].max() <= 100
    assert result['accident_prob'].min() >= 0

def test_remove_outliers_empty():
    """Test with empty DataFrame."""
    df = pd.DataFrame({'accident_prob': []})
    
    result = remove_outliers(df)
    
    assert len(result) == 0
```

### Test Coverage

Aim for:
- **Unit tests**: >80% coverage for core functionality
- **Integration tests**: Key workflows (ETL, prediction pipeline)
- **API tests**: All endpoints

## Documentation

### Code Documentation

- **All functions**: Should have docstrings
- **Complex logic**: Add inline comments explaining "why", not "what"
- **Type hints**: Required for public API functions

### Project Documentation

When adding features, update:
- `README.md`: User-facing features and usage
- `docs/methodology.md`: Technical implementation details
- `docs/api_documentation.md`: New API endpoints
- `docs/model_card.md`: Model changes or new models

### Jupyter Notebooks

For exploratory analysis:
- Clear cell outputs before committing
- Add markdown cells explaining each section
- Place in `model/EDA/` or `model/Notebooks/`

## Pull Request Process

### Before Submitting

Ensure your PR:
- [ ] Passes all tests (`pytest`)
- [ ] Has no linting errors (`flake8 model/`)
- [ ] Includes tests for new functionality
- [ ] Updates relevant documentation
- [ ] Has a clear, descriptive title
- [ ] References related issue(s)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How was this tested?

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Follows coding standards

## Related Issues
Closes #123
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and linters
2. **Code Review**: At least one team member reviews
3. **Discussion**: Address reviewer comments
4. **Approval**: Reviewer approves changes
5. **Merge**: Maintainer merges to `develop`

### After Merge

- Delete your feature branch
- Update your local repository
- Close related issues

## Areas for Contribution

We welcome contributions in these areas:

### High Priority
- [ ] Add uncertainty quantification to predictions
- [ ] Implement SHAP-based model explanations
- [ ] Add real-time traffic data integration
- [ ] Create Docker deployment configuration
- [ ] Expand test coverage to >80%

### Medium Priority
- [ ] Add API authentication and rate limiting
- [ ] Implement model A/B testing framework
- [ ] Create data quality monitoring dashboard
- [ ] Add support for ensemble predictions
- [ ] Improve frontend visualization

### Documentation
- [ ] Add more usage examples
- [ ] Create video tutorials
- [ ] Write blog posts about methodology
- [ ] Translate documentation to Dutch

### Research
- [ ] Experiment with alternative models (LightGBM, CatBoost)
- [ ] Try temporal models (LSTM, GRU)
- [ ] Investigate graph neural networks for road networks
- [ ] Benchmark against baseline models

## Questions?

If you have questions about contributing:
- Open a GitHub issue with the `question` label
- Check existing issues and discussions
- Refer to project documentation in `docs/`

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to the ANWB Road Events Predictor! 🚗🛣️
