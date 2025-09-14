# Browser Project

A lightweight web browser implementation written in Python using Tkinter for the GUI. This project follows the educational approach from the book [Web Browser Engineering](https://browser.engineering/) by Pavel Panchekha and Chris Harrelson, demonstrating the core concepts of web browsing including HTML parsing, layout rendering, and HTTP communication.

> **Note**: This is a work in progress! I'm still working through the book and implementing features as I learn. Not all browser functionality is complete yet.

## Features

- **HTML Parsing**: Custom HTML parser that builds a DOM tree from HTML content
- **CSS Parsing**: Parses basic CSS rules and selectors (class, tag, descendant)
- **Block Layout Engine**: Supports block-level layout, text rendering, and basic box model
- **Selectors**: Tag and descendant selectors for applying CSS rules
- **Drawing Primitives**: Renders rectangles and text using a display list
- **HTTP/HTTPS Support**: Full support for HTTP and HTTPS protocols with SSL/TLS
- **Caching System**: Built-in browser cache with cache-control header support
- **Scrolling**: Mouse wheel and keyboard scrolling support
- **View Source**: Special `view-source:` protocol for viewing page source
- **File Protocol**: Support for local HTML files
- **Data URLs**: Basic support for data: URLs
- **Responsive**: Window resizing support with automatic re-layout

## Project Structure

browser/

```
browser/
├── browser.py          # Main browser class and GUI
├── URL.py              # URL handling and HTTP requests
├── HTMLParser.py       # HTML parsing and DOM tree construction
├── CSSParser.py        # CSS parsing and rule extraction
├── BlockLayout.py      # Block-level layout engine
├── DocumentLayout.py   # Document-level layout and painting
├── DrawRect.py         # Rectangle drawing primitive
├── DrawText.py         # Text drawing primitive
├── TagSelector.py      # CSS selector logic
├── Element.py          # HTML element representation
├── Text.py             # Text node representation
├── BrowserCache.py     # Caching system implementation
├── scrollbar.py        # Scrollbar widget
├── test.html           # Sample HTML file for testing
└── testing/            # Test files directory
```

## Requirements

- Python 3.10+
- tkinter (usually included with Python)
- ssl (included with Python)
- socket (included with Python)

## Installation

1. Clone or download this repository
2. Ensure you have Python 3.10+ installed
3. No additional dependencies needed - uses Python standard library

## Usage

### Basic Usage

Run the browser with a default test page:
```bash
python browser.py
```

### Load a Specific URL

```bash
python browser.py https://example.com
```

### Specify HTTP Version and User Agent

```bash
python browser.py https://example.com 1.1 Chrome
```

### View Page Source

```bash
python browser.py view-source:https://example.com
```

### Load Local Files

```bash
python browser.py file://path/to/your/file.html
```

## Controls

- **Mouse Wheel**: Scroll up/down
- **Up Arrow**: Scroll up
- **Down Arrow**: Scroll down
- **Window Resize**: Automatically re-layouts content

## Supported Protocols

- `http://` - HTTP requests
- `https://` - HTTPS requests with SSL/TLS
- `file://` - Local file access
- `data:` - Data URLs (basic support)
- `view-source:` - View page source

## Architecture

### Core Components

1. **Browser Class** (`browser.py`)
   - Main application window and GUI
   - Event handling (scrolling, resizing)
   - Rendering pipeline coordination

2. **URL Handler** (`URL.py`)
   - HTTP/HTTPS request handling
   - SSL/TLS support
   - Redirect following
   - Gzip decompression

3. **HTML Parser** (`HTMLParser.py`)
   - Tokenizes HTML content
   - Builds DOM tree structure
   - Handles self-closing and head tags

4. **CSS Parser** (`CSSParser.py`)
   - Parses CSS rules and selectors
   - Supports tag, class, and descendant selectors

5. **Block Layout Engine** (`BlockLayout.py`, `DocumentLayout.py`)
   - Block-level layout and box model
   - Text positioning, wrapping, and font management
   - Display list generation for painting

6. **Drawing Primitives** (`DrawRect.py`, `DrawText.py`)
   - Renders rectangles and text to the screen

7. **Selectors** (`TagSelector.py`)
   - Implements tag and descendant selector logic for CSS

8. **Cache System** (`BrowserCache.py`)
   - Singleton cache implementation
   - Cache-Control header support
   - TTL-based expiration

## Features in Detail

### HTML Support
- Basic HTML tag parsing
- Attribute handling
- Text content rendering
- Self-closing tag support
- Head tag filtering

### HTTP Features
- HTTP/1.1 support
- HTTPS with SSL verification
- Gzip compression
- Cache-Control headers
- Redirect following (with loop protection)
- Custom User-Agent strings


### CSS & Rendering
- Block-level layout (no inline or flex/grid yet)
- Basic CSS parsing and application (tag, descendant selectors)
- Font size, weight, and style support
- Rectangle and text drawing
- Line wrapping
- Scrollable content
- Responsive layout on window resize

## Limitations

- No image, video, or JavaScript support
- CSS support is basic: only block-level, no inline/flex/grid, limited selectors
- No form handling
- No link clicking functionality
- No advanced layout (floats, positioning, etc.)


## Development

This browser is implemented following the educational approach from [Web Browser Engineering](https://browser.engineering/), serving as a learning project that demonstrates:
- HTTP protocol implementation
- HTML parsing techniques
- CSS parsing and selector logic
- Block-level layout and rendering
- GUI programming with Tkinter
- Caching strategies
- Text layout algorithms

The implementation closely follows the book's progressive approach to building a web browser from scratch.

## Testing

Use the included `test.html` file or create your own HTML files in the `testing/` directory to test browser functionality.

## License

No license specified - educational project.
