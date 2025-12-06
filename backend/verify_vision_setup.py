#!/usr/bin/env python3
"""
Vision AI Setup Verification Script
This script tests if Google Vision AI is properly configured
"""

import os
import sys
from pathlib import Path


# Colors for terminal output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    END = "\033[0m"


def print_header(text):
    print(f"\n{Colors.CYAN}{'=' * 60}{Colors.END}")
    print(f"{Colors.CYAN}{text.center(60)}{Colors.END}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.END}\n")


def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def check_env_file():
    """Check if .env file exists"""
    print_header("Step 1: Checking .env File")

    env_path = Path(__file__).parent / ".env"

    if env_path.exists():
        print_success(f".env file found at {env_path}")
        return True
    else:
        print_error(f".env file not found at {env_path}")
        print_info("Create .env file with: GOOGLE_API_KEY=your_key_here")
        return False


def check_env_variables():
    """Check if required environment variables are set"""
    print_header("Step 2: Checking Environment Variables")

    from dotenv import load_dotenv

    load_dotenv()

    required_vars = {
        "GOOGLE_API_KEY": "Google Vision API Key",
        "ENABLE_OCR_FEATURE": "OCR Feature Toggle",
    }

    found_all = True
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask the actual key for security
            if var == "GOOGLE_API_KEY":
                masked = (
                    f"{value[:10]}...{value[-5:]}"
                    if len(value) > 15
                    else "*" * len(value)
                )
                print_success(f"{var} = {masked}")
            else:
                print_success(f"{var} = {value}")
        else:
            print_error(f"{var} not set")
            found_all = False

    return found_all


def check_dependencies():
    """Check if required Python packages are installed"""
    print_header("Step 3: Checking Python Dependencies")

    required_packages = {
        "google.generativeai": "google-generativeai",
        "PIL": "Pillow",
        "flask": "Flask",
        "flask_sqlalchemy": "Flask-SQLAlchemy",
    }

    all_installed = True
    for module, package_name in required_packages.items():
        try:
            __import__(module)
            print_success(f"{package_name} is installed")
        except ImportError:
            print_error(f"{package_name} is NOT installed")
            print_info(f"  Install with: pip install {package_name}")
            all_installed = False

    return all_installed


def check_google_api_connection():
    """Test connection to Google Generative AI API"""
    print_header("Step 4: Testing Google API Connection")

    from dotenv import load_dotenv

    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print_error("GOOGLE_API_KEY not found in environment")
        return False

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)

        # Try to access the model
        _ = genai.GenerativeModel("gemini-2.5-flash")
        print_success("✨ Connected to Google Generative AI API!")
        print_success("✨ Model: Gemini 2.5 Flash")
        return True

    except Exception as e:
        print_error(f"Failed to connect to API: {str(e)}")
        print_info("Check that:")
        print_info("  1. API Key is correct")
        print_info("  2. Generative Language API is enabled in Google Cloud")
        print_info("  3. Internet connection is working")
        return False


def check_database():
    """Check if database has OCR columns"""
    print_header("Step 5: Checking Database Schema")

    try:
        from config import FLASK_CONFIG
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from sqlalchemy import inspect

        app = Flask(__name__)
        app.config.update(FLASK_CONFIG)
        db = SQLAlchemy(app)

        with app.app_context():
            inspector = inspect(db.engine)
            columns = [col["name"] for col in inspector.get_columns("users")]

            if "ocr_enabled" in columns and "image_urls" in columns:
                print_success("OCR column 'ocr_enabled' exists in users table")
                print_success("Column 'image_urls' exists in users table")
                return True
            else:
                if "ocr_enabled" not in columns:
                    print_error("OCR column 'ocr_enabled' NOT found in users table")
                if "image_urls" not in columns:
                    print_error("Column 'image_urls' NOT found in users table")
                print_info("Run migration: python migrate_add_ocr.py")
                return False

    except Exception as e:
        print_error(f"Database check failed: {str(e)}")
        return False


def check_config():
    """Check if config.py is correctly updated"""
    print_header("Step 6: Checking Configuration Module")

    try:
        from config import ENABLE_OCR_FEATURE, GOOGLE_VISION_API_KEY

        print_success(f"OCR Feature Enabled: {ENABLE_OCR_FEATURE}")

        if GOOGLE_VISION_API_KEY:
            masked = f"{GOOGLE_VISION_API_KEY[:10]}...{GOOGLE_VISION_API_KEY[-5:]}"
            print_success(f"Google Vision API Key: {masked}")
        else:
            print_error("GOOGLE_VISION_API_KEY not configured")
            return False

        return True

    except Exception as e:
        print_error(f"Config check failed: {str(e)}")
        return False


def run_full_test():
    """Run a full end-to-end test"""
    print_header("Step 7: Running Full End-to-End Test")

    try:
        import google.generativeai as genai
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            print_error("API key not found")
            return False

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")

        print_info("Sending test message to Gemini...")
        response = model.generate_content(
            "Say 'Vision AI Setup Successful!' in exactly this format"
        )

        print_success("✨ API Response Received!")
        print_info(f"Response: {response.text}")
        return True

    except Exception as e:
        print_error(f"End-to-end test failed: {str(e)}")
        print_info("This is usually due to API key or network issues")
        return False


def main():
    """Run all verification checks"""
    print(f"\n{Colors.CYAN}{'=' * 60}{Colors.END}")
    print(
        f"{Colors.CYAN}{'Google Vision AI Setup Verification'.center(60)}{Colors.END}"
    )
    print(f"{Colors.CYAN}{'=' * 60}{Colors.END}")

    results = {
        "Environment File": check_env_file(),
        "Environment Variables": check_env_variables(),
        "Python Dependencies": check_dependencies(),
        "Google API Connection": check_google_api_connection(),
        "Database Schema": check_database(),
        "Configuration Module": check_config(),
        "End-to-End Test": run_full_test(),
    }

    # Print summary
    print_header("Verification Summary")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for check, result in results.items():
        status = "PASS" if result else "FAIL"
        symbol = "✅" if result else "❌"
        print(f"{symbol} {check}: {status}")

    print(f"\n{Colors.CYAN}Score: {passed}/{total} checks passed{Colors.END}")

    if passed == total:
        print_success("All checks passed! Vision AI is ready to use! 🎉")
        return 0
    else:
        print_warning(f"{total - passed} check(s) failed. Review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
