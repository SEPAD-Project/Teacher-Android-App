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

def show_dashboard(page: ft.Page, udata):
    """Show the dashboard after successful login"""
    # Read app config
    app_config = read_app_config()
    
    # Clear the page
    page.clean()
    
    # Update page settings
    page.title = f"Welcome {udata['teacher_name'] + ' '+ udata['teacher_family']}"
    page.theme_mode = ft.ThemeMode.LIGHT if app_config['theme'] == 'light' else ft.ThemeMode.DARK
    page.bgcolor = app_config['secondary_color']
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Welcome text
    welcome_text = ft.Text(
        f"Welcome {udata['teacher_name'] + ' '+ udata['teacher_family']}",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=app_config['primary_color'],
        text_align=ft.TextAlign.CENTER
    )
    
    # Common dimensions
    control_width = 400  # Same width for all controls
    control_height = 50  # Same height for all controls
    
    # Class dropdown with instruction text
    class_selector = ft.Column([
        ft.Text("Select your class:", size=16, color=ft.Colors.GREY_700),
        ft.Dropdown(
            hint_text="Choose from list",
            value="loading...",
            options=[
                ft.dropdown.Option("loading..."),
            ],
            width=control_width,
            border_color=app_config['primary_color'],
            text_size=16,
            content_padding=10,
        )
    ], spacing=10)
    
    # Enter class button
    enter_class_btn = ft.ElevatedButton(
        text="Enter Classroom",
        width=control_width,
        height=control_height,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=app_config['primary_color'],
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=20)
        )
    )
    
    # Logout button
    logout_btn = ft.ElevatedButton(
        text="Logout",
        width=control_width,
        height=control_height,
        on_click=lambda e: back_to_login(page),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=ft.Colors.RED_400,
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=20)
        )
    )
    
    # Main content container
    dashboard_content = ft.Container(
        ft.Column(
            [
                welcome_text,
                ft.Container(height=40),
                class_selector,
                ft.Container(height=30),
                enter_class_btn,
                ft.Container(height=20),
                logout_btn
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        ),
        padding=40,
        border_radius=15,
        bgcolor=ft.Colors.WHITE,
        width=650,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLUE_100,
            offset=ft.Offset(0, 0)
        )
    )
    
    page.add(dashboard_content)
    
    # Store the update function in page for external access
    def update_dropdown_options(new_options):
        class_selector.controls[1].options = [ft.dropdown.Option(opt) for opt in new_options]
        class_selector.controls[1].value = new_options[0] if new_options else "loading..."
        page.update()
    
    page.update_dropdown_options = update_dropdown_options

def back_to_login(page: ft.Page):
    """Return to login page"""
    from gui.login import main as login_main
    page.clean()
    login_main(page)

if __name__ == "__main__":
    # Sample user data for testing
    sample_user_data = {
        "teacher_name": "John",
        "teacher_family": "Smith",
        "teacher_national_code": "1234567890"
    }
    
    def main(page: ft.Page):
        show_dashboard(page, sample_user_data)
        
        # Example of updating dropdown after 2 seconds
        import threading
        def update_dropdown_later():
            import time
            time.sleep(2)
            page.update_dropdown_options(["Math Class", "Science Class", "Literature Class", "Language Class"])
        
        threading.Thread(target=update_dropdown_later, daemon=True).start()
    
    ft.app(target=main)