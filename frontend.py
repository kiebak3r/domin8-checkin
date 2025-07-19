import flet as ft
import asyncio
from flet import *
from backend import *


async def main(page: Page):
    # Page Configuration
    page.title = f'DOMIN8 {TITLE}'
    page.padding = 0
    page.bgcolor = ft.Colors.TRANSPARENT

    # Save both versions of the image using Pillow (in backend)
    save_image(flip=False, filename=normal_path)
    save_image(flip=True, filename=flipped_path)

    # Spinning Logo
    spinning_image = ft.Image(src=normal_path, width=150)
    spinning_logo = ft.Container(
        content=spinning_image,
        alignment=ft.alignment.center,
        padding=20
    )

    # Spinning Logo Logic
    async def flip_loop():
        flip = False
        while True:
            spinning_image.src = flipped_path if flip else normal_path
            page.update()
            flip = not flip
            await asyncio.sleep(1)
    asyncio.create_task(flip_loop())

    # Snack bar
    snack_title = ft.Text("", color="black", style=ft.TextThemeStyle.TITLE_MEDIUM)
    snack_text = ft.Text("", color="black", style=ft.TextThemeStyle.BODY_MEDIUM)
    snackbar = ft.SnackBar(
        ft.Column(
            controls=[],
            alignment="center",
            horizontal_alignment="center"
        ),
        show_close_icon=True,
        duration=6000
    )

    # Button click handler
    def submit_checkin(e):
        user_id = user_id_input.value.strip()
        snackbar.content.clean()
        snackbar.content.color = "white"

        if not user_id or not user_id.isdigit() or user_id == str(0):
            snack_title.value = INPUT_EMPTY_ERROR
            snackbar.bgcolor = "yellow"
            snackbar.content.controls.append(snack_title)
        else:
            status, text = verify_user(user_id)
            snackbar.bgcolor = "green" if status == 0 else "yellow" if status == 2 else "red"
            snack_title.value = text[0]
            snack_text.value = text[1]
            snackbar.content.controls.extend([snack_title, snack_text])

        page.update()
        page.open(snackbar)
        user_id_input.focus()

    # Check in Button
    checkin_button = TextButton(
        text="Check In",
        on_click=submit_checkin,
        style=ft.ButtonStyle(color=ft.Colors.WHITE),
    )

    # Input field for user ID
    user_id_input = TextField(
        label=INPUT_LABEL,
        width=300,
        border_color="yellow",
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
        autofocus=True,
        on_submit=submit_checkin
    )

    # Layout body
    body = Column(
        [
            spinning_logo,
            user_id_input,
            checkin_button,
            snackbar,
        ],
        spacing=20,
        alignment="center",
        horizontal_alignment="center",
    )

    # Page layout
    page.add(
        Stack(
            controls=[
                ft.Image(
                    src=BACKGROUND,
                    fit="cover",
                    width=float("inf"),
                    height=float("inf"),
                ),
                Container(
                    content=body,
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            expand=True,
        ),
    )


if __name__ == "__main__":
    init_db()
    ft.app(target=main)
