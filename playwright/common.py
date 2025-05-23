from playwright.sync_api import expect, Page
import tkinter as tk


def go_to_profile(page: Page, login_vars: dict):
    page.goto(f"https://www.instagram.com/{login_vars["username"]}/")
    

def login(page: Page, login_vars: dict):
    #login
    page.goto("https://www.instagram.com/")

    username_textbox = page.get_by_role("textbox").nth(0)
    passowrd_textbox = page.get_by_role("textbox").nth(1)

    username_textbox.fill(login_vars["username"])
    passowrd_textbox.fill(login_vars["password"])
    

    submit_btn = page.get_by_role("button", name="Log in", exact=True)
    submit_btn.click()
    
    page.pause()

    #go to profile
    page.get_by_role("link", name="profile picture Profile").click()
    

def question_follower(page: Page, login_vars: dict, log):
    
    follower_set = set()
    
    
    log.write("Started Cleansing\n")

    go_to_profile(page, login_vars)
    
    followers_link = page.get_by_role("link", name="followers")
    
    follower_count = int(followers_link.text_content().strip("followers").strip(",").strip())
    print(follower_count)
    
    following_link = page.get_by_role("link", name="following")
    
    #aggregate followers
    followers_link.click()
    
    first_follower_username = page.get_by_role('link').nth(0).text_content().strip("/")
    print(first_follower_username)
    
    
    #hover first profile
    profiles = page.get_by_role("dialog").get_by_role("link").filter(visible="True")

    profiles.nth(0).hover()

    
    while len(follower_set) != follower_count:
            
        for i in range(profiles.count()-5, profiles.count()):
            nth_follower_username_on_page = profiles.nth(i).text_content().strip("/").strip()
            # print(nth_follower_username_on_page)
            if nth_follower_username_on_page != '':
                follower_set.add(nth_follower_username_on_page)
                # print(f"Added {nth_follower_username_on_page}")
        
        
        print(f"Aggregated {len(follower_set)} users to question")
        scroll_amt = 100 #change
        page.mouse.wheel(0, scroll_amt)

    
    # page.goto(f"https://www.instagram.com/{first_follower_username}/")
    
    # def on_green_button_click():
    #     print("Green button clicked!")
    #     root.quit()
        
    # def on_yellow_button_click():
    #     print("Yellow button clicked!")
    #     root.quit()
    
    # def on_red_button_click():
    #     print("Red button clicked!")
    #     root.quit()
    
    # # Create the main window
    # root = tk.Tk()
    # root.title("Simple GUI")

    # # Create a green button
    # green_button = tk.Button(root, text="Keep 'em!", bg="green", fg="white", command=on_green_button_click)
    # green_button.pack(padx=20, pady=10)

    # # Create a red button
    # red_button = tk.Button(root, text="Russian Roulette! 🎲", bg="#9c9119", fg="white", command=on_yellow_button_click)
    # red_button.pack(padx=20, pady=10)
    
    # # Create a red button
    # red_button = tk.Button(root, text="Bye Bye :(", bg="red", fg="white", command=on_red_button_click)
    # red_button.pack(padx=20, pady=10)

    # # Run the main loop
    # root.mainloop()