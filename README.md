Steps to Generate an API Token in Confluence
1. Log in to Atlassian
2. Go to https://id.atlassian.com/manage-profile/security/api-tokens.
3. Sign in with the same account you use for Confluence.
4. Create a New Token
5. Click Create API token.
6. Give it a label (e.g., Confluence Integration).
7. Click Create.
8. Copy the Token

Open compose.yaml file.
Under back > environment, replace username with the email you use to login to confluce and replace password with the token you generated. 