from common import *
from playwright.sync_api import expect, Page
import tkinter as tk

def test_clean_followers(page: Page, login_vars: dict, log):

    login(page, login_vars)
    
    question_follower(page, login_vars, log)    