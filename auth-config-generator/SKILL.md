---
name: auth-config-generator
description: Use this skill to generate OAuth setup configurations for Supabase, Apple, and Google authentication. Includes config file generation, setup guides, Swift configuration files, and troubleshooting tips. Essential for rapid OAuth integration and mobile app authentication setup.
license: MIT
---

# Auth Config Generator - OAuth & Supabase Setup

## Overview

This skill automates the generation of authentication configurations for modern app development:

- **Supabase OAuth configs** - Environment files, connection strings, JWT settings
- **Apple OAuth guides** - App ID setup, entitlements, provisioning profiles
- **Google OAuth guides** - Service account setup, client IDs, scopes
- **Swift config files** - iOS app configuration, deep linking, keychain setup
- **Troubleshooting & gotchas** - Common pitfalls and solutions

Perfect for:
- Setting up OAuth for new projects
- Onboarding team members
- Documenting auth setup in codebases
- Quick reference guides

## Quick Start

### Generate Supabase Config

```bash
auth-config-generator supabase \
  --project-id my-supabase-project \
  --api-key sk_live_... \
  --jwt-secret your-jwt-secret \
  --output supabase.env

# Output:
# SUPABASE_URL=https://my-supabase-project.supabase.co
# SUPABASE_ANON_KEY=...
# SUPABASE_SERVICE_ROLE_KEY=...
# JWT_SECRET=...
```

### Generate Apple OAuth Setup Guide

```bash
auth-config-generator apple \
  --team-id ABC123DEFG \
  --bundle-id com.example.app \
  --app-name "My App" \
  --output apple-setup.md

# Generates:
# - Step-by-step setup guide
# - Entitlements.plist content
# - Code examples
# - Troubleshooting
```

### Generate Google OAuth Setup

```bash
auth-config-generator google \
  --project-id my-google-project \
  --client-id client-id.apps.googleusercontent.com \
  --client-secret secret \
  --output google-oauth.json

# Generates:
# - OAuth consent setup guide
# - Required scopes
# - Service account config
# - Testing endpoints
```

### Generate Swift iOS Config

```bash
auth-config-generator swift \
  --bundle-id com.example.app \
  --supabase-url https://...supabase.co \
  --supabase-key ... \
  --apple-team-id ABC123DEFG \
  --output Config.swift

# Generates:
# - Config.swift with all URLs and keys
# - Deep linking configuration
# - Keychain setup helpers
# - OAuth flow enums
```

### Generate Complete Setup Package

```bash
auth-config-generator bundle \
  --type "ios-supabase-oauth" \
  --project-name "MyApp" \
  --output ./auth-setup/

# Creates directory with:
# - supabase.env
# - Apple setup guide
# - Google setup guide
# - Config.swift
# - iOS-specific troubleshooting
# - Integration checklist
```

## Python API

```python
from auth_config_generator import (
    SupabaseConfigGenerator,
    AppleOAuthGenerator,
    GoogleOAuthGenerator,
    SwiftConfigGenerator
)

# Generate Supabase config
supabase_gen = SupabaseConfigGenerator(
    project_id="my-project",
    api_key="sk_live_...",
    jwt_secret="secret"
)
supabase_gen.generate_env_file("supabase.env")
supabase_gen.generate_guide("supabase-setup.md")

# Generate Apple OAuth
apple_gen = AppleOAuthGenerator(
    team_id="ABC123DEFG",
    bundle_id="com.example.app",
    app_name="My App"
)
apple_gen.generate_setup_guide("apple-oauth.md")
apple_gen.generate_entitlements("Entitlements.plist")

# Generate Google OAuth
google_gen = GoogleOAuthGenerator(
    project_id="my-gcp-project",
    client_id="...",
    client_secret="..."
)
google_gen.generate_credentials_json("google-oauth.json")
google_gen.generate_guide("google-oauth.md")

# Generate Swift config
swift_gen = SwiftConfigGenerator(
    bundle_id="com.example.app",
    supabase_url="https://...supabase.co",
    supabase_key="...",
    apple_team_id="ABC123DEFG"
)
swift_gen.generate_config("Config.swift")
swift_gen.generate_helpers("AuthHelpers.swift")
```

## Configuration Generation

### Supabase Environment File

Generated `supabase.env`:
```env
# Supabase
SUPABASE_URL=https://abcdefg.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# JWT
JWT_SECRET=your-jwt-secret-here
JWT_EXPIRATION=3600

# URLs
REDIRECT_URL=https://yourapp.com/auth/callback
```

### Apple OAuth Entitlements.plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.developer.applesignin</key>
    <array>
        <string>Default</string>
    </array>
    <key>keychain-access-groups</key>
    <array>
        <string>$(AppIdentifierPrefix)com.example.app</string>
    </array>
</dict>
</plist>
```

### Swift Configuration

Generated `Config.swift`:
```swift
import Foundation

struct AuthConfig {
    // Supabase
    static let supabaseUrl = URL(string: "https://abcdefg.supabase.co")!
    static let supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    
    // Apple OAuth
    static let appleTeamId = "ABC123DEFG"
    static let bundleId = "com.example.app"
    
    // URLs
    static let appDeepLink = URL(string: "myapp://auth/callback")!
    static let redirectUrl = "myapp://auth/callback"
    
    // OAuth Scopes
    enum AppleScopes: String {
        case email
        case fullName = "full_name"
    }
}

// Keychain helpers
class KeychainHelper {
    static func saveToken(_ token: String) throws {
        let data = token.data(using: .utf8)!
        // Keychain implementation
    }
    
    static func retrieveToken() throws -> String? {
        // Keychain retrieval
        return nil
    }
}
```

## Setup Guides

### Apple OAuth Setup Steps

1. **Create App ID**
   - Go to Apple Developer account
   - Create new App ID with `Sign in with Apple` capability
   - Enter Bundle ID: `com.example.app`

2. **Configure Sign in with Apple**
   - Enable "Sign in with Apple" service
   - Set up return URLs
   - Configure email privacy settings

3. **Add Entitlements**
   - Add `com.apple.developer.applesignin` entitlement
   - Set value to `Default`

4. **Update Info.plist**
   ```xml
   <key>CFBundleIdentifier</key>
   <string>com.example.app</string>
   ```

5. **Implement in Code**
   - Import `AuthenticationServices`
   - Create `ASAuthorizationController`
   - Handle credentials and errors

### Google OAuth Setup Steps

1. **Create GCP Project**
   - Go to Google Cloud Console
   - Create new project
   - Enable Google+ API

2. **Create OAuth Credentials**
   - Create OAuth 2.0 Client ID
   - Choose "Web application" or "iOS app"
   - Add redirect URIs
   - Download client secrets JSON

3. **Configure Consent Screen**
   - Fill in app information
   - Add required scopes
   - Set logo and privacy policy

4. **Test Configuration**
   - Use Google's OAuth playground
   - Test with sample credentials
   - Verify refresh token flow

5. **Integrate in Code**
   - Import Google Auth library
   - Initialize with client ID
   - Handle sign-in flow

## Swift Integration Examples

### Sign in with Apple

```swift
import AuthenticationServices

class AuthManager: NSObject, ASAuthorizationControllerDelegate {
    
    func startSignInWithApple() {
        let request = ASAuthorizationAppleIDProvider().createRequest()
        request.requestedScopes = [.email, .fullName]
        
        let controller = ASAuthorizationController(authorizationRequests: [request])
        controller.delegate = self
        controller.presentationContextProvider = self
        controller.performRequests()
    }
    
    func authorizationController(
        _ controller: ASAuthorizationController,
        didCompleteWithAuthorization authorization: ASAuthorization
    ) {
        if let appleIDCredential = authorization.credential as? ASAuthorizationAppleIDCredential {
            let userIdentifier = appleIDCredential.user
            let email = appleIDCredential.email ?? ""
            let fullName = appleIDCredential.fullName?.givenName ?? ""
            
            // Sign in with Supabase
            Task {
                try await signInWithApple(
                    identityToken: appleIDCredential.identityToken!,
                    nonce: appleIDCredential.nonce!
                )
            }
        }
    }
}
```

### Sign in with Google

```swift
import GoogleSignIn

class GoogleAuthManager {
    
    func signInWithGoogle() {
        guard let clientID = GIDSignIn.sharedInstance.configuration?.clientID else { return }
        
        GIDSignIn.sharedInstance.signIn(withPresenting: nil) { result, error in
            if let error = error {
                print("Error signing in with Google: \(error)")
                return
            }
            
            guard let user = result?.user,
                  let idToken = user.idToken?.tokenString else {
                return
            }
            
            // Sign in with Supabase
            Task {
                try await supabase.auth.signInWithIdToken(
                    credentials: .init(provider: .google, idToken: idToken)
                )
            }
        }
    }
}
```

## Troubleshooting Guide

### Apple Sign-in Issues

**Problem: "The operation couldn't be completed. (com.apple.AuthenticationServices.AuthorizationError error 1001.)"**
- Solution: Check entitlements are configured correctly
- Ensure bundle ID matches provisioning profile
- Verify App ID has Sign in with Apple capability enabled

**Problem: Identity token is nil**
- Solution: Request `.email` and `.fullName` scopes
- Check user data privacy settings
- Verify nonce is included in request

**Problem: Credential persistence fails**
- Solution: Use Keychain for secure storage
- Implement proper error handling
- Check app sandbox entitlements

### Google OAuth Issues

**Problem: "Invalid client id" error**
- Solution: Verify client ID is from OAuth credentials, not API key
- Check bundle ID matches GCP configuration
- Ensure correct redirect URIs are registered

**Problem: Refresh token not returned**
- Solution: Use `access_type=offline` in auth request
- Force consent screen with `prompt=consent`
- Check token expiration settings

**Problem: Email claim missing**
- Solution: Add `email` scope to OAuth request
- Enable Google+ API in GCP
- Verify consent screen has required scopes

### Supabase Integration Issues

**Problem: "Invalid JWT" or auth failures**
- Solution: Verify JWT_SECRET matches Supabase project
- Check token expiration time
- Ensure token is properly signed

**Problem: Redirect URL mismatch**
- Solution: Register exact redirect URL in Supabase
- Include protocol (https://)
- Test with allowed URLs

## Gotchas & Best Practices

### Security

✓ **DO:**
- Store tokens in secure Keychain (iOS)
- Use HTTPS for all endpoints
- Rotate secrets regularly
- Validate JWT tokens on backend

✗ **DON'T:**
- Hardcode secrets in code
- Store tokens in UserDefaults (iOS)
- Log sensitive information
- Use expired tokens

### Development vs Production

```swift
#if DEBUG
let config = AuthConfig.Development()
#else
let config = AuthConfig.Production()
#endif
```

### Token Management

```swift
// Implement automatic refresh
class TokenManager {
    func refreshTokenIfNeeded() async {
        if isTokenExpiringSoon() {
            try await refreshAccessToken()
        }
    }
    
    private func isTokenExpiringSoon() -> Bool {
        let expiresAt = // get from keychain
        return Date().addingTimeInterval(300) > expiresAt
    }
}
```

## See Also

- **references/** - Complete configuration templates and examples
- **scripts/auth-config-generator.py** - Main generator implementation
- **references/checklists/** - Setup verification checklists
