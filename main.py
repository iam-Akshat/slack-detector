import mss
import time
import os
from datetime import datetime
import numpy as np
from skimage.metrics import structural_similarity as ssim
from PIL import Image
from google import genai
from pydantic import BaseModel, TypeAdapter
from playsound import playsound

# Store previous screenshots for comparison
previous_screenshots = {}
was_last_image_slacking = False

class IsUserSlackingResponse(BaseModel):
    isUserSlacking: bool
    reasoning: str

gemini_key = os.environ.get("GEMINI_API_KEY")
def ask_ai_if_user_is_slacking(paths):
    client = genai.Client(api_key=gemini_key)
    images = paths
    respone = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=["You will be supplied a series of screenshots. If the user is slacking, return 'true'. If the user is not slacking, return 'false'. The user is a software engineer so they should be working on a project. Looking at technical websites, code editors etc is considered working. Also provide reasoning", *images],
        config={
        'response_mime_type': 'application/json',
        'response_schema': IsUserSlackingResponse,
    },
    )
    print(respone.text)
    parsed_response : IsUserSlackingResponse = respone.parsed
    return parsed_response;

def play_alert_sound():
    """Play an alert sound."""
    sound_file = "alert.mp3"  # Make sure this file exists in your project directory
    try:
        playsound(sound_file)
    except Exception as e:
        print(f"Could not play alert sound: {e}")

def show_alert(monitor):
    """Display an alert image and play a sound on the unchanged monitor."""
    alert_img = "alert.jpg"
    img = Image.open(alert_img)
    width = monitor["width"]
    height = monitor["height"]
    
    img = img.resize((width, height))  # Resize to match monitor dimensions

    img.show()
    play_alert_sound()  # Play the alert sound
    print(f"Alert displayed on monitor {monitor}.")

def compare_images(img1, img2):
    """Compare two images using SSIM and return the similarity percentage."""
    img1_gray = np.array(img1.convert("L"))  # Convert to grayscale
    img2_gray = np.array(img2.convert("L"))  # Convert to grayscale

    similarity = ssim(img1_gray, img2_gray)
    return similarity  # Value between -1 and 1 (1 = identical)

def capture_screenshots():
    global previous_screenshots
    global was_last_image_slacking
    save_dir = "screenshots"
    os.makedirs(save_dir, exist_ok=True)

    with mss.mss() as sct:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            for monitor_num, monitor in enumerate(sct.monitors[1:], start=1):
                screenshot = sct.grab(monitor)
                img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

                # Compare with previous screenshot  
                if monitor_num in previous_screenshots:
                    similarity = compare_images(previous_screenshots[monitor_num], img)
                    print(f"Similarity with previous screenshot: {similarity}")
                    if similarity >= 0.9:
                        print("Image is similar to previous screenshot. Skipping API call.")
                        if was_last_image_slacking:
                            show_alert(monitor)
                            print(ai_response.reasoning)
                            print("User is still slacking (not calling api)")

                    else:
                        ai_response = ask_ai_if_user_is_slacking([img])
                        print("Making api call")
                        was_last_image_slacking = ai_response.isUserSlacking
                        if(ai_response.isUserSlacking):
                            show_alert(monitor)
                            print(ai_response.reasoning)
                            print("User is slacking")
                        else:
                            print("User is not slacking")
                        # Save new screenshot
                        file_path = os.path.join(save_dir, f"monitor_{monitor_num}_{timestamp}.png")
                        img.save(file_path)
                        print(f"Screenshot saved: {file_path}")

                        # Update previous screenshot
                        previous_screenshots[monitor_num] = img.copy()
                else:
                    ai_response = ask_ai_if_user_is_slacking([img])
                    print("Making api call")
                    was_last_image_slacking = ai_response.isUserSlacking
                    if(ai_response.isUserSlacking):
                        show_alert(monitor)
                        print(ai_response.reasoning)
                        print("User is slacking")
                    else:
                        print("User is not slacking")
                    
                    # Save new screenshot
                    file_path = os.path.join(save_dir, f"monitor_{monitor_num}_{timestamp}.png")
                    img.save(file_path)
                    print(f"Screenshot saved: {file_path}")

                    # Update previous screenshot
                    previous_screenshots[monitor_num] = img.copy()


                
                

            time.sleep(5)

if __name__ == "__main__":
    capture_screenshots()
