# Multilingual Chatbot for Commonwealth Bank

## Project Overview

This project aims to revolutionize chatbot accessibility for non-English speaking customers of Commonwealth Bank by leveraging serverless computing and advanced AI language processing technologies. Our solution enables multilingual capabilities within chatbot interfaces, facilitating banking inquiries in the customer's native language to foster inclusivity and ease of interaction from diverse linguistic backgrounds.

### Challenge

The initiative focuses on enhancing communication through:
- Auto-detecting the language used by the user.
- Processing banking inquiries in multiple languages.
- Utilizing user-friendly interfaces that consider cultural nuances to bridge the communication gap.

### Solution

We are developing a chatbot that integrates with Azure Function Apps for serverless computing, Azure Cognitive Services for language detection and translation, and OpenAI's API for AI-driven response generation. This approach aims to provide seamless engagement for customers across various linguistic backgrounds.

## Technology Stack

- **Azure Function Apps**: Serverless computing for chatbot logic.
- **Azure Cognitive Services & Translator Text API**: For multilingual support.
- **OpenAI API**: Advanced AI for context-aware responses.
- **Cosmos DB**: NoSQL database for storing scraped data.
- **Azure AI Search & RAG**: Enhancing data retrieval and response generation.
- **Azure Key Vault**: Securing secrets.
- **Selenium**: Web scraping.
- **React**: Frontend interface.
- **GitHub Actions**: CI/CD for deployment.
- **Visual Studio Code**: IDE with Azure and Python extensions.
- **Python 3.11**: Programming language.


## Setup and Installation

### Prerequisites

- An Azure account with access to Azure Function Apps and Azure Cognitive Services.
- An OpenAI API key for integrating chatbot intelligence.
- Python 3.11 installed on your machine.
- Visual Studio Code with Azure Function App and Python extensions installed.
- Git for version control.

### Basic Infrastructure Setup

1. **Azure Function App Setup**
   - Create a new Function App resource in Azure.
   - Follow the Azure documentation for initial setup: [Azure Function Apps Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/).
2. **Azure Cognitive Services Integration**
   - Set up an instance of Azure Cognitive Services for language detection and translation capabilities.
   - Securely store the API key and endpoint URL for later use in the application.

3. **OpenAI API Integration**
   - Sign up for an OpenAI API key.
   - Securely store the API key for use in the chatbot's response generation logic.

### Running the Project

1. Clone the project repository to your local machine.
    ```bash
    git clone https://github.com/ITU-0327/CBA_Multilingual_Chatbot
    ```

2. Install the required Python dependencies.
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables for Azure and OpenAI API keys.
   - Create a .env file in the root directory of your project.
   - Add your Azure Cognitive Services and OpenAI API keys as follows:
     ```
     AZURE_TRANSLATOR_TEXT_KEY=<your-translator-text-api-key>
     AZURE_SERVICE_REGION=<your-service-region>
     OPENAI_API_KEY=<your-openai-api-key>
     ```

4. Start the Azure Function App locally for testing.
   - Follow the Azure Functions extension in Visual Studio Code to run your app.

## Development and Contribution

### Mock Data Preparation

- Create mock data covering a range of banking inquiries in different languages for initial testing.

### Testing and Feedback

- Perform functionality and user experience testing with multilingual individuals.
- Iteratively refine the chatbot based on feedback.

### Demonstration Preparation

- Develop scenarios to showcase the chatbot's capabilities effectively.
- Prepare presentation materials and practice demonstration scenarios.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Contributors

- **Tony** - Contributed to the overall project development, focusing on integrating Azure Function Apps and ensuring seamless operation across different components of the chatbot. Provided leadership and ensured smooth operation across chatbot components.
  - [GitHub](https://github.com/ITU-0327)
  - [LinkedIn](https://www.linkedin.com/in/i-tung-hsieh-it)

- **Akshita** - Played a key role in integrating Azure Cognitive Services, ensuring the chatbot's language detection and response generation capabilities were optimized for multilingual support. Additionally, Akshita took on the role of project manager, overseeing project timelines, coordinating tasks among team members, and ensuring project milestones were met efficiently.
  - [GitHub]()
  - [LinkedIn]()

- **Kimme** - Specialized in user experience and testing, making the chatbot interface intuitive and accessible across diverse linguistic backgrounds. Led the collection of user feedback and the refinement of chatbot functionality. Played a key role in integrating the Translator API, enriching the chatbot's multilingual support and advanced conversational abilities.
  - [GitHub](https://github.com/shuenyng)
  - [LinkedIn](https://www.linkedin.com/in/shuen-y%E2%80%99ng-tan-942b36198/)

Each member of the team has been instrumental in all phases of the project, from planning and development to testing and refinement, demonstrating a collaborative effort throughout.

---

This project is part of the Monash Innovation Guarantee unit, aiming to use cutting-edge technology to make banking solutions more inclusive and accessible.
