# CHATLEOS

Is a chatbot for company employees where users can make queries and retain information based on company resources: Confluence, Jira, and GitHub; aiming to empower personnel performance and work adaptability with a powerful AI assistant specialized for company tools.

- CHATLEOS utilizes a LLM and Vector Database to optimize work efficiency

- With user-tailored queries, personnel can obtain answers to technical questions immediately.
- CHATLEOS will be using information from GitHub, Jira, Confluence - to answer technical questions
- (Securely hosted on company servers - no leaks of confidential information)

This demo application uses the [SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct) lightweight LLM model (for running on a local machine) and [Chroma](https://www.trychroma.com/) as a vector database.

Currently, CHATLEOS can retrieve documents only from the companies Confuence system by using the Confuence API and setting an API token (to test the application, follow next steps to install the token):

## Steps to Generate an API Token in Confluence

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

## Run App

### Requirements: `Docker desktop`

- Run: `docker compose up`
- Open browser and set next url: http://localhost:4200/
