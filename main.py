import os
import sys
import time
import pandas as pd
import pygsheets as pg
import tempfile
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Define global variables
SCOPES = [
    "https://www.googleapis.com/auth/contacts.readonly",
    "https://www.googleapis.com/auth/chat.spaces.readonly",
    "https://www.googleapis.com/auth/chat",
    "https://www.googleapis.com/auth/chat.messages",
    "https://www.googleapis.com/auth/chat.messages.readonly",
    "https://www.googleapis.com/auth/chat.memberships",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.send",
]
SERVICE_KEY_PATH = "TeacherCommunity.json"
TOKEN_PATH = "tc.json"
IMAGES_FOLDER = "Anniversary Images"
ANIV_TEMPLATE_TITLE = "Anniversary"
BIRTH_TEMPLATE_TITLE = "Birthday"

def authenticate(token_file, client_secret):
    """
    Authenticates with Google Workspace and returns the credentials.
    """
    creds = None

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret, SCOPES)
            creds = flow.run_local_server(port=0, prompt="consent", authorization_prompt_message="")

        with open(token_file, "w") as token:
            token.write(creds.to_json())
    return creds

def load_sheet(url, title):
    gs = pg.authorize(custom_credentials=gkey)
    sheet = gs.open_by_url(url)
    return sheet.worksheet("title", title)

def load_images(folder):
    return [img for img in os.listdir(folder) if img.endswith(".jpg")]

def create_anniversary_image(teacher_name, img_path, percent):
    image = Image.open(img_path)
    font = ImageFont.truetype("arial.ttf", 90)
    draw = ImageDraw.Draw(image)
    text = teacher_name
    text_bbox = draw.textbbox((0, 0), text=text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    if text_width > image.width or text_height > image.height:
        aspect_ratio = image.width / image.height
        base_width = max(text_width, image.width)
        new_width = int(base_width * 1.3)
        new_height = int(new_width / aspect_ratio)
        image = image.resize((new_width, new_height))

    text_position = (
        (image.width - text_width) // 2,
        image.height - (image.height * percent) - text_height // 2,
    )
    draw = ImageDraw.Draw(image)
    text_color = (255, 255, 255)
    draw.text(text_position, text, font=font, fill=text_color)

    image_in_memory = BytesIO()
    image.save(image_in_memory, format="PNG")

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        image.save(temp_file, format="PNG")
        temp_file_path = temp_file.name

    return temp_file_path

def upload_media(space_id, file_name, media):
    return (
        chat.media()
        .upload(
            parent=space_id,
            body={"filename": file_name},
            media_body=media,
        )
        .execute()
    )

def send_message(space_id, message, attachment):
    return (
        chat.spaces()
        .messages()
        .create(
            parent=space_id,
            body={"text": message, "attachment": [attachment]},
        )
        .execute()
    )

def main():
    # Authenticate
    gkey = authenticate(TOKEN_PATH, SERVICE_KEY_PATH)

    # Load Sheets
    chat = build("chat", "v1", credentials=gkey)
    sheet = load_sheet(
        "https://docs.google.com/spreadsheets/d/1ta-K8gMuNLctx18cq-JW9y6LfSV8J89dQeJTB9YYHcI/edit#gid=0",
        "Template_List"
    )
    email_sheet = load_sheet("https://docs.google.com/spreadsheets/d/...", "Today")

    # Load Templates
    anniv_temp = sheet.get_as_df(start="A", end="B")["Anniversary"][0]
    birth_temp = sheet.get_as_df(start="A", end="B")["Birthday"][0]

    # Load Data
    anniv_df = email_sheet.get_as_df(start="G", end="M")
    birth_df = email_sheet.get_as_df(start="A", end="F")

    # Loop through Anniversary
    for index, row in anniv_df.iterrows():
        space_id = row["SpaceID"]
        teacher_name = row["Name"].strip()
        image_name = f"{row['Year']}.jpg"
        years = str(row["Year"])
        message_template = anniv_temp.format(TeacherName=teacher_name, Years=years)
        image_path = os.path.join(IMAGES_FOLDER, image_name)

        image = create_anniversary_image(teacher_name, image_path, 0.20)
        media = MediaFileUpload(image, mimetype="image/png")
        media_upload = upload_media(space_id, image, media)

        try:
            result = send_message(space_id, message_template, media_upload)
        except Exception as e:
            print(f"Failed for {teacher_name}")
        print(f"Sent to: {teacher_name}")
        time.sleep(10)

    print("Anniversary Messages Posted 😊👌👌")

    # Loop through Birthdays
    for index, row in birth_df.iterrows():
        space_id = row["SpaceID"]
        teacher_name = row["Name"].strip()
        image_name = "Birth.jpg"
        message_template = birth_temp.format(TeacherName=teacher_name)
        image_path = os.path.join(IMAGES_FOLDER, image_name)

        image = create_anniversary_image(teacher_name, image_path, 0.20)
        media = MediaFileUpload(image, mimetype="image/png")
        media_upload = upload_media(space_id, image, media)
        result = send_message(space_id, message_template, media_upload)
        print(f"Sent to: {teacher_name}")
        time.sleep(10)

    print("Birthday Messages Posted 😊👌👌")
    print("Process Finished...✅ You can Exit...☺️")

if __name__ == "__main__":
    main()
