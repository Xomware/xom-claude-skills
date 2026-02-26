# Auth Config Generator - Setup Checklist

## Supabase OAuth Setup Checklist

- [ ] Supabase project created
- [ ] Project URL recorded
- [ ] Anon key obtained
- [ ] Service role key stored securely
- [ ] JWT secret configured
- [ ] Redirect URLs registered in Auth Settings
- [ ] OAuth providers enabled:
  - [ ] Google
  - [ ] Apple
  - [ ] GitHub (optional)
- [ ] Row Level Security (RLS) policies created
- [ ] Email templates customized (optional)
- [ ] Webhook URLs configured (optional)
- [ ] Development environment configured
- [ ] Staging environment configured
- [ ] Production environment configured

**Verification Steps:**
```bash
# Test connection
curl -H "Authorization: Bearer $ANON_KEY" \
  https://$PROJECT_ID.supabase.co/rest/v1/

# Should return 200 OK
```

## Apple OAuth Setup Checklist

### Prerequisites
- [ ] Apple Developer Account (paid)
- [ ] Team ID obtained
- [ ] Bundle ID decided (e.g., com.example.app)

### App ID Configuration
- [ ] Log in to Apple Developer Account
- [ ] Create new App ID with:
  - [ ] Explicit App ID (not wildcard)
  - [ ] Bundle ID: {BUNDLE_ID}
  - [ ] Description set
- [ ] Enable "Sign in with Apple" capability
  - [ ] Configure as primary app
  - [ ] Set up email settings (shared vs private)

### Signing Certificate
- [ ] Create iOS App Development certificate
- [ ] Create iOS App Distribution certificate
- [ ] Download and install certificates

### Provisioning Profiles
- [ ] Create development provisioning profile
- [ ] Create distribution provisioning profile
- [ ] Download profiles
- [ ] Install in Xcode

### Xcode Configuration
- [ ] Update Bundle ID in Xcode
- [ ] Select correct signing team
- [ ] Add "Sign in with Apple" capability
- [ ] Entitlements.plist configured
- [ ] Device added to development team (for testing)

### Code Setup
- [ ] AuthenticationServices framework imported
- [ ] ASAuthorizationAppleIDProvider initialized
- [ ] Nonce generation implemented
- [ ] Credential handling implemented
- [ ] Keychain storage configured

**Verification Steps:**
```swift
// Test Sign in with Apple
import AuthenticationServices

let provider = ASAuthorizationAppleIDProvider()
let request = provider.createRequest()
request.requestedScopes = [.email, .fullName]
// Should complete without "invalid bundle ID" error
```

## Google OAuth Setup Checklist

### GCP Project
- [ ] Google Cloud Project created
- [ ] Project ID noted
- [ ] Billing enabled

### APIs & Services
- [ ] Google+ API enabled
- [ ] Google Identity Services API enabled
- [ ] Google Identity Service API enabled

### OAuth Consent Screen
- [ ] User type selected (External)
- [ ] App information filled:
  - [ ] App name
  - [ ] User support email
  - [ ] Developer contact info
- [ ] Logo/brand assets added
- [ ] Privacy policy URL added
- [ ] Terms of service URL added (optional)
- [ ] Scopes configured:
  - [ ] openid
  - [ ] email
  - [ ] profile
- [ ] Sensitive scope claims added

### OAuth Credentials
- [ ] OAuth 2.0 Client ID created
- [ ] Application type selected:
  - [ ] Web application (for backend)
  - [ ] iOS app (for iOS)
  - [ ] Android app (for Android)
- [ ] Authorized redirect URIs added:
  - [ ] http://localhost:3000/auth/callback
  - [ ] https://yourdomain.com/auth/callback
- [ ] Authorized JavaScript origins configured
- [ ] Client ID obtained
- [ ] Client secret obtained
- [ ] Credentials JSON downloaded

### Service Account (if needed)
- [ ] Service account created
- [ ] Service account key generated
- [ ] Key JSON downloaded securely

**Verification Steps:**
```bash
# Test client ID
curl -X POST https://oauth2.googleapis.com/token \
  -d "code=AUTH_CODE&client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET&redirect_uri=http://localhost:3000/auth/callback&grant_type=authorization_code"

# Should return access_token
```

## Swift iOS Configuration Checklist

### Xcode Project Setup
- [ ] Bundle ID set correctly
- [ ] Team ID configured
- [ ] Signing certificate selected

### Info.plist Updates
- [ ] CFBundleIdentifier set to {BUNDLE_ID}
- [ ] Deep link URL schemes configured
- [ ] Query scheme whitelist added (if needed)

### Supabase Integration
- [ ] Supabase Swift SDK added (via SPM or CocoaPods)
- [ ] Config.swift created with:
  - [ ] SUPABASE_URL
  - [ ] SUPABASE_ANON_KEY
  - [ ] Deep link scheme
  - [ ] Auth callback path
- [ ] SupabaseClient initialized in AppDelegate

### Apple Sign-In Setup
- [ ] AuthenticationServices framework imported
- [ ] Sign in with Apple capability enabled
- [ ] Entitlements.plist configured:
  - [ ] com.apple.developer.applesignin = Default
  - [ ] keychain-access-groups configured
- [ ] Apple Sign-In button UI added
- [ ] SignInWithAppleButton implemented
- [ ] ASAuthorizationControllerDelegate implemented
- [ ] Nonce generation added
- [ ] Token verification implemented

### Google Sign-In Setup (if using)
- [ ] GoogleSignIn SDK installed
- [ ] Client ID configured in code
- [ ] GIDSignIn initialization in AppDelegate
- [ ] Sign-in button UI added
- [ ] Token handling implemented

### Keychain Configuration
- [ ] Keychain access group set (for team apps)
- [ ] KeychainHelper or similar utility created
- [ ] Token storage implemented securely
- [ ] Token retrieval with error handling

### Deep Linking
- [ ] URL scheme configured (e.g., myapp://)
- [ ] SceneDelegate configured to handle URLs
- [ ] Auth callback path handled
- [ ] Token extraction from URL implemented

### Testing
- [ ] Sign in with Apple works on real device
- [ ] Nonce matches between client and server
- [ ] Tokens stored and retrieved from Keychain
- [ ] Token refresh works
- [ ] Sign out clears Keychain
- [ ] Deep linking redirects correctly

**Verification Tests:**
```swift
// Test Keychain access
let helper = KeychainHelper.shared
try helper.saveToken("test-token", forKey: "auth_token")
let retrieved = try helper.retrieveToken(forKey: "auth_token")
assert(retrieved == "test-token")  // Should pass

// Test nonce generation
let nonce = AppleSignInHelper().generateNonce()
assert(nonce.count == 32)  // Should pass
```

## Environment-Specific Configuration

### Development
- [ ] Local Supabase instance (or Supabase free tier)
- [ ] ngrok or similar for local HTTPS
- [ ] http://localhost:3000 registered as redirect URI
- [ ] Test credentials created
- [ ] Test user accounts created

### Staging
- [ ] Staging Supabase project
- [ ] Staging bundle ID (e.g., com.example.app.staging)
- [ ] Staging certificate created
- [ ] Staging provisioning profile created
- [ ] https://staging.yourdomain.com registered
- [ ] Staging Google OAuth credentials

### Production
- [ ] Production Supabase project
- [ ] Production bundle ID
- [ ] Production certificate (Apple)
- [ ] Production provisioning profile
- [ ] Production Google OAuth credentials
- [ ] Production URLs registered
- [ ] HTTPS enforced everywhere
- [ ] Secrets rotated

## Security Checklist

- [ ] No API keys in version control
- [ ] Secrets stored in .env or environment variables
- [ ] JWT secret rotated on schedule
- [ ] HTTPS enforced in production
- [ ] Tokens use appropriate expiration times
- [ ] Refresh tokens used for long-lived sessions
- [ ] Keychain (iOS) used for token storage
- [ ] No sensitive data logged
- [ ] CORS properly configured
- [ ] Rate limiting enabled on auth endpoints
- [ ] Input validation on all auth endpoints
- [ ] Error messages don't leak sensitive info
- [ ] PKCE used for OAuth flows (where applicable)
- [ ] State parameter validated in OAuth callback

## Troubleshooting Checklist

### Apple Sign-In Issues
- [ ] Bundle ID matches provisioning profile
- [ ] Team ID is correct
- [ ] Entitlements.plist syntax valid
- [ ] Sign in with Apple enabled in App ID
- [ ] Certificate not expired
- [ ] App has correct capabilities

### Google OAuth Issues
- [ ] Client ID is for OAuth credentials (not API key)
- [ ] Redirect URI matches exactly (including trailing slash)
- [ ] Client secret is correct
- [ ] Google+ API is enabled in GCP
- [ ] Authorized JavaScript origins configured
- [ ] Consent screen is published

### Supabase Issues
- [ ] Redirect URLs registered in Auth Settings
- [ ] JWT secret matches between client and server
- [ ] Token expiration not too short
- [ ] RLS policies allow auth operations
- [ ] Email provider configured
- [ ] SMTP settings if using custom email

### iOS App Issues
- [ ] CocoaPods/SPM dependencies updated
- [ ] Bridging header configured (if using Objective-C)
- [ ] Framework linked correctly
- [ ] Privacy settings allow Keychain access
- [ ] Entitlements provisioned correctly

## Post-Setup Verification

- [ ] Can sign up with email/password
- [ ] Can sign in with email/password
- [ ] Can sign in with Apple
- [ ] Can sign in with Google
- [ ] Tokens are valid and decode correctly
- [ ] Token refresh works
- [ ] Sign out clears authentication
- [ ] Deep linking redirects to app
- [ ] Errors handled gracefully
- [ ] No sensitive data in logs
- [ ] Performance is acceptable (< 500ms auth)
- [ ] Works on both simulators and real devices

## Maintenance Checklist

### Weekly
- [ ] Monitor auth error rates
- [ ] Check for failed OAuth attempts
- [ ] Review access logs for anomalies

### Monthly
- [ ] Review and update dependencies
- [ ] Check certificate expiration dates
- [ ] Test authentication flows

### Quarterly
- [ ] Rotate secrets and API keys
- [ ] Audit access logs
- [ ] Review security configurations
- [ ] Update documentation

### Annually
- [ ] Renew Apple Developer certificate
- [ ] Renew SSL certificates
- [ ] Full security audit
- [ ] Penetration testing (optional but recommended)

## Documentation Requirements

Ensure you have documented:
- [ ] Setup instructions (one-time)
- [ ] Configuration guide (for team)
- [ ] Troubleshooting guide
- [ ] OAuth flow diagrams
- [ ] API reference for auth endpoints
- [ ] Token management procedures
- [ ] Secret rotation procedures
- [ ] Disaster recovery procedures
- [ ] Contact list for emergency support
