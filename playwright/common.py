from playwright.sync_api import expect, Page
import tkinter as tk
import time

def go_to_profile(page: Page, login_vars: dict):
    page.goto(f"https://www.instagram.com/{login_vars["username"]}/")
    
def load_usernames_to_set(file, removal_only=False):
    
    file.seek(0)
    
    usernames = set()

    for line in file:
        line = line.strip()
        # Skip empty lines and lines that aren't likely usernames
        if not line:
            continue
            
        line_split = line.split(":")

        if removal_only:
            if line_split[1] == "N":
                usernames.add(line_split[0])
        else:
            usernames.add(line_split[0])
            
    file.seek(0)
    
    return usernames


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
    

def question_follower(page: Page, login_vars: dict, log, followers_list: list):
    
    follower_set = load_usernames_to_set(log) #get cached users
    
    print("Cached to Remove Users:")
    print(follower_set)
    # go_to_profile(page, login_vars)
    
    # followers_link = page.get_by_role("link", name="followers")
    
    # # follower_count = int(followers_link.text_content().strip("followers").strip(",").strip())
    # # print(follower_count)
    
    # following_link = page.get_by_role("link", name="following")
    
    # #aggregate followers
    # followers_link.click()
    
    # first_follower_username = page.get_by_role('link').nth(0).text_content().strip("/")
    # print(first_follower_username)
    
    
    # #hover first profile
    # profiles = page.get_by_role("dialog").get_by_role("link").filter(visible="True")

    # profiles.nth(0).hover()

    finish_flag = False
    c = 0
    
    for follower in followers_list:
        if finish_flag:
            break
        
        if follower["string_list_data"][0]["value"] in follower_set:
            continue
        
        c += 1

        print(f"Questioning {c}/{len(followers_list)-len(follower_set)}")
        
        page.goto(follower["string_list_data"][0]["href"])
    
    # while len(follower_set) != follower_count:
            
    #     for i in range(profiles.count()-5, profiles.count()):
    #         nth_follower_username_on_page = profiles.nth(i).text_content().strip("/").strip()
    #         # print(nth_follower_username_on_page)
    #         if nth_follower_username_on_page != '':
    #             follower_set.add(nth_follower_username_on_page)
    #             # print(f"Added {nth_follower_username_on_page}")
        
        
    #     print(f"Aggregated {len(follower_set)} users to question")
    #     scroll_amt = 100 #change
    #     page.mouse.wheel(0, scroll_amt)

        
        def on_green_button_click():
            print("Green button clicked!")
            log.write(follower["string_list_data"][0]["value"] + ":Y\n" )
            root.quit()
            root.destroy()
            
        def on_yellow_button_click():
            print("Yellow button clicked!")
            root.quit()
            root.destroy()
            
        def on_red_button_click():
            print("Red button clicked!")
            log.write(follower["string_list_data"][0]["value"] + ":N\n")
            log.flush()
            root.quit()
            root.destroy()
        
        def on_save_button_click():
            print("Finish button clicked!")
            root.quit()
            root.destroy() 
            nonlocal finish_flag
            finish_flag = True
        
        # Create the main window
        root = tk.Tk()
        root.title("Simple GUI")

        # Create a green button
        green_button = tk.Button(root, text="Keep 'em!", bg="green", fg="white", command=on_green_button_click)
        green_button.pack(padx=20, pady=10)

        # Create a red button
        red_button = tk.Button(root, text="Russian Roulette! 🎲", bg="#9c9119", fg="white", command=on_yellow_button_click)
        red_button.pack(padx=20, pady=10)
        
        # Create a red button
        yellow_button = tk.Button(root, text="Bye Bye :(", bg="red", fg="white", command=on_red_button_click)
        yellow_button.pack(padx=20, pady=10)

        save_button = tk.Button(root, text="Finish Now", bg="grey", fg="white", command=on_save_button_click)
        save_button.pack(padx=20, pady=10)
        
        # Run the main loop
        root.mainloop()
        
def remove_followers(removal_page_1, removal_page_2, removal_set):
    
    with open("removals.log", "a+") as file:
        
        file.write("Starting Cleanse\n")
        file.flush()
        
        for follower in removal_set:
            ####FIRST PAGE
            text_box_1 = removal_page_1.get_by_role("dialog").get_by_role("textbox")
            text_box_1.fill(follower)
            
            removal_page_1.wait_for_load_state()
            time.sleep(1)
            
            profile = removal_page_1.get_by_role("dialog").get_by_role("link").filter(visible="True")
            if profile.count() == 2: #1 entry else pass
                
                removal_button_1 = removal_page_1.get_by_role("dialog").get_by_role("button", name="Remove")
                removal_button_1.click()
                remove_follower_button_1 = removal_page_1.get_by_role("button", name="Remove")
                remove_follower_button_1.click()
                text_box_1.fill("")
                
                file.write(follower + ":followers\n")
                file.flush()
            
            ######### SECOND PAGE
            text_box_2 = removal_page_2.get_by_role("dialog").get_by_role("textbox")
            text_box_2.fill(follower)
            
            removal_page_2.wait_for_load_state()
            time.sleep(1)

            profile = removal_page_2.get_by_role("dialog").get_by_role("link").filter(visible="True")
            if profile.count() == 2: #1 entry else pass
            
                removal_button_2 = removal_page_2.get_by_role("dialog").get_by_role("button", name="Following")
                removal_button_2.click()
                unfollow_button_2 = removal_page_2.get_by_role("button", name="Unfollow")
                unfollow_button_2.click()
                text_box_2.fill("")

                file.write(follower + ":following\n")
                file.flush()
        