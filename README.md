## Configuration

+ 1. Copy the example environment file:
+ ```bash
+ cp .env.example .env
+ ```
+ 
+ 2. Edit .env file with your settings:
+ ```plaintext
+ OPENAI_API_KEY=your-api-key-here
+ OPENAI_MODEL=gpt-4
+ ```
+
The following environment variables are supported:

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: OpenAI model to use (default: "gpt-4") 

## Troubleshooting

### Common Issues:

1. API Key Issues:
   - Ensure OPENAI_API_KEY is correctly set in .env
   - Check API key permissions

2. File Upload Issues:
   - Verify file format is .pot
   - Check file permissions
   - Ensure upload directory exists

3. Docker Issues:
   - Verify Docker daemon is running
   - Check port availability
   - Ensure sufficient permissions

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 