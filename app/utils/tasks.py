from fastapi import BackgroundTasks
from app.utils.email import send_email

def send_order_confirmation_email(background_tasks: BackgroundTasks, to_email: str, order_id: int):
    subject = f"Order #{order_id} Confirmation"
    body = f"Your order #{order_id} has been successfully placed."
    background_tasks.add_task(send_email, to_email, subject, body)

def send_custom_order_notification(background_tasks: BackgroundTasks, to_email: str, custom_order_id: int):
    subject = f"Custom Order #{custom_order_id} Update"
    body = f"Your custom order #{custom_order_id} is in progress."
    background_tasks.add_task(send_email, to_email, subject, body)
