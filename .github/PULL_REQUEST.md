# Add New Relic Monitoring Support

This PR adds New Relic monitoring integration to help track application performance and identify potential issues.

## Changes Made

- Added New Relic Python agent to requirements.txt
- Created newrelic.ini configuration file with standard monitoring settings
- Integrated New Relic agent initialization in the FastAPI application
- Updated deployment configuration to support New Relic license key
- Added documentation in README.md about New Relic setup and usage

## Implementation Details

1. **New Relic Agent Integration**
   - Added newrelic package to requirements.txt
   - Initialized New Relic agent before FastAPI app startup
   - Wrapped FastAPI application with New Relic WSGI wrapper

2. **Configuration**
   - Added newrelic.ini with standard monitoring settings including:
     - Transaction tracing
     - SQL monitoring (with obfuscation)
     - Distributed tracing
     - Thread profiling

3. **Deployment Updates**
   - Modified deploy.yml to pass NEW_RELIC_LICENSE_KEY from environment
   - Made New Relic integration optional (only activates if license key is present)

## How to Use

1. Set the `NEW_RELIC_LICENSE_KEY` environment variable with your New Relic license key
2. The monitoring will automatically start when the application runs
3. View metrics and performance data in your New Relic dashboard

## Testing

The changes are non-invasive and won't affect application functionality:
- Application works normally without New Relic key set
- When key is set, monitoring activates without affecting app behavior
- No changes to existing endpoints or business logic
