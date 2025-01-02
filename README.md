# Baby Name Thunderdome

A collaborative baby name selection platform that helps parents choose the perfect name through a fun and interactive voting system. Visit our live site at [https://babynamethunderdome.com/](https://babynamethunderdome.com/)

## Features

- **For Parents**:
  - Create and manage lists of potential baby names
  - Invite friends and family to participate in name selection
  - View voting results and rankings
  - Simple link sharing - no complex authentication needed

- **For Friends & Family**:
  - Easy-to-use voting interface
  - Compare names in head-to-head matchups
  - No accounts required - just use the shared link
  - Share feedback on name choices

## Quick Start

1. **Installation**
   ```bash
   # Clone the repository
   git clone https://github.com/posix4e/babynamethunderdome.git
   cd babynamethunderdome

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Running Locally**
   ```bash
   python app/main.py
   ```
   The application will be available at http://localhost:5000

## Development

- **Running Tests**
  ```bash
  python -m pytest tests/
  ```

- **Project Structure**
  - `app/main.py` - Main application code
  - `app/static/` - Static assets (CSS, JS)
  - `app/templates/` - HTML templates
  - `tests/` - Test suite
  - `requirements.txt` - Python dependencies
  - `*.yml/.j2` - Deployment and configuration files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the tests
5. Submit a pull request

## License

This project is open source and available under the MIT License.
