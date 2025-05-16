# Email Spam Detection System

A comprehensive Machine Learning system for detecting spam emails using Natural Language Processing and various classification algorithms.

## Features

- **Accurate Spam Detection**: Advanced ML model trained on a diverse dataset of emails
- **Web-based Interface**: User-friendly web application for easy interaction
- **Real-time Analysis**: Immediate results with confidence scores
- **Comprehensive Model Report**: Detailed analysis of model performance and insights
- **Dark/Light Mode**: UI themes for better user experience

## Project Structure

The project consists of the following components:

- Spam detection model (`spam_detection_model.pkl`)
- Flask web application (`main.py`)
- Utility functions (`utility.py`)
- HTML templates (`templates/`)
- Static assets (`static/`)

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```
4. Navigate to `http://127.0.0.1:5000` in your web browser

## Usage

### Spam Detection

1. Enter the email text in the provided text area or use the example buttons
2. Click "Analyze Email"
3. View the analysis results with confidence scores

### Model Report

1. Navigate to the "Model Report" page from the navigation bar
2. Explore detailed information about:
   - Dataset information
   - Model comparison
   - Best model analysis
   - Performance metrics
   - Limitations and challenges

## Technical Details

### Model

The system uses a machine learning pipeline with the following components:

1. Text preprocessing with custom cleaning functions
2. TF-IDF vectorization with n-grams
3. Feature engineering for spam indicators
4. Multiple classification algorithms comparison:
   - Logistic Regression
   - Multinomial Naive Bayes
   - Linear Support Vector Machine
   - Random Forest

### Performance

The final model achieves:
- Accuracy: 97.8%
- Precision (Spam): 97.2%
- Recall (Spam): 94.5%
- F1 Score: 95.8%

## Future Enhancements

- Integration with email clients
- Support for multiple languages
- Continuous model retraining with user feedback
- API access for third-party applications

## License

This project is available under the MIT License.

## Acknowledgments

- Dataset sources: [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection)
- Libraries: scikit-learn, pandas, matplotlib, Flask, Bootstrap
