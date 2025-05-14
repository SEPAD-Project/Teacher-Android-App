import flet as ft

def main(page: ft.Page):
    # Page settings
    page.title = "Login System"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f5f5f5"
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Variables
    terms_accepted = ft.Ref[ft.Checkbox]()
    login_button = ft.Ref[ft.ElevatedButton]()
    
    # Form validation
    def validate_form(e):
        if all([
            username_field.value,
            password_field.value,
            terms_accepted.current.value
        ]):
            login_button.current.disabled = False
        else:
            login_button.current.disabled = True
        page.update()
    
    # Login button action
    def login_clicked(e):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Welcome {username_field.value}!"),
            bgcolor=ft.Colors.GREEN_400
        )
        page.snack_bar.open = True
        page.update()
    
    # UI Elements
    logo = ft.Image(
        src="https://cdn-icons-png.flaticon.com/512/6681/6681204.png",
        width=90,
        height=90,
        fit=ft.ImageFit.CONTAIN,
        color=ft.Colors.BLUE_700
    )
    
    header_text = ft.Text(
        "Login to Your Account",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_700
    )
    
    username_field = ft.TextField(
        label="Username",
        hint_text="Enter your username",
        width=400,
        border_radius=15,
        border_color=ft.Colors.BLUE_GREY_200,
        focused_border_color=ft.Colors.BLUE_700,
        prefix_icon=ft.Icons.PERSON,
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
        focused_border_color=ft.Colors.BLUE_700,
        prefix_icon=ft.Icons.LOCK,
        on_change=validate_form
    )
    
    terms_checkbox = ft.Checkbox(
        ref=terms_accepted,
        label="I agree to the terms and conditions",
        fill_color=ft.Colors.BLUE_700,
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
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            padding=15,
            elevation=5
        )
    )
    
    forgot_password = ft.TextButton(
        text="Forgot Password?",
        style=ft.ButtonStyle(color=ft.Colors.BLUE_700)
    )
    
    signup_text = ft.Row(
        [ft.Text("Don't have an account?"), 
         ft.TextButton("Sign Up", style=ft.ButtonStyle(color=ft.Colors.BLUE_700))],
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    # Create page
    login_form = ft.Container(
        ft.Column(
            [
                logo,
                header_text,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                username_field,
                password_field,
                ft.Row( 
                    [terms_checkbox],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                login_btn,
                ft.Row( 
                    [forgot_password],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                signup_text
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

ft.app(target=main, view=ft.AppView.WEB_BROWSER)