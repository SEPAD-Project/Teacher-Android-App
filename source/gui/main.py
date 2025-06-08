import flet as ft
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from backend.database import get_students_list_by_class_code

class MainPage:
    """Main page to show student attendance status in a table format"""
    
    def __init__(self, page: ft.Page, selected_class: Dict, app_config: Dict, user_data):
        self.page = page
        self.selected_class = selected_class
        self.app_config = app_config
        self.user_data = user_data
        self.student_data = []  # Initialize empty student data
        self._setup_page()
        
        # Initialize table data
        self.main_logic()
        
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
    
    def update_student_data(self, student_id: str, name: str, accuracy: str, last_review: str):
        """
        Update or add student data to the table
        Args:
            student_id: Student unique identifier
            name: Student name
            accuracy: Accuracy percentage
            last_review: Last review date/time
        """
        # Check if student already exists
        existing_student = next((s for s in self.student_data if s['id'] == student_id), None)
        
        if existing_student:
            # Update existing student
            existing_student['name'] = name
            existing_student['accuracy'] = accuracy
            existing_student['last_review'] = last_review
        else:
            # Add new student
            self.student_data.append({
                'id': student_id,
                'name': name,
                'accuracy': accuracy,
                'last_review': last_review
            })
        
        # Refresh UI
        self._create_ui()
        self.page.update()
    
    def main_logic(self):
        # .. get students national code list by class code
        # .. translate nationals code to name
        # .. set primary data (only names and non vaule for others)
        # calculate_time_difference func 
        # fetch message 
        # if message was not 'No messages yet' check status code and generate final text and time
        # manage accuracy data of each students 
        # set the final data of eache students on the table
        """
        Main function to fetch and process student data safely
        Handles potential errors to prevent crashes
        """
        try:
            # Get students list from database
            students_list = get_students_list_by_class_code(self.selected_class['id'])
            
            if students_list != 0:
                # Process each student
                for student in students_list:
                    try:
                        name = f"{student['student_name']+' '+student['student_family']}" 
                        accuracy = "0%"  
                        last_review = "Getting"
                        
                        # Update student data
                        self.update_student_data(student, name, accuracy, last_review)
                    
                    except Exception as e:
                        print(f"Error processing student {student}: {str(e)}")
                        continue
        
        except Exception as e:
            print(f"Error in main_logic: {str(e)}")
    
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
        
        # Create table only if we have student data
        if self.student_data:
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
        else:
            # Show empty state if no students
            table_content = ft.Text("No students found", size=20)
        
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
        
        MainPage(page, sample_class, app_config, {})
    
    ft.app(target=main)