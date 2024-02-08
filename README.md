# Multilingual Chatbot for Commonwealth Bank

## Project Overview

This project aims to revolutionize chatbot accessibility for non-English speaking customers of Commonwealth Bank by leveraging serverless computing and advanced AI language processing technologies. Our solution enables multilingual capabilities within chatbot interfaces, facilitating banking inquiries in the customer's native language to foster inclusivity and ease of interaction from diverse linguistic backgrounds.

### Challenge

The initiative focuses on enhancing communication through:
- Auto-detecting the language spoken by the user.
- Processing banking inquiries in multiple languages.
- Utilizing user-friendly interfaces that consider cultural nuances to bridge the communication gap.

### Solution

We are developing a chatbot that integrates with Azure Function Apps for serverless computing, Azure Cognitive Services for language detection and translation, and OpenAI's API for AI-driven response generation. This approach aims to provide seamless engagement for customers across various linguistic backgrounds.

## Technology Stack

- **Serverless Framework**: Azure Function Apps for hosting and executing chatbot logic without managing infrastructure.
- **Language Detection and Translation**: Azure Cognitive Services, particularly the Translator Text API for translating user queries and responses.
- **AI Model for Response Generation**: OpenAI API, utilizing its advanced natural language processing capabilities for generating contextually relevant responses.
- **IDE**: Visual Studio Code with extensions supporting Azure development and Python programming.
- **Programming Language**: Python 3.11 for scripting and automation tasks.
- **Data Retrieval**: Custom scripts for web scraping, aimed at extracting and structuring data from the Commonwealth Bank's website for retrieval-augmented generation (RAG).

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

[MIT License](LICENSE)

## Contributors

- **Tony** - Contributed to the overall project development, focusing on integrating Azure Function Apps and ensuring seamless operation across different components of the chatbot. Provided leadership and coordination throughout the project.
  - [GitHub](https://github.com/ITU-0327)
  - [LinkedIn](www.linkedin.com/in/i-tung-hsieh-it)

- **Akshita** - Played a key role in integrating Azure Cognitive Services, ensuring the chatbot's language detection and response generation capabilities were optimized for multilingual support. Additionally, Akshita took on the role of project manager, overseeing project timelines, coordinating tasks among team members, and ensuring project milestones were met efficiently.
  - [GitHub]()
  - [LinkedIn]()

- **Kimme** - Focused on user experience and testing, ensuring the chatbot interface was intuitive and accessible for users from diverse linguistic backgrounds. Led the efforts in gathering user feedback and refining the chatbot functionality. Collaborated with Tony in integrating OpenAI's API, contributing to the chatbot's advanced conversational abilities.
  - [GitHub]()
  - [LinkedIn]()

Each member of the team has been instrumental in all phases of the project, from planning and development to testing and refinement, demonstrating a collaborative effort throughout.

---

This project is part of the Monash Innovation Guarantee unit, aiming to use cutting-edge technology to make banking solutions more inclusive and accessible.
