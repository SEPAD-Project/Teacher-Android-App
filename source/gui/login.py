import flet as ft
import configparser
import os

from pathlib import Path
import sys

project_root = Path(__file__).parent.parent 
sys.path.append(str(project_root))

from backend.auth import authenticate_user
from gui.dashboard import show_dashboard

def read_app_config():
    """Read app configuration from config.ini"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return {
        'theme': config['App']['Theme'],
        'primary_color': config['App']['PrimaryColor'],
        'secondary_color': config['App']['SecondaryColor']
    }

def main(page: ft.Page):
    # Read app config
    app_config = read_app_config()
    
    # Page settings
    page.title = "Teacher Login System"
    page.theme_mode = ft.ThemeMode.LIGHT if app_config['theme'] == 'light' else ft.ThemeMode.DARK
    page.bgcolor = app_config['secondary_color']
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Variables
    terms_accepted = ft.Ref[ft.Checkbox]()
    login_button = ft.Ref[ft.ElevatedButton]()
    
    # Form validation
    def validate_form(e):
        if all([
            national_code_field.value,
            password_field.value,
            terms_accepted.current.value
        ]):
            login_button.current.disabled = False
        else:
            login_button.current.disabled = True
        page.update()
    
    # Login button action
    def login_clicked(e):
        # Authenticate user
        user = authenticate_user(national_code_field.value, password_field.value)
        
        if user[0]:
            # Successful login
            teacher_name=user[1]['teacher_name']
            teacher_family=user[1]['teacher_family']
            teacher_national_code=user[1]['teacher_national_code']
            teacher_password=user[1]['teacher_password']
            lesson=user[1]['lesson']
            user_id=user[1]['id']
            show_dashboard(page, teacher_national_code, teacher_name+" "+teacher_family)
        else:
            # Failed login
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Invalid national code or password!"),
                bgcolor=ft.Colors.RED_400,
                behavior=ft.SnackBarBehavior.FLOATING
            )
            page.snack_bar.open = True
            page.update()
    
    # UI Elements
    logo = ft.Image(
        src="https://cdn-icons-png.flaticon.com/512/6681/6681204.png",
        width=90,
        height=90,
        fit=ft.ImageFit.CONTAIN,
        color=app_config['primary_color']
    )
    
    header_text = ft.Text(
        "Teacher Login System",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=app_config['primary_color']
    )
    
    national_code_field = ft.TextField(
        label="National Code",
        hint_text="Enter your national code",
        width=400,
        border_radius=15,
        border_color=ft.Colors.BLUE_GREY_200,
        focused_border_color=app_config['primary_color'],
        prefix_icon=ft.Icons.BADGE,
        on_change=validate_form
    )
    
    password_field = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        width=400,
        password=True,
        can_reveal_password=True,
        border_radius=15,
        border_color=ft.Colors.BLUE_GREY_200,
        focused_border_color=app_config['primary_color'],
        prefix_icon=ft.Icons.LOCK,
        on_change=validate_form
    )
    
    terms_checkbox = ft.Checkbox(
        ref=terms_accepted,
        label="I agree to the terms and conditions",
        fill_color=app_config['primary_color'],
        on_change=validate_form
    )
    
    login_btn = ft.ElevatedButton(
        ref=login_button,
        text="Login",
        width=400,
        height=50,
        disabled=True,
        on_click=login_clicked,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=app_config['primary_color'],
            color=ft.Colors.WHITE,
            padding=15,
            elevation=5
        )
    )
    
    forgot_password = ft.TextButton(
        text="Forgot Password?",
        style=ft.ButtonStyle(color=app_config['primary_color'])
    )
    
    # Create page
    login_form = ft.Container(
        ft.Column(
            [
                logo,
                header_text,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                national_code_field,
                password_field,
                ft.Row( 
                    [terms_checkbox],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                login_btn,
                ft.Row( 
                    [forgot_password],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=20,
        border_radius=15,
        bgcolor=ft.Colors.WHITE,
        width=440,  
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLUE_100,
            offset=ft.Offset(0, 0)
        )
    )
    
    page.add(login_form)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)