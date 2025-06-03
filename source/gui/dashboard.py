import flet as ft
import configparser

from pathlib import Path
import sys

project_root = Path(__file__).parent.parent 
sys.path.append(str(project_root))

def read_app_config():
    """Read app configuration from config.ini"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return {
        'theme': config['App']['Theme'],
        'primary_color': config['App']['PrimaryColor'],
        'secondary_color': config['App']['SecondaryColor']
    }

def show_dashboard(page: ft.Page, username: str, full_name: str):
    """Show the dashboard after successful login"""
    # Read app config
    app_config = read_app_config()
    
    # Clear the page
    page.clean()
    
    # Update page settings
    page.title = f"Welcome {full_name}"
    page.theme_mode = ft.ThemeMode.LIGHT if app_config['theme'] == 'light' else ft.ThemeMode.DARK
    page.bgcolor = app_config['secondary_color']
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Create dashboard content
    welcome_text = ft.Text(
        f"Welcome, {full_name}!",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=app_config['primary_color']
    )
    
    user_info = ft.Text(
        f"National Code: {username}",
        size=16,
        color=ft.Colors.BLUE_GREY_600
    )
    
    logout_btn = ft.ElevatedButton(
        text="Logout",
        width=200,
        height=40,
        on_click=lambda e: back_to_login(page),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=app_config['primary_color'],
            color=ft.Colors.WHITE
        )
    )
    
    dashboard_content = ft.Container(
        ft.Column(
            [
                ft.Divider(height=50),
                welcome_text,
                ft.Divider(height=20),
                user_info,
                ft.Divider(height=40),
                logout_btn
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=30,
        border_radius=15,
        bgcolor=ft.Colors.WHITE,
        width=500,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLUE_100,
            offset=ft.Offset(0, 0)
        )
    )
    
    page.add(dashboard_content)

def back_to_login(page: ft.Page):
    """Return to login page"""
    from gui.login import main as login_main
    page.clean()
    login_main(page)