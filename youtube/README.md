<div style="display: flex; justify-content: center; align-items: center;">
  <img
    src="https://docs.arcade.dev/images/logo/arcade-logo.png"
    style="width: 250px;"
  >
</div>

<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 8px;">
  <img src="https://img.shields.io/github/v/release/regiscamimura/youtube" alt="GitHub release" style="margin: 0 2px;">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python version" style="margin: 0 2px;">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" style="margin: 0 2px;">
  <img src="https://img.shields.io/pypi/v/arcade_youtube" alt="PyPI version" style="margin: 0 2px;">
</div>
<div style="display: flex; justify-content: center; align-items: center;">
  <a href="https://github.com/regiscamimura/youtube" target="_blank">
    <img src="https://img.shields.io/github/stars/regiscamimura/youtube" alt="GitHub stars" style="margin: 0 2px;">
  </a>
  <a href="https://github.com/regiscamimura/youtube/fork" target="_blank">
    <img src="https://img.shields.io/github/forks/regiscamimura/youtube" alt="GitHub forks" style="margin: 0 2px;">
  </a>
</div>

<br>
<br>

# Arcade YouTube Toolkit 🎮

Ever wondered what your kids are watching on YouTube? Well, now you can find out! This toolkit helps you keep an eye on YouTube activity without being too creepy about it. It's like having a friendly neighborhood watch, but for YouTube.

## Project Structure

This repository contains two main components:

1. **[arcade_youtube/](arcade_youtube/README.md)** - The core toolkit that provides YouTube data collection and analysis capabilities
2. **[app/](app/README.md)** - A sample application demonstrating how to use the toolkit to create a parental monitoring dashboard

Each component has its own README with detailed information:
- [arcade_youtube/README.md](arcade_youtube/README.md) - Toolkit documentation and API reference
- [app/README.md](app/README.md) - Sample application setup and usage guide

## Installation

Since this is still in development (and not yet part of the Arcade tools), you'll need to install it from source:

```bash
# Clone the repository
git clone https://github.com/regiscamimura/youtube.git
cd youtube

# Install dependencies using Poetry
poetry install
```

> 💡 **Note**: This will be available via `pip install arcade_youtube` once it's integrated into the Arcade tools. For now, you'll need to use Poetry to manage the dependencies.

## Setting Up Your Environment Variables 🔑

Before you can start spying on YouTube activity (in a totally non-creepy way), you'll need to set up your Google API credentials. Here's how:

1. **Create a Google Cloud Project** 🏗️
   - Go to [console.cloud.google.com](https://console.cloud.google.com)
   - Create a new project (or use an existing one)
   - Enable the YouTube Data API v3 for your project

2. **Get Your Credentials** 🎫
   - In the Google Cloud Console, go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client ID"
   - Choose "Desktop app" as the application type
   - Download the JSON credentials file (keep this safe, like your secret cookie recipe)

3. **Generate Your Tokens** 🎟️
   - Put your downloaded credentials JSON file in the project root
   - Run the token generator script:
   ```bash
   python get_tokens.py
   ```
   - Follow the prompts to authenticate (you'll need to open a browser and log in)
   - The script will create a `.env` file with all the necessary tokens

4. **Your `.env` File Should Look Like This** 📝
   ```env
   YOUTUBE_CLIENT_ID=your_client_id_here
   YOUTUBE_CLIENT_SECRET=your_client_secret_here
   YOUTUBE_REFRESH_TOKEN=your_refresh_token_here
   ```

> 💡 **Pro Tip**: Never commit your `.env` file to version control! It's already in the `.gitignore` file, but you know, just saying...

## Testing

The test suite uses `vcrpy` to record and replay HTTP interactions. This approach offers several advantages:

- Tests use real API responses, ensuring accurate representation of API behavior
- Cassettes store complete request/response cycles for inspection
- Tests are deterministic and reliable
- No need for complex mocking of HTTP interactions

### vcrpy vs pytest-mock

While pytest-mock is a popular choice, we strongly prefer vcrpy for this project. Here's why:

**Why I advocate for vcrpy:**
- Real API responses ensure tests match production behavior exactly
- Cassettes serve as living documentation of API interactions
- No risk of unrealistic mock data that doesn't match the real API
- API changes are caught automatically, making tests more reliable
- You can inspect the actual request/response cycles to debug issues
- Minimal setup required - no need to create the mocks, just configure vcrpy once and you're good to go
- No false positives. Requests will fail if they fail.

**The pytest-mock approach has drawbacks:**
- Mock data might not reflect real API behavior
- Developers might make assumptions about API responses
- Tests could pass with incorrect mock data
- More maintenance overhead when API changes
- Harder to debug issues without real API context

Yes, the cassettes are larger than mock files, but they contain real data that you can trust. In our experience, the benefits of using real API responses far outweigh the storage overhead.

To run the tests:
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v
```

> Note: If you need to update the cassettes (e.g., API response format changed), delete the old ones and run the tests again. vcrpy will record new interactions.

## License

MIT License - because we're nice like that. See the [LICENSE](LICENSE) file for the boring details.