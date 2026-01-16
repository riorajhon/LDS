import requests
from datetime import datetime
import bittensor
import argparse

# Edit these variables directly in the file
latitude = 43.7291884  # Optional: set to float value (e.g., 4.5) or leave as None
longitude = 7.4172013  # Optional: set to float value (e.g., 31.6) or leave as None
wallet_name = "riora_coldkey"  # Your wallet name
wallet_hotkey = "default"  # Your hotkey name
api_url = "http://34.211.230.92:5000/validate"  # API endpoint URL


def sign_message(wallet: bittensor.Wallet, message_text: str = "API Request") -> str:
    """
    Signs a message using the specified wallet.

    Args:
        wallet (bittensor.Wallet): The wallet object to use for signing.
        message_text (str): The message you want to sign.

    Returns:
        str: The combined signature contents (message + signature info).
    """
    # Use the wallet's hotkey for signing
    keypair = wallet.hotkey

    # Generate a timestamped message
    timestamp = datetime.now()
    timezone_name = timestamp.astimezone().tzname()
    signed_message = f"<Bytes>On {timestamp} {timezone_name} {message_text}</Bytes>"

    # Sign the message
    signature = keypair.sign(data=signed_message)

    # Construct the output in the expected format
    signature_text = (
        f"{signed_message}\n"
        f"\tSigned by: {keypair.ss58_address}\n"
        f"\tSignature: {signature.hex()}"
    )

    return signature_text


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Call LDS API with miner address')
    parser.add_argument('--miner_address', type=str, required=True, help='Miner address (e.g., "123 main street, Ukraine")')
    args = parser.parse_args()
    
    # Load wallet
    wallet = bittensor.Wallet(name=wallet_name, hotkey=wallet_hotkey)
    
    # Sign message
    signature = sign_message(wallet)
    
    # Prepare payload
    payload = {
        'miner_address': args.miner_address,
        'signature': signature
    }
    
    # Add optional coordinates
    if latitude is not None:
        payload['latitude'] = latitude
    if longitude is not None:
        payload['longitude'] = longitude
    
    # Send request
    print(f"\nSending request to API...")
    print(f"Miner Address: {args.miner_address}")
    
    response = requests.post(api_url, json=payload)
    
    print(f"\n{'='*50}")
    print("API Response:")
    print(f"{'='*50}")
    
    response_data = response.json()
    for key, value in response_data.items():
        print(f"{key}: {value}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()

