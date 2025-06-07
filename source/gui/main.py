import flet as ft
from typing import Dict, List
import random
from datetime import datetime, timedelta

class MainPage:
    """Main page to show student attendance status in a table format"""
    
    def __init__(self, page: ft.Page, selected_class: Dict, app_config: Dict):
        self.page = page
        self.selected_class = selected_class
        self.app_config = app_config
        self.student_data = self._generate_sample_student_data()
        self._setup_page()
        self._create_ui()
        
        # Add resize event handler
        self.page.on_resize = self._handle_resize
    
    def _handle_resize(self, e):
        # Rebuild UI when page is resized
        self._create_ui()
        self.page.update()
    
    def _setup_page(self):
        self.page.clean()
        self.page.title = f"Classroom: {self.selected_class['class_name']}"
        self.page.bgcolor = self.app_config['secondary_color']
        self.page.padding = 20
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def _generate_sample_student_data(self) -> List[Dict]:
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
    
    def _create_header_row(self, is_portrait: bool) -> ft.Row:
        if is_portrait:
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
                spacing=0
            )
        else:
            return ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text("Name", weight=ft.FontWeight.BOLD),
                        expand=True,
                        padding=10,
                        border=ft.border.all(1, self.app_config['primary_color'])),
                    ft.Container(
                        content=ft.Text("Accuracy", weight=ft.FontWeight.BOLD),
                        expand=True,
                        padding=10,
                        border=ft.border.all(1, self.app_config['primary_color'])),
                    ft.Container(
                        content=ft.Text("Last Review", weight=ft.FontWeight.BOLD),
                        expand=True,
                        padding=10,
                        border=ft.border.all(1, self.app_config['primary_color'])),
                ],
                spacing=0
            )
    
    def _create_student_row(self, student: Dict, is_portrait: bool) -> ft.Row:
        if is_portrait:
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
        else:
            return ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(student['name']),
                        expand=True,
                        padding=10,
                        border=ft.border.all(1, ft.Colors.GREY_300)),
                    ft.Container(
                        content=ft.Text(student['accuracy']),
                        expand=True,
                        padding=10,
                        border=ft.border.all(1, ft.Colors.GREY_300)),
                    ft.Container(
                        content=ft.Text(student['last_review']),
                        expand=True,
                        padding=10,
                        border=ft.border.all(1, ft.Colors.GREY_300)),
                ],
                spacing=0
            )
    
    def _create_back_button(self) -> ft.ElevatedButton:
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
        # Clear existing controls
        self.page.controls.clear()
        
        # Determine current orientation
        is_portrait = self.page.height > self.page.width
        
        # Header with class info
        class_header = ft.Text(
            f"Class: {self.selected_class['class_name']}",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=self.app_config['primary_color'],
            text_align=ft.TextAlign.CENTER
        )
        
        # Create table
        table_header = self._create_header_row(is_portrait)
        student_rows = [self._create_student_row(student, is_portrait) for student in self.student_data]
        
        if is_portrait:
            # Portrait mode - fixed width with horizontal scrolling
            table = ft.Column(
                controls=[table_header] + student_rows,
                spacing=0,
                scroll=ft.ScrollMode.ALWAYS,
                height=min(500, self.page.height - 250)
            )
            
            table_container = ft.Container(
                content=table,
                width=520,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=5
            )
            
            # Horizontal scroll for portrait mode
            scrollable_table = ft.Row(
                [table_container],
                scroll=ft.ScrollMode.ALWAYS,
                width=self.page.width - 80
            )
            
            table_content = scrollable_table
        else:
            # Landscape mode - full width expanding table
            table = ft.Column(
                controls=[table_header] + student_rows,
                spacing=0,
                scroll=ft.ScrollMode.ALWAYS,
                height=min(500, self.page.height - 250)
            )
            
            table_container = ft.Container(
                content=table,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=5,
                alignment=ft.alignment.top_center,
                expand=True
            )
            
            table_content = table_container
        
        # Main content container
        content = ft.Container(
            ft.Column(
                [
                    class_header,
                    ft.Container(height=20),
                    table_content,
                    ft.Container(height=20),
                    self._create_back_button()
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                expand=False
            ),
            padding=40,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            width=min(1200, self.page.width + 400) if not is_portrait else min(600, self.page.width - 40),
            height=min(700, self.page.height - 40),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.BLUE_100,
                offset=ft.Offset(0, 0)
            ),
            alignment=ft.alignment.center
        )
        
        # Center everything on page
        self.page.add(
            ft.Container(
                content,
                alignment=ft.alignment.center,
                expand=True
            )
        )
    
    def _return_to_dashboard(self, e):
        from gui.dashboard import show_dashboard
        show_dashboard(self.page, self.user_data)

if __name__ == "__main__":
    def main(page: ft.Page):
        app_config = {
            'theme': 'light',
            'primary_color': ft.Colors.BLUE_600,
            'secondary_color': ft.Colors.BLUE_50
        }
        
        sample_class = {
            'class_id': 101,
            'class_name': 'Math Class',
            'class_description': 'Advanced Mathematics',
            'class_code': 'MATH101'
        }
        
        MainPage(page, sample_class, app_config)
    
    ft.app(target=main)