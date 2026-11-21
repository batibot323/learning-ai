"""
DragonPay Test MCP Server

Provides tools to interact with DragonPay payment gateway:
- Create payment requests
- Check payment status
"""

import os
import uuid
from pathlib import Path
import httpx
from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer

# Load .env file from the server directory
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Configuration from environment variables
BASE_URL = os.environ.get("DRAGONPAY_BASE_URL", "https://test.dragonpay.ph/Api/collect")
USERNAME = os.environ.get("DRAGONPAY_USERNAME", "")
PASSWORD = os.environ.get("DRAGONPAY_PASSWORD", "")

if not USERNAME or not PASSWORD:
    raise ValueError("DRAGONPAY_USERNAME and DRAGONPAY_PASSWORD required. Create a .env file in dragonpay-test/")

mcp = MCPServer("dragonpay-test")


@mcp.tool()
def create_payment(
    amount: float,
    description: str,
    email: str,
    mobile_no: str = "09179999999",
    currency: str = "PHP",
    proc_id: str = "RCDD"
) -> str:
    """
    Create a new payment request in DragonPay.
    
    Use this when the user wants to create a payment link or initiate a payment.
    Returns the reference number (RefNo) and payment URL.
    
    Args:
        amount: Payment amount (e.g., 100.00)
        description: Description of the payment
        email: Customer email address
        mobile_no: Customer mobile number (default: 09179999999)
        currency: Currency code (default: PHP)
        proc_id: Processor ID / payment channel (default: RCDD)
    
    Common proc_ids: RCDD (card), CEBL (Cebuana), GCR2 (GCash)
    """
    txn_id = str(uuid.uuid4())
    
    url = f"{BASE_URL}/v2/{txn_id}/post"
    payload = {
        "amount": amount,
        "currency": currency,
        "description": description,
        "email": email,
        "mobileNo": mobile_no,
        "procId": proc_id
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(
                url,
                json=payload,
                auth=(USERNAME, PASSWORD),
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return (
                    f"Payment created successfully!\n"
                    f"Reference No: {data.get('RefNo')}\n"
                    f"Status: {data.get('Status')}\n"
                    f"Message: {data.get('Message')}\n"
                    f"Payment URL: {data.get('Url')}\n"
                    f"Transaction ID: {txn_id}"
                )
            else:
                return f"Error: HTTP {response.status_code} - {response.text}"
                
    except Exception as e:
        return f"Error creating payment: {str(e)}"


@mcp.tool()
def check_payment_status(ref_no: str) -> str:
    """
    Check the status of a payment request.
    
    Use this when the user wants to know if a payment has been completed,
    is pending, or has failed.
    
    Args:
        ref_no: The reference number returned from create_payment (e.g., BPGVX4Y7QUK8)
    """
    url = f"{BASE_URL}/v1/refno/{ref_no}"
    
    try:
        with httpx.Client() as client:
            response = client.get(
                url,
                auth=(USERNAME, PASSWORD),
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                # Format the response nicely
                status_map = {
                    "S": "Success",
                    "P": "Pending",
                    "F": "Failed",
                    "U": "Unknown",
                    "R": "Refunded",
                    "K": "Chargeback",
                    "V": "Void",
                    "A": "Authorized"
                }
                
                status_code = data.get("Status", "U")
                status_text = status_map.get(status_code, status_code)
                
                return (
                    f"Payment Status for {ref_no}:\n"
                    f"Status: {status_text} ({status_code})\n"
                    f"Amount: {data.get('Amount', 'N/A')} {data.get('Currency', '')}\n"
                    f"Description: {data.get('Description', 'N/A')}\n"
                    f"Email: {data.get('Email', 'N/A')}\n"
                    f"Processor: {data.get('ProcId', 'N/A')}"
                )
            else:
                return f"Error: HTTP {response.status_code} - {response.text}"
                
    except Exception as e:
        return f"Error checking payment status: {str(e)}"


if __name__ == "__main__":
    mcp.run()
