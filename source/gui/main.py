import flet as ft
from typing import Dict, List
import random
from datetime import datetime, timedelta

class MainPage:
    """Main page to show student attendance status in a table format"""
    
    def __init__(self, page: ft.Page, selected_class: Dict, app_config: Dict):
        """
        Initialize the main page
        
        Args:
            page: The Flet page object
            selected_class: Dictionary containing selected class information
            app_config: Dictionary containing app theme and color settings
        """
        self.page = page
        self.selected_class = selected_class
        self.app_config = app_config
        self.student_data = self._generate_sample_student_data()
        self._setup_page()
        self._create_ui()
    
    def _setup_page(self):
        """Configure page settings"""
        self.page.clean()
        self.page.title = f"Classroom: {self.selected_class['class_name']}"
        self.page.bgcolor = self.app_config['secondary_color']
        self.page.padding = 20
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def _generate_sample_student_data(self) -> List[Dict]:
        """Generate sample student data for demonstration
        
        Returns:
            List of dictionaries containing student information
        """
        students = []
        first_names = ["Ali", "Mohammad", "Ahmad", "Fatemeh", "Zahra", "Hossein", 
                      "Reza", "Maryam", "Sara", "Narges"]
        last_names = ["Mohammadi", "Ahmadi", "Alavi", "Hosseini", "Rahmani", 
                     "Kazemi", "Salehi", "Moradi", "Gholami", "Karimi"]
        
        for i in range(30):
            students.append({
                "id": i + 1,
                "name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "accuracy": f"{random.randint(50, 100)}%",
                "last_review": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            })
        return students
    
    def _create_header_row(self) -> ft.Row:
        """Create the table header row
        
        Returns:
            ft.Row containing the table headers
        """
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text("Name", weight=ft.FontWeight.BOLD),
                    width=200,
                    padding=10,
                    border=ft.border.all(1, self.app_config['primary_color'])),
                ft.Container(
                    content=ft.Text("Accuracy", weight=ft.FontWeight.BOLD),
                    width=150,
                    padding=10,
                    border=ft.border.all(1, self.app_config['primary_color'])),
                ft.Container(
                    content=ft.Text("Last Review", weight=ft.FontWeight.BOLD),
                    width=150,
                    padding=10,
                    border=ft.border.all(1, self.app_config['primary_color'])),
            ],
            spacing=0)

    
    def _create_student_row(self, student: Dict) -> ft.Row:
        """Create a table row for a student
        
        Args:
            student: Dictionary containing student information
            
        Returns:
            ft.Row containing the student data
        """
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(student['name']),
                    width=200,
                    padding=10,
                    border=ft.border.all(1, ft.Colors.GREY_300)),
                ft.Container(
                    content=ft.Text(student['accuracy']),
                    width=150,
                    padding=10,
                    border=ft.border.all(1, ft.Colors.GREY_300)),
                ft.Container(
                    content=ft.Text(student['last_review']),
                    width=150,
                    padding=10,
                    border=ft.border.all(1, ft.Colors.GREY_300)),
            ],
            spacing=0
        )
    
    def _create_back_button(self) -> ft.ElevatedButton:
        """Create the back button to return to dashboard
        
        Returns:
            ft.ElevatedButton configured for navigation
        """
        return ft.ElevatedButton(
            text="Back to Dashboard",
            width=400,
            height=50,
            on_click=self._return_to_dashboard,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                bgcolor=self.app_config['primary_color'],
                color=ft.Colors.WHITE,
                padding=ft.padding.symmetric(horizontal=20)
            )
        )
    
    def _create_ui(self):
        """Create all UI components for the classroom details page"""
        # Header with class info
        class_header = ft.Text(
            f"Class: {self.selected_class['class_name']}",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=self.app_config['primary_color'],
            text_align=ft.TextAlign.CENTER
        )
        
        # Create table header
        table_header = self._create_header_row()
        
        # Create student rows
        student_rows = [self._create_student_row(student) for student in self.student_data]
        
        # Create scrollable table
        table = ft.Column(
            controls=[table_header] + student_rows,
            scroll=ft.ScrollMode.ALWAYS,
            height=500
        )
        
        # Back button
        back_button = self._create_back_button()
        
        # Main content container
        content = ft.Container(
            ft.Column(
                [
                    class_header,
                    ft.Container(height=20),
                    table,
                    ft.Container(height=20),
                    back_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0
            ),
            padding=40,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            width=800,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.BLUE_100,
                offset=ft.Offset(0, 0)
            )
        )
        
        self.page.add(content)
    
    def _return_to_dashboard(self, e):
        """Return to the dashboard page
        
        Args:
            e: The event that triggered this callback
        """
        from gui.dashboard import show_dashboard
        show_dashboard(self.page, self.user_data)  # Assuming user_data is stored in app


# Sample usage in main (for testing)
if __name__ == "__main__":
    def main(page: ft.Page):
        # Sample config
        app_config = {
            'theme': 'light',
            'primary_color': ft.Colors.BLUE_600,
            'secondary_color': ft.Colors.BLUE_50
        }
        
        # Sample class data
        sample_class = {
            'class_id': 101,
            'class_name': 'Math Class',
            'class_description': 'Advanced Mathematics',
            'class_code': 'MATH101'
        }
        
        # Show the classroom details page directly for testing
        MainPage(page, sample_class, app_config)
    
    ft.app(target=main)