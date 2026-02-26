#!/usr/bin/env python3
"""
Auth Config Generator
Generate OAuth and authentication configurations for various platforms.
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class ConfigGenerator:
    """Base class for config generators."""
    
    def __init__(self, output_dir: str = "."):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
    
    def write_file(self, filename: str, content: str) -> Path:
        """Write content to file."""
        filepath = self.output_dir / filename
        filepath.write_text(content)
        return filepath


class SupabaseConfigGenerator(ConfigGenerator):
    """Generate Supabase authentication configuration."""
    
    def __init__(
        self,
        project_id: str,
        api_key: str,
        jwt_secret: str,
        service_role_key: Optional[str] = None,
        output_dir: str = "."
    ):
        super().__init__(output_dir)
        self.project_id = project_id
        self.api_key = api_key
        self.jwt_secret = jwt_secret
        self.service_role_key = service_role_key
        self.url = f"https://{project_id}.supabase.co"
    
    def generate_env_file(self, filename: str = "supabase.env") -> Path:
        """Generate .env file for Supabase."""
        content = f"""# Supabase Configuration
# Generated: {datetime.now().isoformat()}

SUPABASE_URL={self.url}
SUPABASE_ANON_KEY={self.api_key}
SUPABASE_JWT_SECRET={self.jwt_secret}"""
        
        if self.service_role_key:
            content += f"\nSUPABASE_SERVICE_ROLE_KEY={self.service_role_key}"
        
        content += """

# Additional Configuration
JWT_EXPIRATION=3600
REDIRECT_URL=http://localhost:3000/auth/callback
"""
        
        return self.write_file(filename, content)
    
    def generate_guide(self, filename: str = "supabase-setup.md") -> Path:
        """Generate setup guide."""
        content = f"""# Supabase Authentication Setup Guide

## Project Details
- **Project ID**: {self.project_id}
- **URL**: {self.url}
- **Generated**: {datetime.now().isoformat()}

## Configuration

### Environment Variables
Set these in your `.env` file:

```env
SUPABASE_URL={self.url}
SUPABASE_ANON_KEY={self.api_key}
```

### Initialize Client

#### JavaScript/TypeScript
```javascript
import {{ createClient }} from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY
)
```

#### Python
```python
from supabase import create_client, Client

url = "{self.url}"
key = "{self.api_key}"
supabase: Client = create_client(url, key)
```

#### Flutter
```dart
import 'package:supabase_flutter/supabase_flutter.dart';

await Supabase.initialize(
  url: '{self.url}',
  anonKey: '{self.api_key}',
);
```

## Authentication Methods

### Email/Password
```javascript
// Sign up
const {{ user, session, error }} = await supabase.auth.signUp({{
  email: 'user@example.com',
  password: 'password123',
}})

// Sign in
const {{ user, session, error }} = await supabase.auth.signInWithPassword({{
  email: 'user@example.com',
  password: 'password123',
}})
```

### OAuth Providers
```javascript
const {{ user, session, error }} = await supabase.auth.signInWithOAuth({{
  provider: 'google', // or 'github', 'apple', etc.
  options: {{
    redirectTo: 'http://localhost:3000/auth/callback',
  }},
}})
```

## Security Best Practices

✓ Use HTTPS in production
✓ Keep JWT secret secure (never commit to repo)
✓ Use Row Level Security (RLS) on tables
✓ Validate JWT tokens on backend
✓ Implement token refresh logic

## Troubleshooting

**Invalid JWT Error**: Ensure JWT_SECRET matches your Supabase project

**Auth failures**: Check that redirect URLs are registered in Supabase dashboard

**Token expiration**: Implement automatic refresh before token expires
"""
        
        return self.write_file(filename, content)


class AppleOAuthGenerator(ConfigGenerator):
    """Generate Apple OAuth configuration."""
    
    def __init__(
        self,
        team_id: str,
        bundle_id: str,
        app_name: str,
        output_dir: str = "."
    ):
        super().__init__(output_dir)
        self.team_id = team_id
        self.bundle_id = bundle_id
        self.app_name = app_name
    
    def generate_entitlements(self, filename: str = "Entitlements.plist") -> Path:
        """Generate Entitlements.plist for Sign in with Apple."""
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.developer.applesignin</key>
    <array>
        <string>Default</string>
    </array>
    <key>keychain-access-groups</key>
    <array>
        <string>${{AppIdentifierPrefix}}{self.bundle_id}</string>
    </array>
</dict>
</plist>"""
        
        return self.write_file(filename, content)
    
    def generate_setup_guide(self, filename: str = "apple-oauth-setup.md") -> Path:
        """Generate Apple OAuth setup guide."""
        content = f"""# Sign in with Apple Setup Guide

## Overview
This guide covers setting up Sign in with Apple for **{self.app_name}**.

- **Team ID**: {self.team_id}
- **Bundle ID**: {self.bundle_id}

## Step 1: Create App ID

1. Go to [Apple Developer Account](https://developer.apple.com/account)
2. Navigate to **Identifiers**
3. Click **+** to create new identifier
4. Select **App IDs**
5. Choose **App**
6. Fill in details:
   - **Description**: {self.app_name}
   - **Bundle ID**: {self.bundle_id}

## Step 2: Enable Sign in with Apple

1. In the App ID configuration, scroll to **Capabilities**
2. Find and enable **Sign in with Apple**
3. Configure:
   - **Primary App ID**: {self.bundle_id}
   - **App Groups**: (leave empty if not using shared keychain)

## Step 3: Configure Entitlements

1. In Xcode, select your target
2. Go to **Signing & Capabilities**
3. Click **+ Capability**
4. Add **Sign in with Apple**
5. Ensure bundle ID matches: {self.bundle_id}

Your **Entitlements.plist** should contain:
```xml
<key>com.apple.developer.applesignin</key>
<array>
    <string>Default</string>
</array>
```

## Step 4: Create Signing Certificate

1. Go to [Certificates, Identifiers & Profiles](https://developer.apple.com/account/resources/certificates)
2. Create new **iOS App Development** certificate
3. Download and install certificate
4. Create matching **Provisioning Profile**

## Step 5: Implement Sign in with Apple

### SwiftUI Example

```swift
import AuthenticationServices

struct SignInView: View {{
    @State private var nonce: String?
    
    var body: some View {{
        SignInWithAppleButton({{ request in
            let nonce = UUID().uuidString
            self.nonce = nonce
            request.requestedScopes = [.email, .fullName]
            request.nonce = nonce
        }}, onCompletion: {{ result in
            switch result {{
            case .success(let authorization):
                handleAuthorization(authorization)
            case .failure(let error):
                print("Sign in failed: \\(error)")
            }}
        }})
        .signInWithAppleButtonStyle(.black)
        .frame(height: 50)
    }}
    
    private func handleAuthorization(_ authorization: ASAuthorization) {{
        guard let credential = authorization.credential as? ASAuthorizationAppleIDCredential else {{
            return
        }}
        
        let userIdentifier = credential.user
        let email = credential.email ?? ""
        let fullName = credential.fullName
        
        // Sign in with backend
        signInWithBackend(
            userIdentifier: userIdentifier,
            identityToken: credential.identityToken,
            nonce: nonce ?? ""
        )
    }}
}}
```

### UIKit Example

```swift
import AuthenticationServices

class SignInViewController: UIViewController {{
    override func viewDidLoad() {{
        super.viewDidLoad()
        setupSignInButton()
    }}
    
    private func setupSignInButton() {{
        let button = ASAuthorizationAppleIDButton()
        button.addTarget(self, action: #selector(signInTapped), for: .touchUpInside)
        view.addSubview(button)
        // Layout constraints...
    }}
    
    @objc private func signInTapped() {{
        let provider = ASAuthorizationAppleIDProvider()
        let request = provider.createRequest()
        request.requestedScopes = [.email, .fullName]
        
        let controller = ASAuthorizationController(authorizationRequests: [request])
        controller.delegate = self
        controller.presentationContextProvider = self
        controller.performRequests()
    }}
}}

extension SignInViewController: ASAuthorizationControllerDelegate {{
    func authorizationController(
        _ controller: ASAuthorizationController,
        didCompleteWithAuthorization authorization: ASAuthorization
    ) {{
        // Handle successful authentication
    }}
}}
```

## Step 6: Handle Credentials

After authentication, you'll receive:
- `userIdentifier` - Unique ID for user
- `email` - User's email (if available)
- `fullName` - User's full name
- `identityToken` - JWT token for backend verification

## Troubleshooting

### Error 1001: Unknown Error
- Check App ID exists and has Sign in with Apple enabled
- Verify bundle ID matches exactly
- Ensure provisioning profile includes Sign in with Apple capability

### Error 1000: Cancelled by User
- This is normal when user cancels sign in
- Handle gracefully in your UI

### Identity Token is nil
- User privacy settings may prevent email sharing
- Request .email and .fullName scopes
- Nonce should be included in request

### Team ID Mismatch
- Verify Team ID matches: {self.team_id}
- Check bundle ID is under correct team in Developer Account

## Security Checklist

✓ Use nonce to prevent replay attacks
✓ Verify identity token on backend
✓ Store user identifier securely (Keychain)
✓ Implement token refresh
✓ Use HTTPS for all API calls
✓ Never expose JWT secret in client code
"""
        
        return self.write_file(filename, content)


class GoogleOAuthGenerator(ConfigGenerator):
    """Generate Google OAuth configuration."""
    
    def __init__(
        self,
        project_id: str,
        client_id: str,
        client_secret: str,
        output_dir: str = "."
    ):
        super().__init__(output_dir)
        self.project_id = project_id
        self.client_id = client_id
        self.client_secret = client_secret
    
    def generate_credentials_json(self, filename: str = "google-oauth.json") -> Path:
        """Generate Google OAuth credentials file."""
        credentials = {
            "type": "oauth2",
            "project_id": self.project_id,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uris": [
                "http://localhost:3000/auth/callback",
                "https://yourdomain.com/auth/callback"
            ],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "generated": datetime.now().isoformat()
        }
        
        content = json.dumps(credentials, indent=2)
        return self.write_file(filename, content)
    
    def generate_setup_guide(self, filename: str = "google-oauth-setup.md") -> Path:
        """Generate Google OAuth setup guide."""
        content = f"""# Google OAuth Setup Guide

## Project Details
- **Project ID**: {self.project_id}
- **Client ID**: {self.client_id}
- **Generated**: {datetime.now().isoformat()}

## Step 1: Create GCP Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project or select existing
3. Project ID: {self.project_id}

## Step 2: Enable Required APIs

1. Search for **Google+ API**
2. Click **Enable**
3. Also enable:
   - **Google Identity Services API**
   - **Google Identity Service API**

## Step 3: Create OAuth Consent Screen

1. Go to **APIs & Services** > **OAuth consent screen**
2. Choose **External** user type
3. Fill in required fields:
   - **App name**: Your app name
   - **User support email**: your-email@example.com
   - **Developer contact**: your-email@example.com
4. Add required scopes:
   - `openid`
   - `email`
   - `profile`

## Step 4: Create OAuth Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth Client ID**
3. Choose application type:
   - **Web application** (for backend)
   - **iOS app** (for mobile)
   - **Android app** (for Android)
4. Configure:
   - **Authorized redirect URIs**: 
     - `http://localhost:3000/auth/callback`
     - `https://yourdomain.com/auth/callback`
5. Download JSON credentials

## Step 5: Configure Scopes

Recommended OAuth scopes:
```
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/userinfo.profile
https://www.googleapis.com/auth/calendar
https://www.googleapis.com/auth/drive
```

## Web Implementation

### Using Google Sign-In Library

```html
<script src="https://accounts.google.com/gsi/client" async defer></script>
```

```javascript
google.accounts.id.initialize({{
  client_id: '{self.client_id}',
  callback: handleCredentialResponse
}});

google.accounts.id.renderButton(
  document.getElementById('signInButton'),
  {{ theme: 'outline', size: 'large' }}
);

function handleCredentialResponse(response) {{
  // Verify JWT token on backend
  fetch('/auth/google', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify({{ credential: response.credential }})
  }})
}}`
```

## Backend Verification

### Python (Flask)

```python
from google.auth.transport import requests
from google.oauth2 import id_token

try:
    idinfo = id_token.verify_oauth2_token(
        token,
        requests.Request(),
        client_id="{self.client_id}"
    )
    user_id = idinfo['sub']
    email = idinfo['email']
except ValueError:
    # Token invalid
    pass
```

### Node.js (Express)

```javascript
const {{OAuth2Client}} = require('google-auth-library');
const client = new OAuth2Client('{self.client_id}');

async function verifyToken(token) {{
  const ticket = await client.verifyIdToken({{
    idToken: token,
    audience: '{self.client_id}',
  }});
  const payload = ticket.getPayload();
  return payload;
}}
```

## Troubleshooting

**"Invalid client_id" error**
- Ensure client_id is from OAuth credentials (not API key)
- Check bundle ID/app name matches GCP configuration

**Redirect URI mismatch**
- Register exact redirect URI in GCP (including protocol)
- Ensure trailing slashes match exactly

**Refresh token not returned**
- Add `access_type=offline` to auth request
- Use `prompt=consent` to force consent screen

**Missing email in response**
- Ensure "email" scope is requested
- Check user's privacy settings allow email sharing
"""
        
        return self.write_file(filename, content)


class SwiftConfigGenerator(ConfigGenerator):
    """Generate Swift configuration files."""
    
    def __init__(
        self,
        bundle_id: str,
        supabase_url: str,
        supabase_key: str,
        apple_team_id: str,
        output_dir: str = "."
    ):
        super().__init__(output_dir)
        self.bundle_id = bundle_id
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.apple_team_id = apple_team_id
    
    def generate_config_swift(self, filename: str = "Config.swift") -> Path:
        """Generate Config.swift file."""
        content = f"""import Foundation

/// Application configuration
struct AppConfig {{
    // MARK: - Supabase
    static let supabaseUrl = URL(string: "{self.supabase_url}")!
    static let supabaseAnonKey = "{self.supabase_key}"
    
    // MARK: - App Identity
    static let bundleId = "{self.bundle_id}"
    static let appScheme = "myapp"
    static let teamId = "{self.apple_team_id}"
    
    // MARK: - OAuth
    struct OAuth {{
        // Apple Sign-In
        static let appleTeamId = "{self.apple_team_id}"
        static let appleBundleId = "{self.bundle_id}"
        
        // Google (if using Google Sign-In)
        static let googleClientId = "YOUR_GOOGLE_CLIENT_ID"
        static let googleServerClientId = "YOUR_GOOGLE_SERVER_CLIENT_ID"
    }}
    
    // MARK: - Deep Linking
    static let deepLinkScheme = "myapp://"
    static let authCallbackPath = "auth/callback"
    
    // MARK: - URLs
    static var appDeepLinkUrl: URL {{
        URL(string: "\\(appScheme)://\\(authCallbackPath)")!
    }}
    
    // MARK: - API Endpoints
    struct API {{
        static let baseUrl = "{self.supabase_url}"
        static let authEndpoint = "\\(baseUrl)/auth/v1"
        static let realtimeEndpoint = "\\(baseUrl)/realtime/v1"
    }}
    
    // MARK: - Feature Flags
    struct Features {{
        static let enableAppleSignIn = true
        static let enableGoogleSignIn = false
        static let enablePasswordlessAuth = false
    }}
}}

// MARK: - Environment Configuration
enum Environment {{
    #if DEBUG
    static let current = Environment.development
    #else
    static let current = Environment.production
    #endif
    
    case development
    case staging
    case production
}}

// MARK: - Build Settings
struct BuildInfo {{
    static let version = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "Unknown"
    static let build = Bundle.main.infoDictionary?["CFBundleVersion"] as? String ?? "Unknown"
}}
"""
        
        return self.write_file(filename, content)
    
    def generate_auth_helpers(self, filename: str = "AuthHelpers.swift") -> Path:
        """Generate authentication helper functions."""
        content = f"""import Foundation
import AuthenticationServices
import CryptoKit

// MARK: - Apple Sign-In Helpers

class AppleSignInHelper {{
    private var currentNonce: String?
    
    /// Generate random nonce for Apple Sign-In
    func generateNonce() -> String {{
        let charset = CharacterSet(
            charactersIn: "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-._"
        )
        let random = (0..<32).map {{ _ in
            charset.randomElement()!
        }}
        return String(random)
    }}
    
    /// Create SHA256 hash of nonce (required by Apple)
    func sha256(_ input: String) -> String {{
        let inputData = Data(input.utf8)
        let hashedData = SHA256.hash(data: inputData)
        let hashString = hashedData.compactMap {{ String(format: "%02x", $0) }}.joined()
        return hashString
    }}
    
    /// Perform Sign in with Apple request
    func performSignIn(presentationAnchor: ASPresentationAnchor) async throws -> ASAuthorizationAppleIDCredential {{
        let nonce = generateNonce()
        self.currentNonce = nonce
        
        let request = ASAuthorizationAppleIDProvider().createRequest()
        request.requestedScopes = [.fullName, .email]
        request.nonce = sha256(nonce)
        
        let authorizationController = ASAuthorizationController(authorizationRequests: [request])
        
        return try await withCheckedThrowingContinuation {{ continuation in
            authorizationController.delegate = AppleSignInDelegate(continuation: continuation)
            authorizationController.presentationContextProvider = AppleSignInPresentationProvider(anchor: presentationAnchor)
            authorizationController.performRequests()
        }}
    }}
}}

// MARK: - Apple Sign-In Delegates

class AppleSignInDelegate: NSObject, ASAuthorizationControllerDelegate {{
    private let continuation: CheckedContinuation<ASAuthorizationAppleIDCredential, Error>
    
    init(continuation: CheckedContinuation<ASAuthorizationAppleIDCredential, Error>) {{
        self.continuation = continuation
    }}
    
    func authorizationController(
        _ controller: ASAuthorizationController,
        didCompleteWithAuthorization authorization: ASAuthorization
    ) {{
        if let credential = authorization.credential as? ASAuthorizationAppleIDCredential {{
            continuation.resume(returning: credential)
        }}
    }}
    
    func authorizationController(
        _ controller: ASAuthorizationController,
        didCompleteWithError error: Error
    ) {{
        continuation.resume(throwing: error)
    }}
}}

class AppleSignInPresentationProvider: NSObject, ASAuthorizationControllerPresentationContextProviding {{
    let anchor: ASPresentationAnchor
    
    init(anchor: ASPresentationAnchor) {{
        self.anchor = anchor
    }}
    
    func presentationAnchor(for controller: ASAuthorizationController) -> ASPresentationAnchor {{
        anchor
    }}
}}

// MARK: - Keychain Helpers

class KeychainHelper {{
    static let shared = KeychainHelper()
    
    enum KeychainError: Error {{
        case saveFailed
        case retrieveFailed
        case deleteFailed
    }}
    
    /// Save token to secure Keychain
    func saveToken(_ token: String, forKey key: String) throws {{
        let data = token.data(using: .utf8)!
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        ]
        
        SecItemDelete(query as CFDictionary)
        
        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {{
            throw KeychainError.saveFailed
        }}
    }}
    
    /// Retrieve token from Keychain
    func retrieveToken(forKey key: String) throws -> String? {{
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true
        ]
        
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        
        guard status != errSecItemNotFound else {{
            return nil
        }}
        
        guard status == errSecSuccess,
              let data = result as? Data,
              let token = String(data: data, encoding: .utf8) else {{
            throw KeychainError.retrieveFailed
        }}
        
        return token
    }}
    
    /// Delete token from Keychain
    func deleteToken(forKey key: String) throws {{
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key
        ]
        
        let status = SecItemDelete(query as CFDictionary)
        guard status == errSecSuccess || status == errSecItemNotFound else {{
            throw KeychainError.deleteFailed
        }}
    }}
}}
"""
        
        return self.write_file(filename, content)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="auth-config-generator",
        description="Generate OAuth and authentication configurations"
    )
    
    parser.add_argument("--output", default=".", help="Output directory")
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Command")
    
    # Supabase command
    sub = subparsers.add_parser("supabase", help="Generate Supabase config")
    sub.add_argument("--project-id", required=True)
    sub.add_argument("--api-key", required=True)
    sub.add_argument("--jwt-secret", required=True)
    sub.add_argument("--service-role-key")
    
    # Apple command
    sub = subparsers.add_parser("apple", help="Generate Apple OAuth config")
    sub.add_argument("--team-id", required=True)
    sub.add_argument("--bundle-id", required=True)
    sub.add_argument("--app-name", required=True)
    
    # Google command
    sub = subparsers.add_parser("google", help="Generate Google OAuth config")
    sub.add_argument("--project-id", required=True)
    sub.add_argument("--client-id", required=True)
    sub.add_argument("--client-secret", required=True)
    
    # Swift command
    sub = subparsers.add_parser("swift", help="Generate Swift config")
    sub.add_argument("--bundle-id", required=True)
    sub.add_argument("--supabase-url", required=True)
    sub.add_argument("--supabase-key", required=True)
    sub.add_argument("--apple-team-id", required=True)
    
    args = parser.parse_args()
    
    try:
        if args.command == "supabase":
            gen = SupabaseConfigGenerator(
                project_id=args.project_id,
                api_key=args.api_key,
                jwt_secret=args.jwt_secret,
                service_role_key=args.service_role_key,
                output_dir=args.output
            )
            gen.generate_env_file()
            gen.generate_guide()
            print(f"✓ Generated Supabase config in {args.output}")
        
        elif args.command == "apple":
            gen = AppleOAuthGenerator(
                team_id=args.team_id,
                bundle_id=args.bundle_id,
                app_name=args.app_name,
                output_dir=args.output
            )
            gen.generate_entitlements()
            gen.generate_setup_guide()
            print(f"✓ Generated Apple OAuth config in {args.output}")
        
        elif args.command == "google":
            gen = GoogleOAuthGenerator(
                project_id=args.project_id,
                client_id=args.client_id,
                client_secret=args.client_secret,
                output_dir=args.output
            )
            gen.generate_credentials_json()
            gen.generate_setup_guide()
            print(f"✓ Generated Google OAuth config in {args.output}")
        
        elif args.command == "swift":
            gen = SwiftConfigGenerator(
                bundle_id=args.bundle_id,
                supabase_url=args.supabase_url,
                supabase_key=args.supabase_key,
                apple_team_id=args.apple_team_id,
                output_dir=args.output
            )
            gen.generate_config_swift()
            gen.generate_auth_helpers()
            print(f"✓ Generated Swift config in {args.output}")
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
