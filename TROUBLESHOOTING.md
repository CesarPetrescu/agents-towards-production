# Troubleshooting Guide

## Overview
This guide provides solutions to common issues encountered when working with the "Agents Towards Production" tutorials.

## Common Issues

### Environment Setup

#### Issue: Dependency conflicts
**Symptoms**: 
- Import errors after installing requirements
- Package version incompatibilities
- "Could not find a version that satisfies the requirement" errors

**Solutions**:
1. Use virtual environments for each tutorial:
   ```bash
   python -m venv tutorial_env
   source tutorial_env/bin/activate  # On Windows: tutorial_env\Scripts\activate
   pip install -r requirements.txt
   ```

2. Check for conflicts using the dependency checking script:
   ```bash
   python scripts/check_dependencies.py
   ```

3. Use conda environments for better dependency management:
   ```bash
   conda create -n tutorial_name python=3.9
   conda activate tutorial_name
   pip install -r requirements.txt
   ```

#### Issue: Python version incompatibility
**Symptoms**:
- Syntax errors in dependencies
- "SyntaxError: invalid syntax" for newer Python features
- Type hint errors

**Solutions**:
1. Check the tutorial's required Python version in requirements.txt or README
2. Use pyenv to manage Python versions:
   ```bash
   pyenv install 3.9.16
   pyenv local 3.9.16
   ```
3. Create environment with specific Python version:
   ```bash
   python3.9 -m venv env_name
   ```

### Docker Issues

#### Issue: Docker container won't build
**Symptoms**:
- "Step X: failed" messages during build
- Dependency installation failures
- Permission errors

**Solutions**:
1. Check Dockerfile syntax and base image availability
2. Clear Docker cache:
   ```bash
   docker system prune -a
   ```
3. Build with more memory allocated (in Docker settings)
4. Use multi-stage builds to reduce image size and build time

#### Issue: Container won't start
**Symptoms**:
- Container exits immediately after starting
- Port binding errors
- Missing environment variables

**Solutions**:
1. Check container logs:
   ```bash
   docker logs container_name
   ```
2. Verify environment variables are set:
   ```bash
   docker run -e VAR_NAME=value image_name
   ```
3. Check port availability:
   ```bash
   docker run -p 8000:8000 image_name
   ```

### API Integration

#### Issue: API keys not working
**Symptoms**:
- Authentication errors
- "Invalid API key" messages
- Rate limit exceeded errors

**Solutions**:
1. Verify API key is correctly set in environment variables:
   ```bash
   echo $API_KEY
   ```
2. Check for trailing spaces or special characters in the key
3. Verify the API key has the correct permissions
4. Check rate limits and wait if exceeded
5. Use a .env file for secure key storage:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

#### Issue: Network/timeout errors
**Symptoms**:
- Connection timeout errors
- "Failed to establish connection" messages
- Slow response times

**Solutions**:
1. Check internet connectivity
2. Increase timeout values in API calls
3. Add retry logic with exponential backoff
4. Use a VPN if region-restricted APIs are required

### Jupyter Notebook Issues

#### Issue: Kernel not starting
**Symptoms**:
- "Kernel error" message
- Notebook won't execute cells
- "No module named 'module_name'" errors

**Solutions**:
1. Install IPython kernel for your environment:
   ```bash
   python -m ipykernel install --user --name=env_name
   ```
2. Select the correct kernel in Jupyter (Kernel → Change kernel)
3. Restart Jupyter server after installing new packages

#### Issue: Memory issues with large datasets
**Symptoms**:
- "MemoryError" exceptions
- Notebook becomes unresponsive
- Slow execution times

**Solutions**:
1. Process data in chunks rather than loading everything at once
2. Use generators instead of lists for large datasets
3. Clear variables that are no longer needed:
   ```python
   import gc
   del large_variable
   gc.collect()
   ```
4. Close other applications to free up memory

### Agent-Specific Issues

#### Issue: Agent loops or infinite execution
**Symptoms**:
- Agent runs indefinitely
- High CPU/memory usage
- No response or completion

**Solutions**:
1. Add proper termination conditions
2. Implement step limits:
   ```python
   max_steps = 10
   current_steps = 0
   while not done and current_steps < max_steps:
       # agent logic
       current_steps += 1
   ```
3. Add timeout mechanisms
4. Debug the decision-making logic

#### Issue: Poor agent performance
**Symptoms**:
- Incorrect responses
- Slow decision-making
- Inconsistent behavior

**Solutions**:
1. Review prompt engineering
2. Check LLM model selection and parameters
3. Add better context or examples
4. Implement proper error handling and fallbacks

## Performance Optimization

### Memory Management
- Use generators for large datasets
- Process data in batches
- Clear unused variables with `del`
- Use `gc.collect()` to force garbage collection

### Caching
- Implement result caching for expensive operations
- Use Redis or in-memory caching for repeated queries
- Cache API responses when appropriate

### Parallel Processing
- Use asyncio for I/O-bound operations
- Implement multiprocessing for CPU-bound tasks
- Use thread pools for concurrent API calls

## Security Best Practices

### Credential Management
- Never hardcode API keys
- Use environment variables or secure vaults
- Implement proper key rotation
- Use .gitignore to prevent credential commits

### Input Validation
- Validate all user inputs
- Sanitize inputs before processing
- Implement rate limiting
- Use parameterized queries to prevent injection

## Debugging Strategies

### Logging
- Implement comprehensive logging
- Use different log levels (DEBUG, INFO, WARNING, ERROR)
- Log important state changes and decisions
- Structure logs for easy analysis

### Tracing
- Use LangSmith or similar tools for agent tracing
- Log intermediate steps and decisions
- Track token usage and costs
- Monitor response times

### Error Handling
- Implement graceful error handling
- Provide meaningful error messages
- Log errors with context
- Implement retry mechanisms where appropriate

## Common Error Messages and Solutions

### "No module named..."
- Solution: Activate the correct virtual environment and install requirements

### "Port already in use"
- Solution: Use a different port or stop the process using the port

### "SSL certificate verify failed"
- Solution: Update certificates or set appropriate SSL context

### "Permission denied"
- Solution: Check file permissions and run with appropriate privileges

## Getting Help

If you encounter an issue not covered in this guide:

1. Check the specific tutorial's README for troubleshooting tips
2. Search the repository issues for similar problems
3. Verify your environment matches the tutorial requirements
4. Create a minimal reproduction case
5. Consider opening an issue in the repository with detailed information

## Prevention Tips

- Always use virtual environments for tutorials
- Keep dependencies updated but pinned to specific versions
- Test code in small increments
- Use version control to track changes
- Document your environment setup
- Regularly backup important work