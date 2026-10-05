import time
import json
import base64
import hashlib
import hmac

SECRET_KEY = "ntro-social-lens-secret-key-production"
AUDIT_LOG_FILE = "backend/audit.log"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Mock users database
USERS_DB = {
    "admin": {
        "username": "admin",
        "password_hash": hash_password("admin123"),
        "role": "admin",
        "name": "System Administrator"
    },
    "analyst": {
        "username": "analyst",
        "password_hash": hash_password("analyst123"),
        "role": "analyst",
        "name": "NTRO Senior Analyst"
    },
    "viewer": {
        "username": "viewer",
        "password_hash": hash_password("viewer123"),
        "role": "viewer",
        "name": "Observer Account"
    }
}

def create_jwt_token(username: str, role: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": username,
        "role": role,
        "exp": int(time.time()) + 86400, # 24 hrs
        "iat": int(time.time())
    }
    
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().strip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().strip("=")
    
    signature_input = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(SECRET_KEY.encode(), signature_input, hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().strip("=")
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def verify_jwt_token(token: str) -> dict:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        
        header_b64, payload_b64, signature_b64 = parts
        
        # Pad base64 strings if needed
        def pad_b64(b64_str):
            return b64_str + "=" * (-len(b64_str) % 4)
            
        signature_input = f"{header_b64}.{payload_b64}".encode()
        expected_sig = hmac.new(SECRET_KEY.encode(), signature_input, hashlib.sha256).digest()
        actual_sig = base64.urlsafe_b64decode(pad_b64(signature_b64))
        
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None
            
        payload_bytes = base64.urlsafe_b64decode(pad_b64(payload_b64))
        payload = json.loads(payload_bytes.decode())
        
        if payload.get("exp", 0) < time.time():
            return None
            
        return payload
    except Exception:
        return None

def log_audit(username: str, action: str, details: str):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    log_entry = f"[{timestamp}] USER={username} ACTION={action} DETAILS={details}\n"
    try:
        with open(AUDIT_LOG_FILE, "a") as f:
            f.write(log_entry)
    except Exception:
        pass
