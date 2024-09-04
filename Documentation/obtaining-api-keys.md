# Obtaining API Keys for Cognibot

Cognibot uses APIs from OpenAI and Anthropic to provide its AI-powered features. This guide will walk you through the process of obtaining the necessary API keys for both services.

## OpenAI API Key

OpenAI's API is used for ChatGPT conversations and DALL-E image generation.

1. **Create an OpenAI Account**

   - Go to [OpenAI's website](https://openai.com/).
   - Click on "Sign up" in the top right corner.
   - Follow the prompts to create your account.

2. **Access the API Section**

   - Once logged in, go to the [API section](https://platform.openai.com/account/api-keys).

3. **Generate an API Key**

   - Click on the "Create new secret key" button.
   - Give your key a name (optional).
   - Copy the key immediately and store it securely. You won't be able to see it again!

4. **Set Up Billing (Optional)**

   - OpenAI offers $5 worth of free credit, which expires after 3 months.
   - For continued use, set up billing in the [Billing section](https://platform.openai.com/account/billing/overview).

5. **Usage and Quotas**
   - Be aware of [usage limits and rate limits](https://platform.openai.com/docs/guides/rate-limits).
   - Monitor your usage in the [Usage section](https://platform.openai.com/account/usage).

## Anthropic API Key

Anthropic's API is used for interactions with the Claude AI model.

1. **Request Access**

   - Go to [Anthropic's website](https://www.anthropic.com/).
   - Click on "Get Started" or look for a "Request Access" option.
   - Fill out the form to request API access.
   - Wait for approval (this may take some time).

2. **Create an Account**

   - Once approved, you'll receive an email with instructions to create your account.
   - Follow the link and complete the account creation process.

3. **Access the Console**

   - Log in to your Anthropic account.
   - Navigate to the API or Developer Console section.

4. **Generate an API Key**

   - Look for an option to create or manage API keys.
   - Generate a new API key.
   - Copy the key and store it securely.

5. **Review Documentation**
   - Familiarize yourself with [Anthropic's API documentation](https://www.anthropic.com/product).
   - Pay attention to usage guidelines and best practices.

## Configuring Cognibot

After obtaining both API keys:

1. Open your Cognibot project.
2. Locate the `.env` file (or create one if it doesn't exist).
3. Add your API keys to the file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```
4. Save the file and restart Cognibot for the changes to take effect.

## Security Notes

- Never share your API keys publicly or commit them to version control.
- If you suspect your keys have been compromised, regenerate them immediately.
- Use environment variables or secure secret management systems in production environments.

## Troubleshooting

- If you encounter "Unauthorized" errors, double-check that your API keys are correct and properly set in the `.env` file.
- Ensure you have sufficient credit or an active subscription for both services.
- Check the respective dashboards for any account or API usage issues.

For any further assistance with API keys or integration, please refer to the official documentation of [OpenAI](https://platform.openai.com/docs) and Anthropic, or seek help in our community support channels.
