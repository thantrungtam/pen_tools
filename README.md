# Cipher Tools - Django Web Application

A Django website for encoding, decoding, and transforming text using various cipher algorithms and encoding methods. The application features a clean, responsive interface built with Bootstrap and custom SCSS.

## Features

- Multiple encoding and decoding tools:
  - URL Encoder/Decoder
  - Base64 Encoder/Decoder
  - MD5 Hash Generator
  - HTML Encoder/Decoder
  - Caesar Cipher
- Clean, responsive user interface
- Client-side processing for security and privacy
- Easy-to-use tabbed interface for encoding/decoding
- Copy-to-clipboard functionality

## Requirements

- Python 3.8+
- Django 4.0+
- Other dependencies in requirements.txt

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd cipher_tools
```

2. Create a virtual environment and activate it:
```
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install requirements:
```
pip install -r requirements.txt
```

4. Run migrations:
```
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```
python manage.py createsuperuser
```

6. Start the development server:
```
python manage.py runserver
```

7. Visit http://127.0.0.1:8000/admin/ to add tools to the database

## Adding Tools

Tools can be added through the Django admin interface. Each tool requires:

- Name: The name of the cipher/encoding tool
- Slug: A URL-friendly version of the name (auto-generated)
- Description: A brief description of the tool
- Tool Type: Whether the tool is for encoding, decoding, or both

## Extending

To add new cipher or encoding methods:

1. Add a new method to the `CipherHandler` class in `tools/views.py`
2. Update the `process_text` view to handle the new tool type
3. Add the tool to the database through the admin interface

## License

MIT License 