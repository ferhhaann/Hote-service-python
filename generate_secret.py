#!/usr/bin/env python3
"""Generate a new SECRET_KEY for production use."""
import secrets

if __name__ == "__main__":
    secret_key = secrets.token_hex(32)
    print("\n" + "="*60)
    print("NEW SECRET_KEY FOR PRODUCTION:")
    print("="*60)
    print(f"\n{secret_key}\n")
    print("="*60)
    print("\nCopy this key to your production .env file on EC2")
    print("Never use the same SECRET_KEY for dev and production!")
    print("="*60 + "\n")
