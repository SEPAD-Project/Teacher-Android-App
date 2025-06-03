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
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Create class dropdown
    class_dropdown = ft.Dropdown(
        label="Class List",
        hint_text="Select a class",
        value="updating",
        options=[
            ft.dropdown.Option("updating"),
        ],
        width=300,
        autofocus=True,
        border_color=app_config['primary_color'],
        text_size=16,
    )
    
    # Function to update dropdown options
    def update_dropdown_options(new_options):
        class_dropdown.options = [ft.dropdown.Option(opt) for opt in new_options]
        class_dropdown.value = new_options[0] if new_options else "updating"
        page.update()
    
    # Create dashboard content
    welcome_text = ft.Text(
        f"Welcome, {udata['teacher_name'] + ' '+ udata['teacher_family']}!",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=app_config['primary_color']
    )
    
    user_info = ft.Text(
        f"National Code: {udata['teacher_national_code']}",
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
                ft.Divider(height=20),
                class_dropdown,
                ft.Divider(height=30),
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
    
    # Store the update function in page for external access
    page.update_dropdown_options = lambda options: update_dropdown_options(options)

def back_to_login(page: ft.Page):
    """Return to login page"""
    from gui.login import main as login_main
    page.clean()
    login_main(page)

if __name__ == "__main__":
    # Sample user data for testing
    sample_user_data = {
        "teacher_name": "John",
        "teacher_family": "Doe",
        "teacher_national_code": "1234567890"
    }
    
    def main(page: ft.Page):
        show_dashboard(page, sample_user_data)
        
        # Example of updating dropdown after 3 seconds
        import threading
        def update_dropdown_later():
            import time
            time.sleep(3)
            page.update_dropdown_options(["Class A", "Class B", "Class C", "Class D"])
        
        threading.Thread(target=update_dropdown_later, daemon=True).start()
    
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=44445)