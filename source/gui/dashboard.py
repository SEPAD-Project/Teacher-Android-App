import flet as ft
import configparser
from pathlib import Path
import sys
from threading import Thread
from typing import Dict, List
from main import MainPage

# Add project root to path
project_root = Path(__file__).parent.parent 
sys.path.append(str(project_root))

from backend.database import get_teacher_classes, get_class_name

class Dashboard:
    """Dashboard class that handles the teacher dashboard UI and functionality"""
    
    def __init__(self, page: ft.Page, user_data: Dict):
        """
        Initialize the Dashboard with page and user data
        
        Args:
            page: The Flet page object
            user_data: Dictionary containing teacher information
        """
        self.page = page
        self.user_data = user_data
        self.app_config = self._read_app_config()
        self.class_info: List[Dict] = []  # Store complete class information
        self._setup_page()
        self._create_ui()
        
    def _read_app_config(self) -> Dict:
        """Read app configuration from config.ini file
        
        Returns:
            Dictionary containing theme settings and colors
        """
        config = configparser.ConfigParser()
        config.read('config.ini')
        return {
            'theme': config['App']['Theme'],
            'primary_color': config['App']['PrimaryColor'],
            'secondary_color': config['App']['SecondaryColor']
        }
    
    def _setup_page(self):
        """Configure page settings"""
        self.page.clean()
        self.page.title = f"Welcome {self.user_data['teacher_name'] + ' '+ self.user_data['teacher_family']}"
        self.page.theme_mode = ft.ThemeMode.LIGHT if self.app_config['theme'] == 'light' else ft.ThemeMode.DARK
        self.page.bgcolor = self.app_config['secondary_color']
        self.page.padding = 20
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def _create_ui(self):
        """Create all UI components for the dashboard"""
        self._create_welcome_text()
        self._create_class_selector()
        self._create_action_buttons()
        self._assemble_dashboard()
        
        # Load classes in background thread
        self._load_classes()
    
    def _create_welcome_text(self):
        """Create the welcome text widget"""
        self.welcome_text = ft.Text(
            f"Welcome {self.user_data['teacher_name'] + ' '+ self.user_data['teacher_family']}",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=self.app_config['primary_color'],
            text_align=ft.TextAlign.CENTER
        )
    
    def _create_class_selector(self):
        """Create the class selection dropdown"""
        # Common dimensions
        control_width = 400
        
        self.class_dropdown = ft.Dropdown(
            hint_text="Choose from list",
            value="loading...",
            options=[ft.dropdown.Option("loading...")],
            width=control_width,
            border_color=self.app_config['primary_color'],
            text_size=16,
            content_padding=10,
        )
        
        self.class_selector = ft.Column([
            ft.Text("Select your class:", size=16, color=ft.Colors.GREY_700),
            self.class_dropdown
        ], spacing=10)
    
    def _create_action_buttons(self):
        """Create the action buttons (Enter Classroom and Logout)"""
        # Common dimensions
        control_width = 400
        control_height = 50
        
        self.enter_class_btn = ft.ElevatedButton(
            text="Enter Classroom",
            width=control_width,
            height=control_height,
            on_click=self._handle_enter_classroom,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                bgcolor=self.app_config['primary_color'],
                color=ft.Colors.WHITE,
                padding=ft.padding.symmetric(horizontal=20)
            )
        )
        
        self.logout_btn = ft.ElevatedButton(
            text="Logout",
            width=control_width,
            height=control_height,
            on_click=self._back_to_login,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                bgcolor=ft.Colors.RED_400,
                color=ft.Colors.WHITE,
                padding=ft.padding.symmetric(horizontal=20)
            )
        )
    
    def _assemble_dashboard(self):
        """Assemble all components into the main dashboard container"""
        self.dashboard_content = ft.Container(
            ft.Column(
                [
                    self.welcome_text,
                    ft.Container(height=40),
                    self.class_selector,
                    ft.Container(height=30),
                    self.enter_class_btn,
                    ft.Container(height=20),
                    self.logout_btn
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
        
        self.page.add(self.dashboard_content)
    
    def _load_classes(self):
        """Load teacher's classes in a background thread"""
        def update_class_drop_menu():
            # Get class ids for the teacher
            result = get_teacher_classes(self.user_data['id'])
            
            if result[0]:  # If any class exists
                class_ids = result[1]
                self.class_info = []  # Reset class info
                
                # Get class names for each class id
                for class_id in class_ids:
                    class_data = get_class_name(class_id)
                    self.class_info.append(class_data)  # Store complete class info
                
                # Update dropdown with class names
                self._update_dropdown_options([info['class_name'] for info in self.class_info])
        
        # Start background thread
        update_thread = Thread(target=update_class_drop_menu)
        update_thread.start()
    
    def _update_dropdown_options(self, new_options: List[str]):
        """Update the class dropdown options
        
        Args:
            new_options: List of class names to display in dropdown
        """
        self.class_dropdown.options = [ft.dropdown.Option(opt) for opt in new_options]
        self.class_dropdown.value = new_options[0] if new_options else "No classes found"
        self.page.update()

    def _handle_enter_classroom(self, e):
        """Handle Enter Classroom button click
        
        Args:
            e: The event that triggered this callback
        """
        if not self.class_info:
            print("No class information available")
            return
            
        selected_class_name = self.class_dropdown.value
        selected_class = next(
            (cls for cls in self.class_info if cls['class_name'] == selected_class_name),
            None
        )
        
        if selected_class:
            # Navigate to classroom details page
            MainPage(self.page, selected_class, self.app_config, self.user_data)
        else:
            print("No class selected or class not found")


    def _back_to_login(self, e):
        """Return to login page
        
        Args:
            e: The event that triggered this callback
        """
        from gui.login import main as login_main
        self.page.clean()
        login_main(self.page)


def show_dashboard(page: ft.Page, user_data: Dict):
    """Show the dashboard (wrapper function for backward compatibility)
    
    Args:
        page: The Flet page object
        user_data: Dictionary containing teacher information
    """
    Dashboard(page, user_data)


if __name__ == "__main__":
    # Sample user data for testing
    sample_user_data = {
        "id": 1,
        "teacher_name": "mhrd",
        "teacher_family": "njfi",
        "teacher_national_code": "1234567890"
    }
    
    def main(page: ft.Page):
        """Main function for testing the dashboard"""
        dashboard = Dashboard(page, sample_user_data)
        
        # Example of updating dropdown after 2 seconds
        import threading
        def update_dropdown_later():
            import time
            time.sleep(2)
            # For testing, we'll mock some class info
            dashboard.class_info = [
                {
                },
                {
                }
            ]
            dashboard._update_dropdown_options([info['class_name'] for info in dashboard.class_info])
        
        threading.Thread(target=update_dropdown_later, daemon=True).start()
    
    ft.app(target=main)