# ChainCertify: Module Fraud Detection

## Setup Instructions

### Prerequisites

- Python 3.12.x installed on your system.
- Ensure you have `pip` (Python package installer) installed.

### Requirements
The project requires the following Python packages:
```sh
Flask==3.0.3
joblib==1.4.2
numpy==1.26.4
pandas==2.2.2
python-dotenv==1.0.1
requests==2.31.0
web3==6.17.0
```


### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/khanhphamk2/ChainCertify-FraudDetection.git
   cd ChainCertify-FraudDetection
   
2. **Create a virtual environment**
   ```sh
   python -m venv venv
   
3. **Activate the virtual environment**
- On Windows:
   ```sh
   venv/Scripts/activate
- On macOS/Linux:
   ```bash
    source venv/bin/activate
4. **Install the dependencies**
   ```sh
   pip install -r requirements.txt
### Running the API
1. **Set up environment variables:**

   - Copy the example environment file to create a your `.env` file:

     ```sh
     cp .env.example .env
     ```
   - Open the `.env` file and add any necessary environment variables.

   ```sh
    ETHERSCAN_API_KEY = YOUR_ETHERSCAN_API_KEY
    FEATURES = SELECTED FEATURES

2. **Run the application:**

   ```sh
    flask run
    ```
3. **Access the API:**

Open your web browser or API client (like Postman) and navigate to http://127.0.0.1:5000 to interact with your API.

### Additional Notes

- Ensure your virtual environment is activated whenever you work on this project to maintain dependencies correctly.

- You can deactivate the virtual environment by running the following command:

  ```sh
  deactivate
  ```
- To update the packages in the `requirements.txt` file, use the following command:

  ```sh
    pip freeze > requirements.txt
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.