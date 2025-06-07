from common import *
from playwright.sync_api import expect, Page
import tkinter as tk

def test_clean_followers(browser, login_vars: dict, log, followers_list):

    context = browser.new_context()
    page = context.new_page()
    
    login(page, login_vars)
    
    question_follower(page, login_vars, log, followers_list)    
    
    
    removal_set = load_usernames_to_set(log, removal_only=True)
    
    print(f"Removing following users: {removal_set}")
    
    choice = input("Please Enter 'CONFIRM' to confirm removal of following users: ")
    
    if choice=="CONFIRM":
        removal_page_1 = context.new_page()
        removal_page_2 = context.new_page()
        
        go_to_profile(removal_page_1, login_vars)
        go_to_profile(removal_page_2, login_vars)
        
        followers_link = removal_page_1.get_by_role("link", name="followers")
        following_link = removal_page_2.get_by_role("link", name="following")

        followers_link.click()
        following_link.click()
        
        removal_page_2.pause()
        
        remove_followers(removal_page_1, removal_page_2, removal_set)
    