# Automated Anniversary and Birthday Wishes Poster

This project is a Python-based tool designed to automate the posting of anniversary and birthday wishes to teachers in Google Chat spaces. It streamlines the process of sending personalized greetings to teachers on special occasions, enhancing communication and fostering a positive atmosphere within educational environments.

## Key Features:
- **Automated Greetings Posting**: The tool automates the process of posting anniversary and birthday wishes to designated Google Chat spaces, eliminating the need for manual intervention.
- **Seamless Integration**: Utilizes Python, Pandas, Google Chat API, Pygsheets, and Pillow libraries to ensure seamless integration with Google Chat and Google Sheets.
- **Template Management**: Stores anniversary and birthday templates in Google Sheets for easy access and management, allowing for quick customization and modification.
- **Personalization**: Utilizes the Pillow library to modify creative images by adding teacher names at the bottom 20% of each image, ensuring personalized greetings.
- **Timely Delivery**: Automatically posts modified creative images along with the respective templates in designated Google Chat spaces, ensuring timely delivery of greetings.

## Technologies Used:
- Python
- Pandas
- Google Chat API
- Pygsheets
- Pillow

## How It Works:

1. The tool retrieves anniversary, birthday templates, Teacher Name and Space_ID stored in Google Sheets.
2. Using the Pillow library, it modifies creative images by adding teacher names at the bottom 20% of each image.
3. It then automatically posts the modified creative images along with the respective templates in designated Google Chat spaces.
4. This process ensures timely and personalized greetings to teachers on their special occasions.

## Benefits:
- Saves time and effort by automating the process of sending anniversary and birthday wishes.
- Enhances communication and strengthens relationships with teachers.
- Facilitates personalized greetings, fostering a positive atmosphere within educational environments.

## Usage:
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Configure Google Chat API credentials and access to Google Sheets.
4. Run the tool and enjoy automated anniversary and birthday wishes posting.

## Contributions:
Contributions are welcome! Feel free to fork the repository, make improvements, and submit pull requests.

## License:
This project is licensed under the [MIT License](LICENSE).

## Contact:
For any inquiries or support, please contact [Sudhanshu Kumar](mailto:Sudhansu65r@gmail.com).
